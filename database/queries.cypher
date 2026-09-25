// 1. Browse movies with their graph metadata
MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre) RETURN m.title, m.year, collect(g.name) AS genres ORDER BY m.year DESC;
// 2. Create a user (CREATE CRUD)
CREATE (u:User {id:$id, name:$name, email:$email, joined:date().toString()}) RETURN u;
// 3. Update a profile (UPDATE CRUD)
MATCH (u:User {id:$id}) SET u.name=$name, u.bio=$bio RETURN u;
// 4. Delete a watchlist edge (DELETE CRUD)
MATCH (u:User {id:$userId})-[w:WATCHLISTED]->(m:Movie {id:$movieId}) DELETE w;
// 5. Rate a movie with a transactional relationship write
MATCH (u:User {id:$userId}),(m:Movie {id:$movieId}) MERGE (u)-[r:RATED]->(m) SET r.value=$value, r.review=$review, r.updated=datetime() RETURN u.name,m.title,r.value;
// 6. Collaborative filtering: similar users and movies they liked
MATCH (me:User {id:$userId})-[my:RATED]->(seen:Movie)<-[their:RATED]-(peer:User)
WHERE their.value >= 4 AND my.value >= 4
MATCH (peer)-[recommendation:RATED]->(candidate:Movie)
WHERE recommendation.value >= 4 AND NOT (me)-[:RATED|WATCHLISTED]->(candidate)
RETURN candidate.title, round(avg(recommendation.value),2) AS score, count(DISTINCT peer) AS sharedTaste ORDER BY score DESC, sharedTaste DESC LIMIT $limit;
// 7. Content-based recommendation: shared genre, cast, director
MATCH (u:User {id:$userId})-[r:RATED]->(liked:Movie) WHERE r.value >= 4
MATCH (liked)-[:BELONGS_TO|ACTED_IN|DIRECTED_BY]->(feature)<-[:BELONGS_TO|ACTED_IN|DIRECTED_BY]-(candidate:Movie)
WHERE NOT (u)-[:RATED|WATCHLISTED]->(candidate)
RETURN candidate.title, count(DISTINCT feature) AS matchedFeatures ORDER BY matchedFeatures DESC LIMIT $limit;
// 8. Search across title, genre, actor and director
CALL db.index.fulltext.queryNodes('movieSearch',$term) YIELD node, score RETURN node.title, score ORDER BY score DESC;
// 9. Shortest path between a user and a movie
MATCH (u:User {id:$userId}),(m:Movie {id:$movieId}), p=shortestPath((u)-[*..6]-(m)) RETURN [n IN nodes(p)|coalesce(n.name,n.title)] AS path, length(p) AS hops;
// 10. PageRank-compatible graph analytics (requires GDS)
CALL gds.graph.project('framewise-network',['User','Movie','Genre','Actor','Director'],{RATED:{orientation:'UNDIRECTED'},BELONGS_TO:{orientation:'UNDIRECTED'},ACTED_IN:{orientation:'UNDIRECTED'},DIRECTED_BY:{orientation:'UNDIRECTED'},FOLLOWS:{orientation:'NATURAL'}});
CALL gds.pageRank.stream('framewise-network') YIELD nodeId, score RETURN gds.util.asNode(nodeId).title AS movie, score ORDER BY score DESC LIMIT 10;
// 11. Recommendation explanation: return the actual path
MATCH (u:User {id:$userId})-[:RATED]->(liked:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(candidate:Movie) WHERE candidate <> liked RETURN liked.title,g.name,candidate.title LIMIT 20;
