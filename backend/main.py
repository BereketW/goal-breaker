from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import models, schemas, crud, database, ai_service
from database import engine
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Smart Goal Breaker API",
    description="AI-powered goal breakdown service that transforms vague goals into actionable steps",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "goals",
            "description": "Operations for managing and breaking down goals",
        }
    ],
    servers=[
        {"url": "http://localhost:8001", "description": "Development server"},
        {"url": "http://localhost:8000", "description": "Production server"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/goals/stream", tags=["goals"])
async def create_goal_stream(goal: schemas.GoalCreate, db: AsyncSession = Depends(database.get_db)):
    async def generate():
        subtasks = []
        goal_id = None
        
        try:
            async for subtask in ai_service.generate_subtasks_stream(goal.description):
                if goal_id is None:
                    db_goal = models.Goal(description=goal.description)
                    db.add(db_goal)
                    await db.flush()
                    goal_id = db_goal.id
                
                db_subtask = models.SubTask(
                    description=subtask.description,
                    complexity_score=subtask.complexity_score,
                    goal_id=goal_id
                )
                db.add(db_subtask)
                await db.flush()
                
                subtasks.append({
                    "id": db_subtask.id,
                    "description": subtask.description,
                    "complexity_score": subtask.complexity_score,
                    "goal_id": goal_id
                })
                
                yield f"data: {json.dumps(subtasks[-1])}\n\n"
            
            await db.commit()
            
            final_goal = await crud.get_goal(db, goal_id)
            yield f"data: {json.dumps({'done': True, 'goal': {'id': final_goal.id, 'description': final_goal.description, 'created_at': final_goal.created_at.isoformat(), 'subtasks': [{'id': st.id, 'description': st.description, 'complexity_score': st.complexity_score} for st in final_goal.subtasks]}})}\n\n"
            
        except Exception as e:
            await db.rollback()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post(
    "/api/goals",
    response_model=schemas.Goal,
    tags=["goals"],
    summary="Create a new goal",
    description="Break down a goal into 5 actionable subtasks with complexity scores using AI",
    responses={
        200: {
            "description": "Goal successfully created with AI-generated subtasks",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "description": "Launch a startup",
                        "created_at": "2025-11-26T00:00:00Z",
                        "subtasks": [
                            {"description": "Validate business idea", "complexity_score": 6},
                            {"description": "Create business plan", "complexity_score": 7},
                        ]
                    }
                }
            }
        },
        500: {"description": "AI generation failed or database error"}
    }
)
async def create_goal(goal: schemas.GoalCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        subtasks = await ai_service.generate_subtasks(goal.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")
    
    return await crud.create_goal(db=db, goal=goal, subtasks=subtasks)

@app.get(
    "/api/goals",
    response_model=List[schemas.Goal],
    tags=["goals"],
    summary="Get all goals",
    description="Retrieve a list of all goals with their subtasks",
    responses={
        200: {
            "description": "List of goals retrieved successfully",
        }
    }
)
async def read_goals(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db)
):
    goals = await crud.get_goals(db, skip=skip, limit=limit)
    return goals

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Goal Breaker API"}
