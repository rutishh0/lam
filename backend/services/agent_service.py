"""
Agent Service

Implements a simple Agent-style orchestration with threads, messages, runs,
tool execution (browser automation + data parsing), and progress streaming hooks.

Note: For MVP, thread/run state is kept in-memory. Supabase persistence can be
added in a follow-up increment by wiring calls to database.supabase_client.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from automation.ai_enhanced_automation import AIEnhancedAutomation
from automation.enhanced_data_parser import EnhancedDataParser


RunProgressCallback = Callable[[Dict[str, Any]], asyncio.Future | Any]


@dataclass
class AgentMessage:
    role: str
    content: str
    attachments: List[str] = field(default_factory=list)


@dataclass
class AgentThread:
    id: str
    user_id: str
    messages: List[AgentMessage] = field(default_factory=list)


@dataclass
class AgentRun:
    id: str
    thread_id: str
    user_id: str
    status: str = "queued"  # queued | running | completed | error
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class AgentService:
    def __init__(self) -> None:
        self._threads: Dict[str, AgentThread] = {}
        self._runs: Dict[str, AgentRun] = {}
        self._progress_callbacks: Dict[str, List[RunProgressCallback]] = {}

    # Threads & messages
    def create_thread(self, user_id: str) -> str:
        thread_id = str(uuid.uuid4())
        self._threads[thread_id] = AgentThread(id=thread_id, user_id=user_id)
        return thread_id

    def add_message(self, thread_id: str, role: str, content: str, attachments: Optional[List[str]] = None) -> None:
        thread = self._threads.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        thread.messages.append(AgentMessage(role=role, content=content, attachments=attachments or []))

    def get_messages(self, thread_id: str) -> List[Dict[str, Any]]:
        thread = self._threads.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        return [
            {"role": m.role, "content": m.content, "attachments": m.attachments}
            for m in thread.messages
        ]

    # Runs
    def create_run(self, thread_id: str, user_id: str) -> str:
        if thread_id not in self._threads:
            raise ValueError("Thread not found")
        run_id = str(uuid.uuid4())
        self._runs[run_id] = AgentRun(id=run_id, thread_id=thread_id, user_id=user_id)
        return run_id

    def get_run(self, run_id: str) -> AgentRun:
        run = self._runs.get(run_id)
        if not run:
            raise ValueError("Run not found")
        return run

    # Progress subscription
    def register_progress_callback(self, run_id: str, cb: RunProgressCallback) -> None:
        self._progress_callbacks.setdefault(run_id, []).append(cb)

    def unregister_progress_callback(self, run_id: str, cb: RunProgressCallback) -> None:
        callbacks = self._progress_callbacks.get(run_id)
        if not callbacks:
            return
        try:
            callbacks.remove(cb)
        except ValueError:
            pass

    async def execute_run(
        self,
        run_id: str,
        *,
        target_url: Optional[str],
        mode: str = "general",
        progress: Optional[RunProgressCallback] = None,
    ) -> None:
        """Execute the run using the current thread context.

        - Parses any uploaded data (future: use file store)
        - Calls AIEnhancedAutomation.intelligent_form_automation
        - Emits progress events via callback
        """
        run = self.get_run(run_id)
        run.status = "running"

        async def emit(event: Dict[str, Any]) -> None:
            # Broadcast to any registered WS callbacks
            for cb in list(self._progress_callbacks.get(run_id, [])):
                try:
                    maybe = cb(event)
                    if asyncio.iscoroutine(maybe):
                        await maybe
                except Exception:
                    # Best-effort progress
                    pass
            # Also emit to explicitly provided callback (optional)
            if progress:
                try:
                    maybe2 = progress(event)
                    if asyncio.iscoroutine(maybe2):
                        await maybe2
                except Exception:
                    pass

        try:
            thread = self._threads[run.thread_id]

            # In MVP, try to extract structured data from last user message attachments/content
            user_messages = [m for m in thread.messages if m.role == "user"]
            last_user = user_messages[-1] if user_messages else None
            user_text_data = last_user.content if last_user else ""
            attachments = (last_user.attachments if last_user else []) or []

            await emit({"type": "status", "status": "preparing", "run_id": run_id})

            parser = EnhancedDataParser()
            parsed_records: List[Dict[str, Any]] = []

            # If attachments are present, assume they are already read upstream (future: files service)
            # For MVP, parse plaintext as a single record; CSV parsing is handled when file bytes are provided
            if user_text_data:
                parsed_records.append({"plaintext": user_text_data})

            # Fallback minimal data to avoid empty payloads
            if not parsed_records:
                parsed_records = [{"note": "no_data_provided"}]

            automation = AIEnhancedAutomation()

            async def progress_callback(update: Dict[str, Any]) -> None:
                await emit({"type": "tool_progress", "run_id": run_id, **update})

            await emit({"type": "status", "status": "starting_browser", "run_id": run_id})

            result = await automation.intelligent_form_automation(
                url=target_url or "https://example.com",
                user_data=parsed_records[0],
                session_id=run_id,
                automation_type=mode,
                progress_callback=progress_callback,
            )

            run.status = "completed"
            run.result = result
            await emit({"type": "completed", "run_id": run_id, "result": result})

        except Exception as e:
            run.status = "error"
            run.error = str(e)
            await emit({"type": "error", "run_id": run_id, "error": str(e)})


# Global singleton
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service


