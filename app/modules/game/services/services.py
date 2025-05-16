from app.modules.game.models.game import AssessmentSubmission
from app.modules.learning_path.models.learn_path import Topics, Subtopic
from app.modules.learning_path.services.learn_path_service import evaluate_answer, build_question_map
from app.utils.logger import get_logger
from collections import defaultdict
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from pathlib import Path
from enum import Enum


logger = get_logger()

def map_subtopic_to_enum(subtopic_str: str) -> Subtopic:
    """
    Map the subtopic string to the corresponding Subtopic enum.
    """
    try:
        # Convert the subtopic string to enum using .__getattr__()
        return Subtopic[subtopic_str.upper()]
    except KeyError:
        # Handle cases where subtopic string does not match enum keys
        logger.error(f"Invalid subtopic: {subtopic_str}")
        raise ValueError(f"Invalid subtopic: {subtopic_str}")


def evaluate_assessment(response):
    data_path = "app/data/initial_assessment.json"
    logger.info(f"Evaluating assessment from file path: {data_path}")

    question_map = build_question_map(data_path)
    logger.info(f"Loaded question map with {len(question_map)} questions")

    question_ids = ["safebrowsing", "passsec", "malware", "socialengineering", "incidentresponse"]
    logger.info(f"Evaluating assessment with response: {response}")

    try:
        result_dict = {}

        for item in response.responses:
            q_id = item.question_id
            subtopic_enum = item.question_subtopic
            prefix = q_id.split("-")[0]
            logger.info(f"DEBUG PREFIX: {prefix}")
            if prefix in question_ids:
                try:
                    result = evaluate_answer(item, question_map)
                    logger.info(f"RESULT: {result}")
                    result_dict[q_id] = (subtopic_enum, result)
                except ValueError:

                    result_dict[q_id] = "Invalid subtopic"
            else:
                result_dict[q_id] = "Invalid prefix"
        logger.info(f"Evaluated assessment: {result_dict}")
        return result_dict
    except Exception as e:
        logger.error(f"Assessment response evaluation error: {e}")
        return {"error": str(e)}

def evaluate_subcat_grade(assessment_result: dict) -> dict:
    subtopic_scores = defaultdict(lambda: {"correct": 0, "total": 0})
    logger.info("Evaluating subcat grade")

    logger.info(f"DEBUG: {assessment_result} ")
    for question_id, (subtopic, is_correct) in assessment_result.items():
        logger.info(f"Current: {question_id} -> {subtopic}, {is_correct}")
        subtopic_scores[subtopic]["total"] += 1
        if is_correct:
            subtopic_scores[subtopic]["correct"] += 1

    # Calculate accuracy per subtopic
    return {
        subtopic: round(scores["correct"] / scores["total"], 2)
        for subtopic, scores in subtopic_scores.items()
    }
    #example output:
    #   {
    #     "SECVSNONSEC": 0.5,        # 1 correct out of 2
    #     "HTTPVSHTTPS": 1.0,        # 2 correct out of 2
    #     "BROWSERSECBP": 0.0        # 0 correct out of 1
    # }

def mongo_serialize(obj):
    if isinstance(obj, dict):
        return {mongo_serialize(k): mongo_serialize(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [mongo_serialize(v) for v in obj]
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj  # already BSON-serializable
    else:
        return obj

async def save_assessment_result(
    db: AsyncIOMotorDatabase,
    user_id: UUID,
    topic: Topics,
    subcat_grade: dict,
    subcat_priority: list
):
    collection = db["initial_assessments"]
    document = {
        "user_id": str(user_id),
        "topic": topic,
        "subcat_scores": subcat_grade,
        "subcat_priority": subcat_priority,
        "timestamp": datetime.utcnow()
    }
    result = await collection.insert_one(mongo_serialize(document))

    return str(result.inserted_id)

