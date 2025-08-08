"""
LLM Service for AI LAM

Enhanced LLM API interface following Suna's patterns for making calls to various language models.
Supports streaming, tool calls, retry logic, and comprehensive error handling.
"""

import os
import json
import asyncio
import logging
from typing import Union, Dict, Any, Optional, List, AsyncGenerator
from datetime import datetime
import litellm
from utils.config import get_config

# Initialize logger
logger = logging.getLogger(__name__)

# Configuration
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 30
RETRY_DELAY = 0.1

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass

class LLMRetryError(LLMError):
    """Exception raised when retries are exhausted."""
    pass

class LLMService:
    """Enhanced LLM service with unified API interface."""
    
    def __init__(self):
        self.config = get_config()
        self._setup_api_keys()
        self.default_model = getattr(self.config, 'DEFAULT_MODEL', 'gemini-2.5-flash')
    
    def _setup_api_keys(self) -> None:
        """Set up API keys from configuration."""
        providers = {
            'OPENAI_API_KEY': getattr(self.config, 'OPENAI_API_KEY', None),
            'ANTHROPIC_API_KEY': getattr(self.config, 'ANTHROPIC_API_KEY', None),
            'GOOGLE_API_KEY': getattr(self.config, 'GOOGLE_API_KEY', None),
        }
        
        for provider, key in providers.items():
            if key:
                os.environ[provider] = key
                logger.debug(f"API key configured for {provider}")
            else:
                logger.warning(f"No API key found for {provider}")
    
    async def _handle_error(self, error: Exception, attempt: int, max_attempts: int) -> None:
        """Handle API errors with appropriate delays and logging."""
        delay = RATE_LIMIT_DELAY if isinstance(error, litellm.exceptions.RateLimitError) else RETRY_DELAY
        logger.warning(f"Error on attempt {attempt + 1}/{max_attempts}: {str(error)}")
        logger.debug(f"Waiting {delay} seconds before retry...")
        await asyncio.sleep(delay)
    
    def _prepare_params(
        self,
        messages: List[Dict[str, Any]],
        model_name: str,
        temperature: float = 0,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Prepare parameters for the API call following Suna's pattern."""
        # Normalize common Gemini aliases
        model_normalized = (model_name or self.default_model).strip()
        alias_map = {
            "gemini-2.5": "gemini-2.5-flash",
            "gemini-2.5-flash": "gemini-2.5-flash",
            "gemini-2.5-flash-exp": "gemini-2.5-flash",
            "gemini-2.0-flash": "gemini-2.5-flash",
            "gemini-1.5-flash": "gemini-1.5-flash",
        }
        model_normalized = alias_map.get(model_normalized, model_normalized)

        params = {
            "model": model_normalized,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        
        # Handle max tokens
        if max_tokens is not None:
            param_name = "max_completion_tokens" if 'o1' in model_name else "max_tokens"
            params[param_name] = max_tokens
        
        # Add tools if provided
        if tools:
            params.update({
                "tools": tools,
                "tool_choice": tool_choice
            })
            logger.debug(f"Added {len(tools)} tools to API parameters")
        
        # Model-specific configurations
        if "claude" in model_normalized.lower() or "anthropic" in model_normalized.lower():
            params["extra_headers"] = {
                "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
            }
            logger.debug("Added Claude-specific headers")
        
        # Add any additional parameters
        params.update(kwargs)
        
        return params
    
    async def make_api_call(
        self,
        messages: List[Dict[str, Any]],
        model_name: str,
        temperature: float = 0,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], AsyncGenerator]:
        """
        Make an API call to a language model using LiteLLM.
        
        Args:
            messages: List of message dictionaries for the conversation
            model_name: Name of the model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in the response
            tools: List of tool definitions for function calling
            tool_choice: How to select tools ("auto" or "none")
            stream: Whether to stream the response
            **kwargs: Additional parameters
        
        Returns:
            Union[Dict[str, Any], AsyncGenerator]: API response or stream
        
        Raises:
            LLMRetryError: If API call fails after retries
            LLMError: For other API-related errors
        """
        logger.info(f"Making LLM API call to model: {model_name}")
        params = self._prepare_params(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice,
            stream=stream,
            **kwargs
        )
        
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Attempt {attempt + 1}/{MAX_RETRIES}")
                response = await litellm.acompletion(**params)
                logger.debug(f"Successfully received API response from {model_name}")
                return response
            
            except (litellm.exceptions.RateLimitError, Exception) as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    await self._handle_error(e, attempt, MAX_RETRIES)
                else:
                    break
        
        error_msg = f"Failed to make API call after {MAX_RETRIES} attempts"
        if last_error:
            error_msg += f". Last error: {str(last_error)}"
        logger.error(error_msg, exc_info=True)
        raise LLMRetryError(error_msg)
    
    async def generate_response(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a simple text response.
        
        Args:
            prompt: The user prompt
            model_name: Model to use (defaults to config default)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            system_prompt: Optional system prompt
        
        Returns:
            str: The generated response text
        """
        model = (model_name or self.default_model)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.make_api_call(
                messages=messages,
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise LLMError(f"Failed to generate response: {str(e)}")
    
    async def generate_with_tools(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        model_name: Optional[str] = None,
        temperature: float = 0,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate response with tool calling capabilities.
        
        Args:
            messages: Conversation messages
            tools: Available tools
            model_name: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens
        
        Returns:
            Dict[str, Any]: Response with potential tool calls
        """
        model = (model_name or self.default_model)
        
        try:
            response = await self.make_api_call(
                messages=messages,
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
                tool_choice="auto"
            )
            return response
        except Exception as e:
            logger.error(f"Error generating response with tools: {e}")
            raise LLMError(f"Failed to generate response with tools: {str(e)}")

# Global instance
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create the global LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service 