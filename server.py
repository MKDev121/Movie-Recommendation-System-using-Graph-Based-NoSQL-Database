"""Local web and AI API server for Framewise.

Serves static UI files as well as REST API endpoints for:
- /api/recommendations (Hybrid AI, Collaborative SVD, Content-Based, Review 1 Graph)
- /api/benchmark (Evaluation metrics: RMSE, MAE, Precision@K, Recall@K, NDCG@K)
- /api/users (Active user profiles)
- /api/similar (Movie similarity engine)
"""

import json
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from ai_model.data import MovieDataset
from ai_model.collaborative import CollaborativeFiltering
from ai_model.content_based import ContentBasedRecommender
from ai_model.graph_engine import GraphTraversalRecommender
from ai_model.hybrid import HybridRecommender
from ai_model.evaluate import ModelEvaluator

ROOT = Path(__file__).parent

# Initialize models in memory
dataset_expanded = MovieDataset("expanded")
dataset_r1 = MovieDataset("review1")

hybrid_model = HybridRecommender(dataset_expanded)
cf_model = CollaborativeFiltering(dataset_expanded)
cf_model.train_svd()
cb_model = ContentBasedRecommender(dataset_expanded)
graph_model = GraphTraversalRecommender(dataset_expanded)

# Cache benchmark
evaluator = ModelEvaluator(dataset_expanded, k=3)
cached_benchmark = None

class FramewiseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/recommendations":
            self.handle_recommendations(params)
        elif parsed.path == "/api/benchmark":
            self.handle_benchmark()
        elif parsed.path == "/api/users":
            self.handle_users()
        elif parsed.path == "/api/similar":
            self.handle_similar(params)
        else:
            super().do_GET()

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_users(self):
        users = [
            {"userId": u["userId"], "name": u["name"], "age": u["age"], "email": u["email"]}
            for u in dataset_expanded.users_data
        ]
        self._send_json({"users": users})

    def handle_recommendations(self, params):
        user_id = params.get("userId", ["u1"])[0]
        model_type = params.get("model", ["hybrid"])[0].lower()
        top_n = int(params.get("top_n", [5])[0])

        # Validate user
        if user_id not in dataset_expanded.user_meta and user_id not in dataset_r1.user_meta:
            user_id = "u1"

        if model_type == "collaborative":
            recs = cf_model.recommend(user_id, top_n=top_n)
        elif model_type == "content":
            recs = cb_model.recommend(user_id, top_n=top_n)
        elif model_type == "graph":
            recs = graph_model.collaborative_graph_recommend(user_id, top_n=top_n)
        else:  # hybrid
            recs = hybrid_model.recommend(user_id, top_n=top_n)

        user_name = dataset_expanded.user_meta.get(user_id, {}).get("name", "Viewer")
        self._send_json({
            "userId": user_id,
            "userName": user_name,
            "model": model_type,
            "recommendations": recs
        })

    def handle_similar(self, params):
        movie_id = params.get("movieId", ["m1"])[0]
        from sklearn.metrics.pairwise import cosine_similarity
        vec = cb_model.get_movie_vector(movie_id).reshape(1, -1)
        sims = cosine_similarity(vec, cb_model.movie_feature_matrix)[0]

        results = []
        for idx, m_id in enumerate(cb_model.movie_ids):
            if m_id != movie_id:
                meta = dataset_expanded.movie_meta[m_id]
                results.append({
                    "movieId": m_id,
                    "title": meta["title"],
                    "similarity": round(float(sims[idx]), 3),
                    "genres": meta["genres"],
                    "director": meta["director"]
                })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        self._send_json({"movieId": movie_id, "similar": results[:5]})

    def handle_benchmark(self):
        global cached_benchmark
        if cached_benchmark is None:
            cached_benchmark = evaluator.evaluate_all()
        self._send_json({"benchmark": cached_benchmark})

if __name__ == '__main__':
    port = 8000
    print(f"Framewise AI Server running: http://localhost:{port}")
    ThreadingHTTPServer(('127.0.0.1', port), FramewiseHandler).serve_forever()
