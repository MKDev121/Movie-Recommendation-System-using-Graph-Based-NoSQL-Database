// Reproducible seed. It creates 126 nodes and a dense relationship network.
MATCH (n) DETACH DELETE n;
UNWIND range(1,10) AS i CREATE (:User {id:'u'+i, name:CASE i WHEN 1 THEN 'Meet Kareliya' ELSE 'Viewer '+i END, email:'viewer'+i+'@framewise.demo', joined:'2026-08-'+toString(10+i)});
UNWIND range(1,20) AS i CREATE (:Movie {id:'m'+i, title:['Past Lives','The Holdovers','Aftersun','The Worst Person in the World','Anatomy of a Fall','The Grand Budapest Hotel','Decision to Leave','Perfect Days','Spider-Man: Across the Spider-Verse','Oppenheimer','The Farewell','Arrival','Moonlight','Whiplash','Portrait of a Lady on Fire','Her','Parasite','The Handmaiden','Before Sunrise','The Secret Life of Walter Mitty'][i-1], year:2010+i, runtime:90+i});
UNWIND ['Drama','Romance','Comedy','Mystery','Adventure','Animation','History','Sci-Fi','Thriller','Fantasy','Crime','Music'] AS name CREATE (:Genre {name:name});
UNWIND range(1,40) AS i CREATE (:Actor {id:'a'+i, name:'Actor '+i});
UNWIND range(1,20) AS i CREATE (:Director {id:'d'+i, name:'Director '+i});
UNWIND range(1,24) AS i CREATE (:Review {id:'r'+i, text:'A thoughtful review for graph recommendation evaluation.', created:'2026-09-'+toString(1+(i%20))});
MATCH (m:Movie),(g:Genre) WHERE toInteger(substring(m.id,1)) % 12 = toInteger(size(g.name)) % 4 CREATE (m)-[:BELONGS_TO]->(g);
MATCH (m:Movie),(a:Actor) WHERE toInteger(substring(m.id,1)) % 8 = toInteger(substring(a.id,1)) % 8 CREATE (m)-[:ACTED_IN]->(a);
MATCH (m:Movie),(d:Director) WHERE toInteger(substring(m.id,1)) = toInteger(substring(d.id,1)) CREATE (m)-[:DIRECTED_BY]->(d);
MATCH (u:User),(m:Movie) WHERE (toInteger(substring(u.id,1))*3 + toInteger(substring(m.id,1))) % 7 IN [0,1,2] CREATE (u)-[:RATED {value:toFloat(1 + ((toInteger(substring(u.id,1))+toInteger(substring(m.id,1))) % 5)), created:'2026-09-20'}]->(m);
MATCH (u:User),(v:User) WHERE u.id < v.id AND (toInteger(substring(u.id,1))+toInteger(substring(v.id,1))) % 4 = 0 CREATE (u)-[:FOLLOWS {since:'2026-09-01'}]->(v);
MATCH (u:User),(m:Movie) WHERE (toInteger(substring(u.id,1))+toInteger(substring(m.id,1))) % 11 = 0 CREATE (u)-[:WATCHLISTED {added:'2026-09-15'}]->(m);
MATCH (m1:Movie),(m2:Movie) WHERE m1.id < m2.id AND abs(toInteger(substring(m1.id,1))-toInteger(substring(m2.id,1))) <= 2 CREATE (m1)-[:SIMILAR_TO {score:0.78}]->(m2);
MATCH (u:User)-[rating:RATED]->(m:Movie) CREATE (u)-[:WROTE]->(:Review {id:'generated-'+u.id+'-'+m.id, text:'Rating review', value:rating.value});
