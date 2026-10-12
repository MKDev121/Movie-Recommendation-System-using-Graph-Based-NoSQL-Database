"""Evaluation suite for Recommendation Models.

Calculates:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Precision@K
- Recall@K
- NDCG@K
- Catalog Coverage (%)
Across Collaborative (SVD), Content-Based (TF-IDF), Graph Traversal, and Hybrid AI models.
"""

import numpy as np
from typing import Dict, List, Any
from ai_model.data import MovieDataset
from ai_model.collaborative import CollaborativeFiltering
from ai_model.content_based import ContentBasedRecommender
from ai_model.graph_engine import GraphTraversalRecommender
from ai_model.hybrid import HybridRecommender

class ModelEvaluator:
    """Evaluates recommender algorithms using leave-one-out cross validation and ranking metrics."""

    def __init__(self, dataset: MovieDataset, k: int = 3):
        self.dataset = dataset
        self.k = k

    def evaluate_all(self) -> Dict[str, Dict[str, float]]:
        """Runs evaluation over all models and returns metrics table."""
        ratings = self.dataset.ratings_df.copy()

        # Split: Leave-one-out for users with at least 3 ratings
        train_ratings = []
        test_ratings = []

        np.random.seed(42)
        for user_id, group in ratings.groupby("userId"):
            items = group.to_dict("records")
            if len(items) >= 2:
                # Pick one random test item
                test_idx = np.random.randint(0, len(items))
                test_ratings.append(items[test_idx])
                for idx, it in enumerate(items):
                    if idx != test_idx:
                        train_ratings.append(it)
            else:
                train_ratings.extend(items)

        # Build train dataset
        import pandas as pd
        train_dataset = MovieDataset("expanded")
        train_dataset.ratings_df = pd.DataFrame(train_ratings)

        # Initialize models
        cf = CollaborativeFiltering(train_dataset)
        cf.train_svd()

        cb = ContentBasedRecommender(train_dataset)
        graph = GraphTraversalRecommender(train_dataset)
        hybrid = HybridRecommender(train_dataset)

        results = {
            "Collaborative (SVD)": self._eval_model(cf, test_ratings, "cf"),
            "Content-Based (TF-IDF)": self._eval_model(cb, test_ratings, "cb"),
            "Graph Traversal (Cypher)": self._eval_model(graph, test_ratings, "graph"),
            "Hybrid AI Model": self._eval_model(hybrid, test_ratings, "hybrid")
        }

        return results

    def _eval_model(self, model: Any, test_set: List[Dict[str, Any]], model_type: str) -> Dict[str, float]:
        errors = []
        abs_errors = []
        hits = 0
        total_relevant = 0
        ndcg_scores = []
        recommended_catalog = set()

        all_catalog = set(self.dataset.movie_meta.keys())

        for test_item in test_set:
            user_id = test_item["userId"]
            movie_id = test_item["movieId"]
            actual_rating = float(test_item["score"])
            is_relevant = actual_rating >= 4.0

            if is_relevant:
                total_relevant += 1

            # Get Top-K recommendations
            recs = []
            if model_type == "cf":
                recs = model.recommend(user_id, top_n=self.k)
                pred_rating = model.predict_svd_rating(user_id, movie_id)
            elif model_type == "cb":
                recs = model.recommend(user_id, top_n=self.k)
                pred_rating = 3.5  # default baseline
                for r in recs:
                    if r["movieId"] == movie_id:
                        pred_rating = r["predictedRating"]
            elif model_type == "graph":
                recs = model.collaborative_graph_recommend(user_id, top_n=self.k)
                pred_rating = 3.8
                for r in recs:
                    if r["movieId"] == movie_id:
                        pred_rating = r["predictedRating"]
            else:  # hybrid
                recs = model.recommend(user_id, top_n=self.k)
                pred_rating = 4.0
                for r in recs:
                    if r["movieId"] == movie_id:
                        pred_rating = r["hybridScore"]

            err = actual_rating - pred_rating
            errors.append(err ** 2)
            abs_errors.append(abs(err))

            # Check if test item is in Top-K
            rec_ids = [r["movieId"] for r in recs]
            recommended_catalog.update(rec_ids)

            if movie_id in rec_ids and is_relevant:
                hits += 1
                rank = rec_ids.index(movie_id) + 1
                ndcg = 1.0 / np.log2(rank + 1)
                ndcg_scores.append(ndcg)
            else:
                ndcg_scores.append(0.0)

        rmse = float(np.sqrt(np.mean(errors))) if errors else 0.0
        mae = float(np.mean(abs_errors)) if abs_errors else 0.0
        precision_at_k = float(hits / (len(test_set) * self.k)) if test_set else 0.0
        recall_at_k = float(hits / max(1, total_relevant))
        mean_ndcg = float(np.mean(ndcg_scores)) if ndcg_scores else 0.0
        coverage = float(len(recommended_catalog) / max(1, len(all_catalog)) * 100)

        return {
            "RMSE": round(rmse, 3),
            "MAE": round(mae, 3),
            f"Precision@{self.k}": round(precision_at_k, 3),
            f"Recall@{self.k}": round(recall_at_k, 3),
            f"NDCG@{self.k}": round(mean_ndcg, 3),
            "Catalog Coverage (%)": round(coverage, 1)
        }

    def print_benchmark_table(self):
        """Prints a benchmark comparison table formatted for project evaluation."""
        results = self.evaluate_all()
        headers = ["Model", "RMSE (lower)", "MAE (lower)", f"Precision@{self.k} (higher)", f"Recall@{self.k} (higher)", f"NDCG@{self.k} (higher)", "Coverage %"]
        
        row_format = "{:<26} | {:<12} | {:<11} | {:<18} | {:<18} | {:<17} | {:<10}"
        separator = "-" * 122

        print("\n" + "=" * 122)
        print("          FRAMEWISE AI RECOMMENDATION SYSTEM -- MODEL BENCHMARK RESULTS")
        print("=" * 122)
        print(row_format.format(*headers))
        print(separator)

        for model_name, metrics in results.items():
            vals = [
                model_name,
                f"{metrics['RMSE']:.3f}",
                f"{metrics['MAE']:.3f}",
                f"{metrics[f'Precision@{self.k}']:.3f}",
                f"{metrics[f'Recall@{self.k}']:.3f}",
                f"{metrics[f'NDCG@{self.k}']:.3f}",
                f"{metrics['Catalog Coverage (%)']:.1f}%"
            ]
            print(row_format.format(*vals))
        print("=" * 98 + "\n")
        return results

if __name__ == "__main__":
    dataset = MovieDataset("expanded")
    evaluator = ModelEvaluator(dataset, k=3)
    evaluator.print_benchmark_table()
