"""Demonstration script showcasing the AI recommendation models against Review 1 specifications.

Executes:
1. Review 1 Section 5.5 Benchmark (Aditi Sharma U1 & Rahul Verma U2 with Inception, Interstellar, The Dark Knight)
2. Latent Factor SVD Matrix Factorization
3. TF-IDF Content-Based Filtering
4. Graph Traversal Path Explanations
5. Hybrid AI Top-N Recommendation
6. Full Model Evaluation Benchmark Table
"""

import sys
from pathlib import Path

# Ensure root dir is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Ensure UTF-8 stdout on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from ai_model.data import MovieDataset
from ai_model.collaborative import CollaborativeFiltering
from ai_model.content_based import ContentBasedRecommender
from ai_model.graph_engine import GraphTraversalRecommender
from ai_model.hybrid import HybridRecommender
from ai_model.evaluate import ModelEvaluator

def run_review1_exact_demo():
    print("=" * 80)
    print(" [REVIEW 1] EXACT SPECIFICATION DEMO (Table 5.1 - 5.5)")
    print("=" * 80)
    ds_r1 = MovieDataset("review1")

    print("\n[1] Review 1 Users:")
    for u in ds_r1.users_data:
        print(f"  - {u['userId']}: {u['name']} (Age: {u['age']}, Joined: {u['joinDate']})")

    print("\n[2] Review 1 Movies:")
    for m in ds_r1.movies_data:
        print(f"  - {m['movieId']}: {m['title']} ({m['releaseYear']}) - Genres: {', '.join(m['genres'])} - Dir: {m['director']}")

    print("\n[3] Review 1 Ratings History:")
    for r in ds_r1.ratings_data:
        u_name = ds_r1.user_meta[r['userId']]['name']
        m_title = ds_r1.movie_meta[r['movieId']]['title']
        print(f"  - {u_name} rated '{m_title}' -> {r['score']} stars")

    print("\n[4] Section 5.5 Cypher Equivalent Traversal for Target User: U1 (Aditi Sharma)")
    graph_r1 = GraphTraversalRecommender(ds_r1)
    recs = graph_r1.collaborative_graph_recommend("U1", min_score=4.0)

    if recs:
        for i, rec in enumerate(recs, 1):
            print(f"  #{i} Recommendation: {rec['title']}")
            print(f"     Strength: {rec['strength']} shared-taste peer(s)")
            print(f"     Graph Path: {rec['graphPath']}")
    else:
        print("  No 2-hop ratings meeting criteria.")

    print("\n[5] Content-Based Recommendation for U1 (Aditi Sharma) using TF-IDF:")
    cb_r1 = ContentBasedRecommender(ds_r1)
    cb_recs = cb_r1.recommend("U1", top_n=2)
    for i, rec in enumerate(cb_recs, 1):
        print(f"  #{i} Movie: {rec['title']} (Similarity: {rec['similarityScore']:.3f}, Pred: {rec['predictedRating']} stars)")
        print(f"     Explanation: {rec['explanation']}")

def run_expanded_ai_demo():
    print("\n" + "=" * 80)
    print(" [AI HYBRID] MULTI-CRITERIA RECOMMENDATION ENGINE")
    print("=" * 80)

    dataset = MovieDataset("expanded")
    hybrid = HybridRecommender(dataset)

    test_user_id = "u1"  # Meet Kareliya
    user_name = dataset.user_meta[test_user_id]["name"]
    print(f"\nUser: {user_name} ({test_user_id})")
    print("Current Ratings:")
    for m_id, score in dataset.get_user_ratings(test_user_id).items():
        print(f"  [{score} stars] -> {dataset.movie_meta[m_id]['title']} ({dataset.movie_meta[m_id]['director']})")

    print(f"\nGenerating Top-5 Hybrid AI Recommendations for {user_name}...")
    recs = hybrid.recommend(test_user_id, top_n=5)

    for i, r in enumerate(recs, 1):
        print(f"\n  #{i} {r['title']} ({r['releaseYear']}) -- {r['matchPercentage']}% Match (Score: {r['hybridScore']}/5.0)")
        print(f"     Genres: {', '.join(r['genres'])} | Director: {r['director']}")
        print(f"     Component Breakdown: CF(SVD)={r['cfScore']} | CB(TF-IDF)={r['cbScore']} | Graph={r['graphScore']}")
        print(f"     Reason: {r['explanation']}")
        if r.get('graphPath'):
            print(f"     Graph Traversal Path: {r['graphPath']}")

def run_evaluation_benchmark():
    dataset = MovieDataset("expanded")
    evaluator = ModelEvaluator(dataset, k=3)
    evaluator.print_benchmark_table()

if __name__ == "__main__":
    run_review1_exact_demo()
    run_expanded_ai_demo()
    run_evaluation_benchmark()
