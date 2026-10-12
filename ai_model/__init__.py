"""Framewise AI Recommendation Model Package based on Review 1."""

from ai_model.data import MovieDataset, REVIEW1_USERS, REVIEW1_MOVIES, REVIEW1_RATINGS
from ai_model.collaborative import CollaborativeFiltering
from ai_model.content_based import ContentBasedRecommender
from ai_model.graph_engine import GraphTraversalRecommender
from ai_model.hybrid import HybridRecommender
from ai_model.evaluate import ModelEvaluator

__all__ = [
    "MovieDataset",
    "CollaborativeFiltering",
    "ContentBasedRecommender",
    "GraphTraversalRecommender",
    "HybridRecommender",
    "ModelEvaluator",
    "REVIEW1_USERS",
    "REVIEW1_MOVIES",
    "REVIEW1_RATINGS"
]
