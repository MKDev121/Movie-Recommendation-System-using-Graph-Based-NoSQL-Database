# AI Movie Recommendation System — Technical Documentation
## BCSE302P Database Systems Lab | Review 1 Implementation & AI Extension

**Project Title:** Movie Recommendation System using Graph-Based NoSQL Database (Neo4j)  
**Team Members:**
- **Harshit Pandey** (24BCT0173)
- **Manik Chauhan** (24BCE2063)
- **Meet Kareliya** (24BCE2053)

---

## 1. Overview & Review 1 Alignment

In **Review 1**, the project established the problem statement, database schema, functional requirements, and sample Cypher queries:
- **FR-4 Collaborative Recommendation:** Recommend movies liked by peers with similar rating patterns.
- **FR-5 Content-Based Recommendation:** Recommend movies sharing genres, actors, or directors with movies the user rated highly.
- **FR-7 Social Graph:** Leverage the user-to-user `FOLLOWS` social network.
- **FR-8 Top-N Recommendations:** Generate ranked lists of Top-$N$ movies per user on demand.
- **Future Extension Noted in Review 1:** Machine learning and AI-powered recommendation algorithms.

We have implemented a complete AI Recommendation Engine (`ai_model/`) that integrates seamlessly with both the Review 1 dataset (Aditi Sharma, Rahul Verma, Sneha Iyer, Karthik Raja) and the full interactive catalog.

---

## 2. Recommendation Model Architectures

### 2.1 Collaborative Filtering: SVD Matrix Factorization
- **File:** [`ai_model/collaborative.py`](file:///c:/Users/harsh/OneDrive/Desktop/MovieR/ai_model/collaborative.py)
- **Theory:** Decomposes the sparse User-Item rating matrix $\mathbf{R} \in \mathbb{R}^{|U| \times |M|}$ into lower-dimensional user latent embeddings $\mathbf{P} \in \mathbb{R}^{|U| \times k}$ and movie latent embeddings $\mathbf{Q} \in \mathbb{R}^{|M| \times k}$ ($k=8$ latent dimensions).
- **Rating Prediction Formula:**
  $$\hat{r}_{u, i} = \mu + b_u + b_i + \mathbf{P}_u \cdot \mathbf{Q}_i^T$$
  where $\mu$ is the global rating mean, $b_u$ is user rating bias, and $b_i$ is movie item bias.
- **Optimization:** Stochastic Gradient Descent (SGD) minimizing regularized mean squared error:
  $$\mathcal{L} = \sum_{(u,i) \in \mathcal{K}} (r_{u,i} - \hat{r}_{u,i})^2 + \lambda (\|\mathbf{P}_u\|^2 + \|\mathbf{Q}_i\|^2 + b_u^2 + b_i^2)$$
- **Explainability:** Identifies peers with highest cosine similarity in the rating space who rated the recommended movie $\ge 4$ stars.

---

### 2.2 Content-Based Filtering: TF-IDF & Metadata Cosine Similarity
- **File:** [`ai_model/content_based.py`](file:///c:/Users/harsh/OneDrive/Desktop/MovieR/ai_model/content_based.py)
- **Theory:** Fulfills Review 1 FR-5 by vectorizing rich movie metadata (repeated genres for weighting, director identity, cast, and plot summary keywords).
- **User Profile Construction:**
  $$\mathbf{u} = \frac{1}{\sum w_m} \sum_{m \in \text{Rated}(u)} (r_{u,m} - 2.5) \cdot \mathbf{v}_m$$
  Positive ratings ($\ge 3$) pull the user taste vector towards those genres and creators.
- **Scoring:** Cosine similarity between normalized user profile $\mathbf{u}$ and candidate movie vectors $\mathbf{v}_m$:
  $$\text{Sim}(\mathbf{u}, \mathbf{v}_m) = \frac{\mathbf{u} \cdot \mathbf{v}_m}{\|\mathbf{u}\| \|\mathbf{v}_m\|}$$
- **Cold-Start Resilience:** Functions immediately even when new movies have zero historical ratings.

---

### 2.3 Graph-Based Traversal Engine
- **File:** [`ai_model/graph_engine.py`](file:///c:/Users/harsh/OneDrive/Desktop/MovieR/ai_model/graph_engine.py)
- **Exact Mirror of Review 1 Section 5.5 Cypher Query:**
  ```cypher
  MATCH (target:User {userId:$userId})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
  MATCH (other)-[r:RATED]->(rec:Movie)
  WHERE NOT (target)-[:RATED]->(rec) AND r.score >= 4
  RETURN rec.title AS recommendation, COUNT(*) AS strength
  ORDER BY strength DESC
  LIMIT 5;
  ```
- **Social Graph Filtering (FR-7):**
  Traverses `(:User)-[:FOLLOWS]->(:User)-[:RATED]->(:Movie)` paths.
- **Explainability:** Generates full multi-hop traversal paths, e.g.:
  `(:User {name: 'Aditi Sharma'}) -[:RATED]-> (:Movie {title: 'Inception'}) <-[:RATED]- (:User {name: 'Rahul Verma'}) -[:RATED]-> (:Movie {title: 'The Dark Knight'})`

---

### 2.4 Hybrid AI Ensemble Model
- **File:** [`ai_model/hybrid.py`](file:///c:/Users/harsh/OneDrive/Desktop/MovieR/ai_model/hybrid.py)
- **Ensemble Formulation:**
  $$\text{Score}_{\text{Hybrid}}(u, m) = w_{cf} \cdot \hat{r}_{cf}(u, m) + w_{cb} \cdot \hat{r}_{cb}(u, m) + w_{graph} \cdot \text{Signal}_{graph}(u, m)$$
- **Dynamic Weight Shifting:**
  - For active users ($>2$ ratings): $w_{cf} = 0.50, w_{cb} = 0.35, w_{graph} = 0.15$.
  - For cold-start users ($\le 2$ ratings): $w_{cb} = 0.65, w_{cf} = 0.25, w_{graph} = 0.10$.
- **Outputs:**
  - Ranked recommendations
  - Predicted score (out of 5.0) and taste match percentage (e.g. 96% Match)
  - Composite explanation breakdown

---

## 3. Evaluation & Benchmark Results

The models were evaluated via leave-one-out cross-validation using [`ai_model/evaluate.py`](file:///c:/Users/harsh/OneDrive/Desktop/MovieR/ai_model/evaluate.py):

| Model Architecture | RMSE (lower) | MAE (lower) | Precision@3 (higher) | Recall@3 (higher) | NDCG@3 (higher) | Catalog Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Collaborative Filtering (SVD)** | 0.549 | 0.488 | 0.100 | 0.300 | 0.200 | 25.0% |
| **Content-Based (TF-IDF)** | 0.946 | 0.896 | 0.200 | 0.600 | 0.513 | 65.0% |
| **Review 1 Graph Traversal** | 0.634 | 0.560 | 0.067 | 0.200 | 0.150 | 80.0% |
| **Hybrid AI Ensemble (Proposed)** | **0.403 (Best)** | **0.277 (Best)** | **0.167** | **0.500** | **0.500** | **65.0%** |

### Key Observations:
1. **Hybrid AI achieves the lowest error:** RMSE drops to **0.403** and MAE to **0.277**, significantly outperforming individual models.
2. **High Explainability & Coverage:** The graph and content models boost catalog discovery to **65–80%**, avoiding the popularity bias typical of pure collaborative filtering.

---

## 4. Running the System

### 4.1 CLI Demonstration & Review 1 Verification
To test the Review 1 sample dataset (Aditi Sharma, Rahul Verma, etc.), the AI hybrid predictions, and print the evaluation benchmark:
```bash
python ai_model/train_and_demo.py
```

### 4.2 Web UI & REST API Server
Start the backend server:
```bash
python server.py
```
Then open [http://localhost:8000](http://localhost:8000) in your web browser.

### 4.3 REST API Endpoints:
- `GET /api/recommendations?userId=u1&model=hybrid&top_n=5`
- `GET /api/benchmark`
- `GET /api/users`
- `GET /api/similar?movieId=m1`
