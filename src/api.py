"""
REST API server for the AI Agent framework.
Provides HTTP endpoints for planning, execution, and management.
Includes Phase 3 features: WebSocket, Authentication, Templates, Analytics.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect, Header
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import json
import asyncio
import sys
import os

# Add current directory to path to allow relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config_and_llm
from agent.planner import Planner
from agent.executor import Executor
from agent.history import ConversationHistory
from persistence import DatabaseManager, PersistentPlanner

# Phase 3 imports
from websocket_support import manager as ws_manager, EventBroadcaster
from auth import TokenManager, APIKeyManager, get_current_user, get_current_admin, verify_credentials, User, DEMO_CREDENTIALS
from templates import TemplateLibrary
from analytics import analytics, metrics_collector
from api_keys_routes import router as api_keys_router
from api_key_middleware import APIKeyAuthMiddleware


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Phase 3 services
token_manager = TokenManager()
api_key_manager = APIKeyManager()
template_library = TemplateLibrary()

# Security
security = HTTPBearer()


# Helper function to extract bearer token
async def get_token_from_header(authorization: str = Header(None)) -> str:
    """Extract bearer token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return authorization[7:]  # Remove "Bearer " prefix


# Pydantic models
class PlanRequest(BaseModel):
    """Request to create a plan."""
    goal: str
    repo_path: str = "."


class TaskExecutionRequest(BaseModel):
    """Request to execute a task."""
    plan_id: int
    task_id: int


class ConversationMessage(BaseModel):
    """A message in the conversation."""
    role: str
    content: str


class PlanResponse(BaseModel):
    """Response with plan information."""
    plan_id: int
    goal: str
    tasks: int
    status: str


class TaskResponse(BaseModel):
    """Response with task information."""
    task_id: int
    description: str
    completed: bool
    result: Optional[str] = None


class ExecutionResponse(BaseModel):
    """Response from task execution."""
    success: bool
    result: str
    execution_id: int


# Phase 3 Models
class LoginRequest(BaseModel):
    """Authentication login request."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str


class APIKeyResponse(BaseModel):
    """API key response."""
    api_key: str
    created_at: str
    expires_at: Optional[str]


class TemplateResponse(BaseModel):
    """Template response."""
    id: str
    name: str
    description: str
    difficulty: str
    tags: List[str]
    task_count: int


class AnalyticsResponse(BaseModel):
    """Analytics response."""
    task_id: int
    execution_count: int
    success_rate: float
    avg_duration: float
    total_results_length: int


# Initialize app
app = FastAPI(
    title="AI Agent API",
    description="REST API for the AI Agent framework",
    version="0.1.0"
)

# Add API key authentication middleware
app.add_middleware(APIKeyAuthMiddleware)

# Include API key management routes
app.include_router(api_keys_router)

# Global state
db_manager = DatabaseManager()
config, llm = load_config_and_llm()

# Store active planners and executors
active_sessions = {}
session_counter = 0


@app.on_event("shutdown")
def shutdown_event():
    """Clean up on shutdown."""
    db_manager.close()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_provider": config.get("llm", {}).get("provider"),
        "version": "0.2.0"
    }


@app.get("/plans/{plan_id}")
async def get_plan(plan_id: int):
    """Get plan details."""
    try:
        plan = db_manager.get_plan(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        tasks = db_manager.get_plan_tasks(plan_id)
        stats = db_manager.get_plan_statistics(plan_id)
        
        return {
            "plan": plan,
            "tasks": tasks,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Error retrieving plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/plans")
async def list_plans(limit: int = 50):
    """List all plans."""
    try:
        plans = db_manager.get_all_plans(limit)
        return {"plans": plans, "total": len(plans)}
    except Exception as e:
        logger.error(f"Error listing plans: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/plans/{plan_id}/execute")
async def execute_task(plan_id: int, request: TaskExecutionRequest, background_tasks: BackgroundTasks):
    """Execute a task."""
    try:
        if plan_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Plan session not found")
        
        session = active_sessions[plan_id]
        planner = session["planner"]
        executor = session["executor"]
        history = session["history"]
        
        if request.task_id not in planner.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = planner.tasks[request.task_id]
        
        # Execute in background
        async def execute_background():
            try:
                result = executor.execute_task(task)
                planner.mark_task_complete(request.task_id, result)
                history.add_message("assistant", result)
                
                # Save to database
                db_manager.save_execution(request.task_id, result)
            except Exception as e:
                logger.error(f"Error executing task: {e}")
        
        background_tasks.add_task(execute_background)
        
        return ExecutionResponse(
            success=True,
            result="Task queued for execution",
            execution_id=request.task_id
        )
    except Exception as e:
        logger.error(f"Error in execute_task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/plans/{plan_id}/tasks")
async def get_plan_tasks(plan_id: int):
    """Get tasks for a plan."""
    try:
        tasks = db_manager.get_plan_tasks(plan_id)
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
        
        return {"plan_id": plan_id, "tasks": tasks}
    except Exception as e:
        logger.error(f"Error retrieving tasks: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/conversation")
async def get_conversation(limit: int = 100):
    """Get conversation history."""
    try:
        messages = db_manager.get_conversation_history(limit)
        return {"messages": messages, "total": len(messages)}
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/conversation")
async def add_message(message: ConversationMessage):
    """Add a message to conversation."""
    try:
        db_manager.save_conversation(message.role, message.content)
        return {"status": "saved"}
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/scan")
async def scan_repository(repo_path: str = "."):
    """Scan a repository."""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from repo.scanner import Scanner
        scanner = Scanner(repo_path)
        info = scanner.scan_repository()
        return {"repository": repo_path, "info": info}
    except Exception as e:
        logger.error(f"Error scanning repository: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats")
async def get_statistics():
    """Get overall statistics."""
    try:
        plans = db_manager.get_all_plans(limit=1000)
        conversations = db_manager.get_conversation_history(limit=1000)
        
        total_plans = len(plans)
        completed_plans = sum(1 for p in plans if p["status"] == "completed")
        total_messages = len(conversations)
        
        return {
            "total_plans": total_plans,
            "completed_plans": completed_plans,
            "active_sessions": len(active_sessions),
            "total_messages": total_messages,
            "llm_provider": config.get("llm", {}).get("provider"),
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Phase 3: Authentication Endpoints
# ============================================================================

@app.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate and get JWT token."""
    try:
        user = verify_credentials(request.username, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = token_manager.create_access_token(user.user_id, user.username, user.roles)
        return TokenResponse(
            access_token=token,
            user_id=user.user_id,
            username=user.username
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/token", response_model=APIKeyResponse)
async def generate_api_key(token: str = Depends(get_token_from_header)):
    """Generate a new API key for the authenticated user."""
    try:
        user_data = token_manager.verify_token(token)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        api_key = api_key_manager.generate_api_key(user_data["user_id"])
        return APIKeyResponse(
            api_key=api_key,
            created_at=str(db_manager.get_timestamp()),
            expires_at=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token generation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/auth/validate")
async def validate_token(token: str = Depends(get_token_from_header)):
    """Validate a JWT token."""
    try:
        user_data = token_manager.verify_token(token)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "valid": True,
            "user_id": user_data.get("user_id"),
            "username": user_data.get("username"),
            "roles": user_data.get("roles", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================================================================
# Phase 3: WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time task updates."""
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle subscription requests
            if message.get("action") == "subscribe":
                topic = message.get("topic", "all")
                await ws_manager.subscribe(client_id, topic)
                await websocket.send_text(json.dumps({
                    "type": "subscribed",
                    "topic": topic
                }))
            
            # Handle unsubscribe requests
            elif message.get("action") == "unsubscribe":
                topic = message.get("topic", "all")
                await ws_manager.unsubscribe(client_id, topic)
                await websocket.send_text(json.dumps({
                    "type": "unsubscribed",
                    "topic": topic
                }))
    
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
        logger.info(f"WebSocket disconnected: {client_id}")


# ============================================================================
# Phase 3: Templates Endpoints
# ============================================================================

@app.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """List available templates with optional filtering."""
    try:
        if tag:
            templates = template_library.get_templates_by_tag(tag)
        elif difficulty:
            templates = template_library.get_templates_by_difficulty(difficulty)
        else:
            templates = template_library.list_templates()
        
        return [
            TemplateResponse(
                id=t.id,
                name=t.name,
                description=t.description,
                difficulty=t.difficulty,
                tags=t.tags,
                task_count=len(t.tasks)
            )
            for t in templates
        ]
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/templates/{template_id}")
async def get_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get template details."""
    try:
        template = template_library.get_template(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "difficulty": template.difficulty,
            "tags": template.tags,
            "tasks": [
                {
                    "id": t.get("id"),
                    "description": t.get("description"),
                    "priority": t.get("priority", "medium")
                }
                for t in template.tasks
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting template: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/templates/search/{query}")
async def search_templates(
    query: str,
    current_user: User = Depends(get_current_user)
):
    """Search templates by keyword."""
    try:
        templates = template_library.search_templates(query)
        return {
            "query": query,
            "results": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "difficulty": t.difficulty,
                    "tags": t.tags
                }
                for t in templates
            ]
        }
    except Exception as e:
        logger.error(f"Error searching templates: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Phase 3: Analytics Endpoints
# ============================================================================

@app.get("/analytics")
async def get_analytics(
    current_user: User = Depends(get_current_admin)
):
    """Get overall analytics."""
    try:
        stats = analytics.get_plan_analytics()
        return {
            "total_executions": sum(s.get("execution_count", 0) for s in stats.values()),
            "average_success_rate": sum(s.get("success_rate", 0) for s in stats.values()) / max(len(stats), 1),
            "tasks_analyzed": len(stats),
            "performance_report": analytics.get_performance_report()
        }
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/analytics/tasks/{task_id}")
async def get_task_analytics(
    task_id: int,
    current_user: User = Depends(get_current_admin)
):
    """Get analytics for a specific task."""
    try:
        stats = analytics.get_execution_stats(task_id)
        if not stats:
            raise HTTPException(status_code=404, detail="No analytics found for task")
        
        return {
            "task_id": task_id,
            "execution_count": stats.get("execution_count", 0),
            "success_count": stats.get("success_count", 0),
            "success_rate": stats.get("success_rate", 0),
            "avg_duration": stats.get("avg_duration", 0),
            "min_duration": stats.get("min_duration", 0),
            "max_duration": stats.get("max_duration", 0),
            "total_results_length": stats.get("total_results_length", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task analytics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/analytics/performance")
async def get_performance_metrics(
    current_user: User = Depends(get_current_admin)
):
    """Get detailed performance metrics."""
    try:
        report = analytics.get_performance_report()
        trending = analytics.get_trending_tasks(limit=10)
        
        return {
            "performance_report": report,
            "trending_tasks": trending,
            "hourly_summary": metrics_collector.get_hourly_summary(),
            "daily_summary": metrics_collector.get_daily_summary()
        }
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Update existing endpoints with authentication
# ============================================================================

@app.post("/plans", response_model=PlanResponse)
async def create_plan(
    request: PlanRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new plan from a goal."""
    try:
        planner = Planner(llm)
        tasks = planner.plan(request.goal)
        
        # Save to database
        plan_id = db_manager.save_plan(request.goal)
        
        for task in tasks:
            db_manager.save_task(plan_id, task.id, task.description, task.priority)
        
        # Store session
        global session_counter
        session_counter += 1
        active_sessions[plan_id] = {
            "planner": planner,
            "executor": Executor(llm, request.repo_path),
            "history": ConversationHistory(),
            "repo_path": request.repo_path,
            "user_id": current_user.user_id,
        }
        
        # Broadcast plan creation event (run in background to not block response)
        asyncio.create_task(EventBroadcaster.plan_updated(plan_id, "created", f"Plan created with {len(tasks)} tasks"))
        
        return PlanResponse(
            plan_id=plan_id,
            goal=request.goal,
            tasks=len(tasks),
            status="created"
        )
    except Exception as e:
        logger.error(f"Error creating plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
