# BCSE302P Database Systems Lab
## Project Review 2 Submission

### Movie Recommendation System Using Graph-Based NoSQL Database (Neo4j)

**Team members:** Harshit Pandey (24BCT0173), Manik Chauhan (24BCE2063), Meet Kareliya (24BCE2053)

**Review focus:** Database implementation, CRUD operations, NoSQL features, and integration

---

## 1. Review 2 Checklist

| Rubric item | Evidence in this project | Status |
|---|---|---|
| Database created | Neo4j schema and seed scripts in `database/` | Ready to demonstrate |
| Sample data loaded | 126 base nodes plus relationships and generated reviews | Ready to demonstrate |
| CRUD operations | User create/update, rating upsert, watchlist delete, movie browsing | Ready |
| Advanced NoSQL features | Multi-hop Cypher recommendations, shortest path, PageRank-compatible projection | Ready |
| Minimum 50 records/nodes | Seed creates 126 base nodes | Satisfied |
| Source code repository | Frontend, server, Cypher, report, and manual | Ready |

> **Before submission:** Run the commands in Section 3 in Neo4j Browser and replace every screenshot box with your own screenshot.

---

## 2. Project Overview

Framewise is a graph-based movie recommendation system. Neo4j stores users, movies, genres, actors, directors, reviews, ratings, follows, and watchlists as a connected graph. This allows recommendation queries to traverse relationships directly instead of performing multiple relational joins.

### Graph labels

`User`, `Movie`, `Genre`, `Actor`, `Director`, `Review`

### Relationship types

`RATED`, `BELONGS_TO`, `ACTED_IN`, `DIRECTED_BY`, `FOLLOWS`, `WATCHLISTED`, `SIMILAR_TO`, `WROTE`

### Files used in the demonstration

- `database/schema.cypher`: constraints and indexes
- `database/seed.cypher`: sample graph data
- `database/queries.cypher`: CRUD, recommendation, search, and analytics queries
- `index.html`, `styles.css`, `app.js`: responsive user interface
- `server.py`: local demo server

---

## 3. Neo4j Demonstration and Screenshot Guide

Open Neo4j Browser and connect to the local Neo4j database or Neo4j Aura instance. Run `database/schema.cypher` first, followed by `database/seed.cypher`.

### Screenshot 1: Constraints and indexes

**What to show:** Neo4j Browser output showing the constraints and indexes created by `schema.cypher`.

**Run this command:**

```cypher
SHOW CONSTRAINTS;
SHOW INDEXES;
```

**Expected output:** Unique constraints for user, movie, genre, actor, director, and review IDs; indexes for movie title, movie year, and user email.

**Paste screenshot here:**

> [SCREENSHOT 1: Constraints and indexes]
>
> Leave approximately 10 cm of space here. Capture Neo4j Browser showing the result table.

---

### Screenshot 2: Database population and node counts

**What to show:** Counts proving that the database contains more than the required 50 nodes.

**Run this command:**

```cypher
MATCH (n)
RETURN labels(n)[0] AS label, count(n) AS total
ORDER BY label;
```

**Expected output:** At least 10 users, 20 movies, 12 genres, 40 actors, 20 directors, and 24 reviews, for 126 base nodes before any generated review nodes.

**Paste screenshot here:**

> [SCREENSHOT 2: Node count by label]
>
> Leave approximately 10 cm of space here. Capture the result table with all labels visible.

---

### Screenshot 3: Graph visualization

**What to show:** A visual graph containing users, movies, genres, actors, and directors.

**Run this command:**

```cypher
MATCH p=(u:User)-[:RATED]->(m:Movie)-[:BELONGS_TO]->(g:Genre)
RETURN p
LIMIT 40;
```

**Expected output:** Neo4j Browser graph view with connected user-rating-movie-genre paths.

**Paste screenshot here:**

> [SCREENSHOT 3: Neo4j graph visualization]
>
> Leave approximately 12 cm of space here. Switch Neo4j Browser from table view to graph view before capturing.

---

### Screenshot 4: Create and read a user

**What to show:** A CRUD create operation and the created user returned by Neo4j.

**Run this command:**

```cypher
CREATE (u:User {
  id: 'demo-user',
  name: 'Review 2 Demo User',
  email: 'review2@framewise.demo',
  joined: date().toString()
})
RETURN u;
```

Then verify the record:

```cypher
MATCH (u:User {id: 'demo-user'})
RETURN u;
```

**Expected output:** A user node with the requested properties.

**Paste screenshot here:**

> [SCREENSHOT 4: User create and read]
>
> Leave approximately 10 cm of space here. Capture the returned node properties.

---

### Screenshot 5: Update and delete operations

**What to show:** Updating a profile and deleting a watchlist relationship.

**Run this command:**

```cypher
MATCH (u:User {id: 'demo-user'})
SET u.bio = 'Graph recommendation evaluator'
RETURN u;
```

For a relationship delete demonstration:

```cypher
MATCH (u:User {id: 'u1'}), (m:Movie {id: 'm1'})
MERGE (u)-[:WATCHLISTED {added: '2026-09-25'}]->(m);

MATCH (u:User {id: 'u1'})-[w:WATCHLISTED]->(m:Movie {id: 'm1'})
DELETE w
RETURN u.id AS user, m.title AS movie, 'watchlist edge deleted' AS result;
```

**Expected output:** Updated user properties and a confirmation row for the deleted relationship.

**Paste screenshot here:**

> [SCREENSHOT 5: Update and delete CRUD]
>
> Leave approximately 10 cm of space here. Capture the final result row.

---

### Screenshot 6: Rating write with relationship properties

**What to show:** A rating stored as a relationship with value, review text, and timestamp.

**Run this command:**

```cypher
MATCH (u:User {id: 'u1'}), (m:Movie {id: 'm10'})
MERGE (u)-[r:RATED]->(m)
SET r.value = 5,
    r.review = 'Powerful and technically precise.',
    r.updated = datetime()
RETURN u.name, m.title, r.value, r.review, r.updated;
```

**Expected output:** One row showing the user, movie, rating value, review, and update timestamp.

**Paste screenshot here:**

> [SCREENSHOT 6: Rating relationship write]
>
> Leave approximately 10 cm of space here. Capture the returned relationship properties.

---

### Screenshot 7: Collaborative recommendation

**What to show:** Recommendations generated by users with similar rating patterns.

**Run this command:**

```cypher
MATCH (me:User {id:'u1'})-[my:RATED]->(seen:Movie)<-[their:RATED]-(peer:User)
WHERE their.value >= 4 AND my.value >= 4
MATCH (peer)-[recommendation:RATED]->(candidate:Movie)
WHERE recommendation.value >= 4
  AND NOT (me)-[:RATED|WATCHLISTED]->(candidate)
RETURN candidate.title,
       round(avg(recommendation.value), 2) AS score,
       count(DISTINCT peer) AS sharedTaste
ORDER BY score DESC, sharedTaste DESC
LIMIT 5;
```

**Expected output:** A ranked list of unseen movies with a score and the number of users sharing the taste pattern.

**Paste screenshot here:**

> [SCREENSHOT 7: Collaborative recommendation result]
>
> Leave approximately 10 cm of space here. Capture the ranked result table.

---

### Screenshot 8: Content-based recommendation

**What to show:** Recommendations based on shared genres, actors, or directors.

**Run this command:**

```cypher
MATCH (u:User {id:'u1'})-[r:RATED]->(liked:Movie)
WHERE r.value >= 4
MATCH (liked)-[:BELONGS_TO|ACTED_IN|DIRECTED_BY]->(feature)
      <-[:BELONGS_TO|ACTED_IN|DIRECTED_BY]-(candidate:Movie)
WHERE NOT (u)-[:RATED|WATCHLISTED]->(candidate)
RETURN candidate.title,
       count(DISTINCT feature) AS matchedFeatures
ORDER BY matchedFeatures DESC
LIMIT 5;
```

**Expected output:** Movies ranked by the number of graph features shared with movies the user rated highly.

**Paste screenshot here:**

> [SCREENSHOT 8: Content-based recommendation result]
>
> Leave approximately 10 cm of space here. Capture the result table and query text.

---

### Screenshot 9: Shortest-path analytics

**What to show:** The relationship path explaining how a user connects to a movie.

**Run this command:**

```cypher
MATCH (u:User {id:'u1'}), (m:Movie {id:'m10'}),
      p=shortestPath((u)-[*..6]-(m))
RETURN [n IN nodes(p) | coalesce(n.name, n.title)] AS path,
       length(p) AS hops;
```

**Expected output:** A path array and hop count. This demonstrates graph traversal analytics.

**Paste screenshot here:**

> [SCREENSHOT 9: Shortest path]
>
> Leave approximately 10 cm of space here. Capture the path and hop count.

---

### Screenshot 10: Application integration

**What to show:** Framewise frontend running locally with recommendations and movie posters.

**Run this command in the project folder:**

```bash
python3 server.py
```

Open `http://localhost:8000` in a browser. Show the home screen, then click a movie to show the detail modal and rating buttons.

**Expected output:** Responsive dark streaming-style interface with search, recommendation modes, real poster artwork, rating flow, library, and graph explorer.

**Paste screenshot here:**

> [SCREENSHOT 10: Framewise application]
>
> Leave approximately 15 cm of space here. Capture the home screen or movie detail modal.

---

## 4. Advanced NoSQL Features Demonstrated

1. **Native graph traversal:** Recommendations use 2–3 hop traversals through users, ratings, movies, genres, actors, and directors.
2. **Relationship properties:** `RATED` stores the rating value, review, and update timestamp.
3. **Constraints and indexes:** Identity constraints and lookup indexes support data integrity and performance.
4. **Shortest path:** Explains the connection between a user and a target movie.
5. **PageRank compatibility:** The query file includes a Neo4j Graph Data Science projection and PageRank query.
6. **Schema flexibility:** New labels such as `Language`, `Award`, or `Platform` can be added without redesigning relational tables.

---

## 5. Review 2 Viva Preparation

**Why did you choose Neo4j?**

The core problem is relationship-heavy. Neo4j stores relationships as first-class graph edges and makes multi-hop recommendation queries readable and efficient.

**How does collaborative filtering work?**

The query finds users who rated the same movies highly as the current user, then collects other movies those similar users rated highly. Already rated or watchlisted movies are excluded.

**How does content-based filtering work?**

It follows relationships from highly rated movies to genres, actors, and directors, then finds candidate movies sharing those features.

**What is stored on the `RATED` relationship?**

The rating value, optional review, and update timestamp are stored as relationship properties because they describe the user-to-movie interaction.

**How is the database protected from duplicate entities?**

Neo4j uniqueness constraints are created for user, movie, genre, actor, director, and review identifiers.

**How does the system scale?**

The graph schema supports additional users, movies, and relationship types without changing a fixed set of relational tables. Indexes improve common identity and search lookups.

---

## 6. Submission Notes

- Add your screenshots in the ten marked sections.
- Keep the Neo4j query text visible where possible.
- Make sure the Neo4j Browser database name and team member details are visible in at least one screenshot if required by your instructor.
- Remove any test node named `demo-user` after the demonstration if your instructor expects a clean database:

```cypher
MATCH (u:User {id:'demo-user'}) DETACH DELETE u;
```

**End of Review 2 submission document**
