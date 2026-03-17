from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional

class ProjectPerformanceCreate(BaseModel):
    project_id: int
    employee_id: int
    task_completion: int = 0
    quality_score: int = 0
    cooperation_score: int = 0
    innovation_score: int = 0
    time_management: int = 0
    evaluator_id: Optional[int] = None
    evaluation_date: Optional[date] = None
    comments: Optional[str] = None
    
    @field_validator('task_completion', 'quality_score', 'cooperation_score', 
                     'innovation_score', 'time_management')
    def validate_score(cls, v):
        if v < 0 or v > 100:
            raise ValueError('分数必须在0-100之间')
        return v

class ProjectPerformanceResponse(BaseModel):
    id: int
    project_id: int
    employee_id: int
    task_completion: int
    quality_score: int
    cooperation_score: int
    innovation_score: int
    time_management: int
    total_score: int
    performance_level: Optional[str]
    evaluation_date: Optional[date]
    comments: Optional[str]
    
    class Config:
        from_attributes = True