"""Hybrid AI Recommendation Model.

Blends Collaborative Filtering (SVD Matrix Factorization),
Content-Based Filtering (TF-IDF Metadata Vectorization),
and Graph-Based Traversal into a unified Top-N recommendation engine.
"""

from typing import Dict, List, Any, Optional
from ai_model.data import MovieDataset
from ai_model.collaborative import CollaborativeFiltering
from ai_model.content_based import ContentBasedRecommender
from ai_model.graph_engine import GraphTraversalRecommender

class HybridRecommender:
    """Ensemble recommender providing high accuracy, cold-start resilience, and explainability."""

    def __init__(
        self,
        dataset: Optional[MovieDataset] = None,
        w_cf: float = 0.50,
        w_cb: float = 0.35,
        w_graph: float = 0.15
    ):
        self.dataset = dataset if dataset is not None else MovieDataset("expanded")
        self.w_cf = w_cf
        self.w_cb = w_cb
        self.w_graph = w_graph

        self.cf = CollaborativeFiltering(self.dataset)
        self.cb = ContentBasedRecommender(self.dataset)
        self.graph = GraphTraversalRecommender(self.dataset)

        self._initialize()

    def _initialize(self):
        self.cf.train_svd()

    def recommend(self, user_id: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Generates Top-N Hybrid recommendations with detailed breakdown."""
        user_ratings = self.dataset.get_user_ratings(user_id)
        candidate_ids = [m_id for m_id in self.dataset.movie_meta if m_id not in user_ratings]

        # Dynamic weight adjustment for cold-start users
        num_ratings = len(user_ratings)
        if num_ratings <= 2:
            cf_weight = 0.25
            cb_weight = 0.65
            graph_weight = 0.10
        else:
            cf_weight = self.w_cf
            cb_weight = self.w_cb
            graph_weight = self.w_graph

        # Retrieve intermediate scores
        # 1. Content-based similarity scores
        user_profile = self.cb.build_user_profile(user_id).reshape(1, -1)
        from sklearn.metrics.pairwise import cosine_similarity
        cb_sims = cosine_similarity(user_profile, self.cb.movie_feature_matrix)[0]

        # 2. Graph collaborative traversal results
        graph_recs = {r["movieId"]: r for r in self.graph.collaborative_graph_recommend(user_id, top_n=20)}
        social_recs = {r["movieId"]: r for r in self.graph.social_graph_recommend(user_id)}

        candidates = []
        for m_id in candidate_ids:
            meta = self.dataset.movie_meta[m_id]

            # CF SVD prediction [1.0, 5.0]
            cf_pred = self.cf.predict_svd_rating(user_id, m_id)

            # CB prediction [1.0, 5.0]
            m_soup_idx = self.cb.movie_ids.index(m_id)
            cb_sim = float(cb_sims[m_soup_idx])
            cb_pred = 3.0 + cb_sim * 2.0

            # Graph signal bonus
            graph_bonus = 3.0
            graph_item = graph_recs.get(m_id)
            social_item = social_recs.get(m_id)

            explanation_parts = []
            graph_path = None

            if graph_item:
                graph_bonus = min(5.0, 3.5 + graph_item["strength"] * 0.75)
                explanation_parts.append(f"Network peer overlap ({', '.join(graph_item['peers'])})")
                graph_path = graph_item["graphPath"]

            if social_item:
                graph_bonus = max(graph_bonus, social_item["score"])
                explanation_parts.append(f"Followed friend {social_item['friendName']} rated {social_item['score']} stars")
                if not graph_path:
                    graph_path = social_item["graphPath"]

            # Content explanation
            matched_features = self.cb.find_matched_features(user_id, m_id)
            if matched_features:
                explanation_parts.append(matched_features[0])

            # Composite hybrid score
            hybrid_score = (cf_weight * cf_pred) + (cb_weight * cb_pred) + (graph_weight * graph_bonus)
            hybrid_score = round(float(hybrid_score), 2)
            match_percentage = int(min(99, max(60, round((hybrid_score / 5.0) * 100))))

            main_explanation = " | ".join(explanation_parts) if explanation_parts else "High affinity based on overall taste profile"

            candidates.append({
                "movieId": m_id,
                "title": meta["title"],
                "releaseYear": meta["releaseYear"],
                "genres": meta["genres"],
                "director": meta["director"],
                "actors": meta["actors"],
                "plotSummary": meta.get("plotSummary", ""),
                "hybridScore": hybrid_score,
                "matchPercentage": match_percentage,
                "cfScore": round(cf_pred, 2),
                "cbScore": round(cb_pred, 2),
                "graphScore": round(graph_bonus, 2),
                "explanation": main_explanation,
                "graphPath": graph_path,
                "model": "Hybrid AI (SVD + TF-IDF + Graph)"
            })

        candidates.sort(key=lambda x: x["hybridScore"], reverse=True)
        return candidates[:top_n]
