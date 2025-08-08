"""Agent-style API routes.

Endpoints:
- POST /api/agent/threads -> {thread_id}
- GET  /api/agent/threads/{thread_id}/messages -> [messages]
- POST /api/agent/runs -> {run_id}
- GET  /api/agent/runs/{run_id} -> status/result
- WS   /ws/agent/{run_id} -> progress events
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from security.auth import get_current_user
from services.agent_service import get_agent_service

router = APIRouter(prefix="/api/agent", tags=["Agent"])


class CreateThreadResponse(BaseModel):
    thread_id: str


@router.post("/threads", response_model=CreateThreadResponse)
async def create_thread(current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()
    thread_id = service.create_thread(user_id=current_user["id"])
    return CreateThreadResponse(thread_id=thread_id)


@router.get("/threads/{thread_id}/messages", response_model=List[Dict[str, Any]])
async def get_messages(thread_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()
    # (MVP: no ownership check; add later)
    return service.get_messages(thread_id)


class AddMessageRequest(BaseModel):
    role: str = Field(default="user")
    content: str
    attachments: Optional[List[str]] = None


@router.post("/threads/{thread_id}/messages", response_model=dict)
async def add_message(thread_id: str, req: AddMessageRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()
    service.add_message(thread_id, req.role, req.content, req.attachments)
    return {"ok": True}


class CreateRunRequest(BaseModel):
    thread_id: str
    target_url: Optional[str] = None
    mode: str = Field(default="general")


class CreateRunResponse(BaseModel):
    run_id: str
    status: str


@router.post("/runs", response_model=CreateRunResponse)
async def create_run(req: CreateRunRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()
    run_id = service.create_run(thread_id=req.thread_id, user_id=current_user["id"])
    return CreateRunResponse(run_id=run_id, status="queued")


@router.get("/runs/{run_id}", response_model=Dict[str, Any])
async def get_run(run_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()
    run = service.get_run(run_id)
    return {"id": run.id, "thread_id": run.thread_id, "status": run.status, "error": run.error, "result": run.result}


class StartRunRequest(BaseModel):
    target_url: Optional[str] = None
    mode: str = Field(default="general")


@router.post("/runs/{run_id}/start", response_model=dict)
async def start_run(run_id: str, req: StartRunRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    service = get_agent_service()

    # Fire-and-forget execution; progress will be streamed via WS
    async def _noop(_event: Dict[str, Any]):
        return None

    import asyncio
    asyncio.create_task(service.execute_run(run_id, target_url=req.target_url, mode=req.mode, progress=_noop))
    return {"ok": True}


# WebSocket for run progress
@router.websocket("/ws/agent/{run_id}")
async def ws_agent(websocket: WebSocket, run_id: str):
    await websocket.accept()

    service = get_agent_service()

    # Relay progress events to this socket
    async def relay(event: Dict[str, Any]):
        try:
            await websocket.send_json(event)
        except Exception:
            pass

    service.register_progress_callback(run_id, relay)
    try:
        # Start sending ping to keep alive
        import asyncio
        async def keepalive():
            while True:
                await asyncio.sleep(30)
                await websocket.send_json({"type": "ping"})

        ka_task = asyncio.create_task(keepalive())

        # Attach progress and wait until run completes by polling
        while True:
            run = service.get_run(run_id)
            if run.status in ("completed", "error"):
                await websocket.send_json({"type": "final", "status": run.status, "error": run.error, "result": run.result})
                break
            await asyncio.sleep(1)
        ka_task.cancel()

    except WebSocketDisconnect:
        pass
    except Exception:
        try:
            await websocket.send_json({"type": "error", "error": "ws_failed"})
        except Exception:
            pass
    finally:
        try:
            service.unregister_progress_callback(run_id, relay)
        except Exception:
            pass

