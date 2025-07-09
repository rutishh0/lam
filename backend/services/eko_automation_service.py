"""
Eko Automation Service - Interface with Eko framework for advanced automation workflows

This service bridges Python backend with Eko's JavaScript automation capabilities.
"""

import asyncio
import json
import logging
import subprocess
import tempfile
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from utils.config import get_config

logger = logging.getLogger(__name__)

class EkoAutomationService:
    """Service to interface with Eko framework for automation workflows"""
    
    def __init__(self):
        self.config = get_config()
        self.eko_script_path = Path(__file__).parent / "eko_scripts"
        self.eko_script_path.mkdir(exist_ok=True)
        
    async def initialize_eko_environment(self) -> bool:
        """Initialize Eko environment and dependencies"""
        try:
            # Check if Eko is installed
            result = await self._run_node_command(["npm", "list", "@eko-ai/eko"])
            if result["success"]:
                logger.info("Eko framework is already installed")
                return True
            
            # Install Eko if not present
            logger.info("Installing Eko framework...")
            install_result = await self._run_node_command(["npm", "install", "@eko-ai/eko", "@eko-ai/eko-nodejs"])
            
            if install_result["success"]:
                logger.info("Eko framework installed successfully")
                return True
            else:
                logger.error(f"Failed to install Eko: {install_result['error']}")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing Eko environment: {str(e)}")
            return False
    
    async def create_automation_workflow(
        self,
        task_description: str,
        client_data: Optional[Dict] = None,
        university_data: Optional[Dict] = None,
        documents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create and execute an automation workflow using natural language
        
        Args:
            task_description: Natural language description of the task
            client_data: Client information for form filling
            university_data: University-specific requirements
            documents: List of document paths to include
            
        Returns:
            Dictionary with workflow execution results
        """
        try:
            # Create workflow configuration
            workflow_config = {
                "task": task_description,
                "client_data": client_data or {},
                "university_data": university_data or {},
                "documents": documents or [],
                "llm_config": {
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-20250514",
                    "apiKey": os.getenv("ANTHROPIC_API_KEY"),
                }
            }
            
            # Generate Eko script
            script_content = await self._generate_eko_script(workflow_config)
            
            # Execute workflow
            result = await self._execute_eko_workflow(script_content)
            
            return {
                "success": True,
                "workflow_id": result.get("workflow_id"),
                "result": result.get("result"),
                "steps_completed": result.get("steps_completed", []),
                "execution_time": result.get("execution_time"),
                "metadata": result.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error creating automation workflow: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def university_application_automation(
        self,
        university_name: str,
        application_url: str,
        client_profile: Dict,
        documents: List[str]
    ) -> Dict[str, Any]:
        """
        Automate university application process
        
        Args:
            university_name: Name of the university
            application_url: URL of application portal
            client_profile: Client's profile information
            documents: List of required documents
            
        Returns:
            Application automation results
        """
        task_description = f"""
        Complete university application for {university_name}:
        1. Navigate to {application_url}
        2. Create account or login if existing
        3. Fill personal information section using provided client data
        4. Upload required documents: {', '.join(documents)}
        5. Complete academic history section
        6. Fill program preferences and personal statement
        7. Review all information for accuracy
        8. Submit application if everything is correct
        9. Save confirmation details and application reference number
        10. Take screenshot of confirmation page
        """
        
        return await self.create_automation_workflow(
            task_description=task_description,
            client_data=client_profile,
            university_data={"name": university_name, "url": application_url},
            documents=documents
        )
    
    async def monitor_application_status(
        self,
        applications: List[Dict]
    ) -> Dict[str, Any]:
        """
        Monitor status of multiple university applications
        
        Args:
            applications: List of application details with URLs and credentials
            
        Returns:
            Status monitoring results
        """
        application_list = []
        for app in applications:
            application_list.append(f"- {app['university']}: {app['portal_url']}")
        
        task_description = f"""
        Monitor application status for multiple universities:
        {chr(10).join(application_list)}
        
        For each application:
        1. Login to the application portal
        2. Navigate to application status page
        3. Check current status and any updates
        4. Screenshot status page if changed
        5. Note any required actions or deadlines
        6. Compile status report with all findings
        """
        
        return await self.create_automation_workflow(
            task_description=task_description,
            client_data={"applications": applications}
        )
    
    async def document_preparation_workflow(
        self,
        required_documents: List[str],
        client_documents: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Automate document preparation and formatting
        
        Args:
            required_documents: List of required document types
            client_documents: Mapping of document types to file paths
            
        Returns:
            Document preparation results
        """
        task_description = f"""
        Prepare and format documents for university applications:
        
        Required documents: {', '.join(required_documents)}
        
        Tasks:
        1. Verify all required documents are present
        2. Check document formats and convert if necessary
        3. Ensure all documents meet university requirements
        4. Create a consolidated document package
        5. Generate document checklist
        6. Prepare backup copies in cloud storage
        """
        
        return await self.create_automation_workflow(
            task_description=task_description,
            client_data={"documents": client_documents}
        )
    
    async def _generate_eko_script(self, config: Dict) -> str:
        """Generate Eko JavaScript execution script"""
        script_template = """
import { Eko, Agent, Log, LLMs, StreamCallbackMessage } from "@eko-ai/eko";
import { BrowserAgent, FileAgent } from "@eko-ai/eko-nodejs";

const config = {config_json};

const llms = {{
  default: {{
    provider: config.llm_config.provider,
    model: config.llm_config.model,
    apiKey: config.llm_config.apiKey,
  }}
}};

const callback = {{
  onMessage: async (message) => {{
    if (message.type === "workflow" && !message.streamDone) return;
    if (message.type === "text" && !message.streamDone) return;
    if (message.type === "tool_streaming") return;
    
    console.log("EKO_MESSAGE:", JSON.stringify(message));
  }}
}};

async function executeWorkflow() {{
  try {{
    Log.setLevel(1);
    
    const agents = [new BrowserAgent(), new FileAgent()];
    const eko = new Eko({{ llms, agents, callback }});
    
    const result = await eko.run(config.task);
    
    console.log("EKO_RESULT:", JSON.stringify({{
      success: true,
      result: result.result,
      workflow_id: Date.now().toString(),
      execution_time: Date.now(),
      metadata: config
    }}));
    
  }} catch (error) {{
    console.log("EKO_ERROR:", JSON.stringify({{
      success: false,
      error: error.message,
      stack: error.stack
    }}));
  }}
}}

executeWorkflow();
        """
        
        return script_template.replace("{config_json}", json.dumps(config))
    
    async def _execute_eko_workflow(self, script_content: str) -> Dict[str, Any]:
        """Execute Eko workflow script"""
        try:
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                # Execute Node.js script
                result = await self._run_node_command(["node", script_path])
                
                if result["success"]:
                    # Parse Eko output
                    output_lines = result["output"].split('\n')
                    eko_result = None
                    
                    for line in output_lines:
                        if line.startswith("EKO_RESULT:"):
                            eko_result = json.loads(line[11:])
                            break
                        elif line.startswith("EKO_ERROR:"):
                            error_data = json.loads(line[10:])
                            raise Exception(error_data["error"])
                    
                    return eko_result or {"success": False, "error": "No result received"}
                else:
                    raise Exception(f"Node.js execution failed: {result['error']}")
                    
            finally:
                # Clean up temporary file
                os.unlink(script_path)
                
        except Exception as e:
            logger.error(f"Error executing Eko workflow: {str(e)}")
            raise
    
    async def _run_node_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run Node.js command and return result"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.eko_script_path
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": stderr.decode(),
                "return_code": process.returncode
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }

# Global service instance
eko_service = EkoAutomationService() 