from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modules.game.schemas.gameschemas import InitialAssessmentRequest, InitialAssessmentResponse
from app.modules.game.services.services import (
    evaluate_assessment,
    evaluate_subcat_grade,
    save_assessment_result,
)
from app.modules.learning_path.models.learn_path import Topics
from app.modules.learning_path.services.learn_path_service import evaluate_subcat_priority
from app.utils.logger import get_logger
from app.core.database_mongo import get_mongo_db
from app.core.standard_response import StandardResponse
from datetime import datetime

from uuid import UUID

router = APIRouter(prefix="/game", tags=["game"])
logger = get_logger(__name__)

@router.post("/", response_model=StandardResponse[InitialAssessmentResponse], status_code=status.HTTP_201_CREATED)
async def initial_assessment_evaluation(
    request: InitialAssessmentRequest,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    logger.info("Evaluating initial assessment")

    grade_dict = evaluate_assessment(request.assessment_response)
    logger.info(f"DEBUG: {grade_dict}")
    subcat_grade = evaluate_subcat_grade(grade_dict)
    subcat_priority = evaluate_subcat_priority(request.topic, subcat_grade)
    inserted_id = await save_assessment_result(db, request.userid, request.topic, subcat_grade, subcat_priority)

    return StandardResponse(
        success=True,
        message="Initial assessment saved successfully.",
        data=InitialAssessmentResponse(
            inserted_id=str(inserted_id),
            timestamp=datetime.utcnow(),
            userid=request.userid,
        )
    )




