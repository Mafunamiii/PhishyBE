# takes in the topic value, the grades in a list format
from ..models.learn_path import Topics, SubtopicPriority

def score_to_priority(score: float) -> SubtopicPriority:
    if 0 <= score <= 0.45:
        return SubtopicPriority.HIGH
    elif 0.46 <= score <= 0.85:
        return SubtopicPriority.MODERATE
    else:
        return SubtopicPriority.LOW

def evaluate_subcategory(topic: Topics, subcat_results: dict):

    subcat_priorities = {}
    for subcat, score in subcat_results.items():
        subcat_priorities[subcat] = score_to_priority(score)

    return topic, subcat_priorities


