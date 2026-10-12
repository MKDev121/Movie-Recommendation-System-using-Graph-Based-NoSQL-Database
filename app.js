// Poster URLs for full catalog
const posterUrls = {
  m1: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m2: 'https://image.tmdb.org/t/p/w500/VHSzNBTwxV8vh7wylo7O9CLdac.jpg',
  m3: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  m4: 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
  m5: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m6: 'https://image.tmdb.org/t/p/w500/VHSzNBTwxV8vh7wylo7O9CLdac.jpg',
  m7: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  m8: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m9: 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
  m10: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  m11: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m12: 'https://image.tmdb.org/t/p/w500/VHSzNBTwxV8vh7wylo7O9CLdac.jpg',
  m13: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  m14: 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
  m15: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m16: 'https://image.tmdb.org/t/p/w500/VHSzNBTwxV8vh7wylo7O9CLdac.jpg',
  m17: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  m18: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  m19: 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
  m20: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg'
};

const movies = [
  {id:'m1',title:'Past Lives',year:2023,genres:['Romance','Drama'],director:'Celine Song',actors:['Greta Lee','Teo Yoo'],rating:4.8,poster:'poster-a',reason:'Because you love intimate stories',plot:'Two childhood friends reunite in New York for one fateful week, asking what might have been.'},
  {id:'m2',title:'The Holdovers',year:2023,genres:['Comedy','Drama'],director:'Alexander Payne',actors:['Paul Giamatti','Da’Vine Joy Randolph'],rating:4.7,poster:'poster-b',reason:'Shared emotional DNA',plot:'A cranky teacher, a grieving cook, and a stranded student find an unlikely family over winter break.'},
  {id:'m3',title:'Aftersun',year:2022,genres:['Drama'],director:'Charlotte Wells',actors:['Paul Mescal','Frankie Corio'],rating:4.6,poster:'poster-c',reason:'Your quiet-beautiful signal',plot:'A daughter looks back on a holiday with her young father and the memories that linger.'},
  {id:'m4',title:'The Worst Person in the World',year:2021,genres:['Romance','Comedy'],director:'Joachim Trier',actors:['Renate Reinsve','Anders Danielsen Lie'],rating:4.5,poster:'poster-d',reason:'A little messy, very human',plot:'Four years in the life of a young woman navigating the troubled waters of her love life.'},
  {id:'m5',title:'Anatomy of a Fall',year:2023,genres:['Drama','Mystery'],director:'Justine Triet',actors:['Sandra Hüller','Swann Arlaud'],rating:4.6,poster:'poster-e',reason:'For your curious side',plot:'A woman is suspected of her husband’s murder, and their blind son faces a moral dilemma.'},
  {id:'m6',title:'The Grand Budapest Hotel',year:2014,genres:['Comedy','Adventure'],director:'Wes Anderson',actors:['Ralph Fiennes','Tony Revolori'],rating:4.4,poster:'poster-f',reason:'Your visual storytelling branch',plot:'A legendary concierge and his lobby boy become ensnared in a theft and a family fortune.'},
  {id:'m7',title:'Decision to Leave',year:2022,genres:['Mystery','Romance'],director:'Park Chan-wook',actors:['Park Hae-il','Tang Wei'],rating:4.4,poster:'poster-a',reason:'Because you liked mysteries',plot:'A detective investigating a man’s death falls for the dead man’s mysterious wife.'},
  {id:'m8',title:'Perfect Days',year:2023,genres:['Drama'],director:'Wim Wenders',actors:['Koji Yakusho','Yumi Aso'],rating:4.5,poster:'poster-b',reason:'A slow-burn discovery',plot:'A Tokyo toilet cleaner finds beauty in the small rituals of his carefully structured days.'},
  {id:'m9',title:'Spider-Man: Across the Spider-Verse',year:2023,genres:['Animation','Adventure'],director:'Joaquim Dos Santos',actors:['Shameik Moore','Hailee Steinfeld'],rating:4.7,poster:'poster-c',reason:'Popular in your network',plot:'Miles Morales catapults across the Multiverse and encounters a team charged with protecting its existence.'},
  {id:'m10',title:'Oppenheimer',year:2023,genres:['Drama','History'],director:'Christopher Nolan',actors:['Cillian Murphy','Emily Blunt'],rating:4.5,poster:'poster-d',reason:'Trending near you',plot:'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.'},
  {id:'m11',title:'The Farewell',year:2019,genres:['Comedy','Drama'],director:'Lulu Wang',actors:['Awkwafina','Tzi Ma'],rating:4.3,poster:'poster-e',reason:'Family-centered storytelling',plot:'A Chinese-American family discovers their grandmother has only a short time left to live and schedule an impromptu wedding.'},
  {id:'m12',title:'Arrival',year:2016,genres:['Sci-Fi','Drama'],director:'Denis Villeneuve',actors:['Amy Adams','Jeremy Renner'],rating:4.7,poster:'poster-f',reason:'Deep sci-fi exploration',plot:'A linguist works with the military to communicate with alien lifeforms after mysterious spacecraft appear.'},
  {id:'m13',title:'Moonlight',year:2016,genres:['Drama'],director:'Barry Jenkins',actors:['Mahershala Ali','Naomie Harris'],rating:4.6,poster:'poster-a',reason:'Lyrical cinematography',plot:'A young man grapples with his identity and sexuality while experiencing the everyday struggles of life.'},
  {id:'m14',title:'Whiplash',year:2014,genres:['Drama','Music'],director:'Damien Chazelle',actors:['Miles Teller','J.K. Simmons'],rating:4.8,poster:'poster-b',reason:'High intensity perfection',plot:'A promising young drummer enrolls at a cut-throat conservatory mentored by an uncompromising instructor.'},
  {id:'m15',title:'Portrait of a Lady on Fire',year:2019,genres:['Drama','Romance'],director:'Céline Sciamma',actors:['Noémie Merlant','Adèle Haenel'],rating:4.7,poster:'poster-c',reason:'Subtle emotional resonance',plot:'On an isolated island in Brittany, a female painter is obliged to secretly paint a wedding portrait.'},
  {id:'m16',title:'Her',year:2013,genres:['Drama','Romance','Sci-Fi'],director:'Spike Jonze',actors:['Joaquin Phoenix','Scarlett Johansson'],rating:4.6,poster:'poster-d',reason:'Thought-provoking romance',plot:'In a near future, a lonely writer develops an unlikely relationship with an advanced operating system.'},
  {id:'m17',title:'Parasite',year:2019,genres:['Drama','Thriller'],director:'Bong Joon Ho',actors:['Song Kang-ho','Lee Sun-kyun'],rating:4.9,poster:'poster-e',reason:'Masterful social tension',plot:'Greed and class discrimination threaten the relationship between the wealthy Park family and the destitute Kim clan.'},
  {id:'m18',title:'The Handmaiden',year:2016,genres:['Drama','Romance','Thriller'],director:'Park Chan-wook',actors:['Kim Min-hee','Kim Tae-ri'],rating:4.7,poster:'poster-f',reason:'Intricate twist-filled narrative',plot:'A woman is hired as a handmaiden to an heiress, but secretly is involved in a plot to defraud her.'},
  {id:'m19',title:'Before Sunrise',year:1995,genres:['Drama','Romance'],director:'Richard Linklater',actors:['Ethan Hawke','Julie Delpy'],rating:4.6,poster:'poster-a',reason:'Pure conversational intimacy',plot:'A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna.'},
  {id:'m20',title:'The Secret Life of Walter Mitty',year:2013,genres:['Adventure','Comedy'],director:'Ben Stiller',actors:['Ben Stiller','Kristen Wiig'],rating:4.4,poster:'poster-b',reason:'Vibrant escapism',plot:'A photo editor takes action by embarking on an adventure more extraordinary than anything he imagined.'}
];

let activeUserId = 'u1';
let currentMode = 'hybrid';
let rated = {m1:5, m3:5, m6:4, m8:4, m15:5, m19:4.5};
let library = new Set(Object.keys(rated));
let activeRecsMap = {}; // movieId -> recommendation object with explainability

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

function card(movie) {
  const rec = activeRecsMap[movie.id];
  const badgeText = rec ? `${rec.matchPercentage ? rec.matchPercentage + '% Match' : '✦ AI Pick'}` : (movie.reason ? `✦ ${movie.reason}` : '');
  const scoreText = rec ? `★ ${rec.hybridScore || rec.predictedRating || movie.rating}` : `★ ${movie.rating}`;
  const modelSub = rec && rec.explanation ? `<div style="font-size:9px;color:#a0a0a5;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${rec.explanation}</div>` : '';

  return `
    <article class="movie-card" data-id="${movie.id}">
      <div class="poster ${movie.poster}" style="background-image:url('${posterUrls[movie.id] || ''}')">
        ${badgeText ? `<span class="movie-badge">${badgeText}</span>` : ''}
      </div>
      <div class="movie-info">
        <span class="rating">${scoreText}</span>
        <h3>${movie.title}</h3>
        <p>${movie.year} · ${movie.genres.join(' / ')}</p>
        ${modelSub}
      </div>
    </article>
  `;
}

async function renderRecommendations() {
  const grid = $('#recommendation-grid');
  grid.innerHTML = '<div style="grid-column:1/-1;padding:30px;color:#85858b;text-align:center;">Running AI model inference...</div>';

  try {
    const res = await fetch(`/api/recommendations?userId=${activeUserId}&model=${currentMode}&top_n=8`);
    if (res.ok) {
      const data = await res.json();
      activeRecsMap = {};
      const recMovies = [];

      for (const r of data.recommendations) {
        activeRecsMap[r.movieId] = r;
        const catalogMovie = movies.find(m => m.id === r.movieId);
        if (catalogMovie) {
          recMovies.push(catalogMovie);
        } else {
          recMovies.push({
            id: r.movieId,
            title: r.title,
            year: r.releaseYear || 2024,
            genres: r.genres || [],
            director: r.director || '',
            actors: r.actors || [],
            rating: r.predictedRating || 4.5,
            poster: 'poster-a',
            plot: r.plotSummary || ''
          });
        }
      }

      if (recMovies.length > 0) {
        grid.innerHTML = recMovies.map(card).join('');
        bindCards();
        return;
      }
    }
  } catch (e) {
    console.log('Serving offline local recommendations fallback:', e);
  }

  // Fallback if API offline
  let list = [];
  if (currentMode === 'popular') {
    list = [...movies].sort((a,b) => b.rating - a.rating);
  } else if (currentMode === 'collaborative') {
    list = [movies[15], movies[1], movies[3], movies[12]];
  } else if (currentMode === 'content') {
    list = [movies[14], movies[18], movies[6], movies[7]];
  } else if (currentMode === 'graph') {
    list = [movies[1], movies[3], movies[12], movies[11]];
  } else {
    // Hybrid AI
    list = [movies[15], movies[1], movies[3], movies[12], movies[11], movies[16]];
  }
  activeRecsMap = {};
  grid.innerHTML = list.map(card).join('');
  bindCards();
}

function renderCatalog(query = '') {
  let list = movies.filter(m => (m.title + ' ' + m.genres.join(' ') + ' ' + m.actors.join(' ') + ' ' + m.director).toLowerCase().includes(query.toLowerCase()));
  $('#catalog-grid').innerHTML = list.map(card).join('');
  bindCards();
}

function renderLibrary() {
  let list = movies.filter(m => library.has(m.id));
  $('#library-grid').innerHTML = list.length ? list.map(card).join('') : '<p class="empty-state">Your shelf is waiting for a story.</p>';
  $('#library-count').textContent = list.length;
  bindCards();
}

function bindCards() {
  $$('.movie-card').forEach(c => c.addEventListener('click', () => openMovie(c.dataset.id)));
}

function openMovie(id) {
  const m = movies.find(x => x.id === id);
  if (!m) return;
  const rec = activeRecsMap[id];

  let explanationHtml = '';
  if (rec) {
    explanationHtml = `
      <div style="margin:16px 0;padding:14px;background:#131316;border:1px solid #282830;border-radius:6px;">
        <div style="font-size:11px;font-family:var(--mono);color:#f5c518;font-weight:700;margin-bottom:6px;">
          ✦ ${rec.model || 'AI Model Prediction'} · ${rec.matchPercentage ? rec.matchPercentage + '% Match' : ''}
        </div>
        <div style="font-size:12px;color:#e2e2e8;line-height:1.5;">${rec.explanation || ''}</div>
        ${rec.graphPath ? `<div style="font-size:10px;font-family:var(--mono);color:#70a8ff;margin-top:8px;padding-top:8px;border-top:1px dashed #33333d;word-break:break-all;"><strong>Graph Traversal Path:</strong><br>${rec.graphPath}</div>` : ''}
      </div>
    `;
  }

  $('#modal-content').innerHTML = `
    <div class="modal-poster poster ${m.poster}" style="background-image:url('${posterUrls[m.id] || ''}')"></div>
    <p class="eyebrow">${m.year} · ${m.genres.join(' / ')}</p>
    <h2>${m.title}</h2>
    <p class="modal-meta">
      Directed by ${m.director}<br>
      Starring ${m.actors.join(', ')}<br>
      <span class="rating">★ ${rec ? (rec.hybridScore || rec.predictedRating || m.rating) : m.rating}</span>
    </p>
    <p class="modal-copy">${m.plot}</p>
    ${explanationHtml}
    <div class="rating-actions">
      <button data-rate="5">★ Loved it</button>
      <button data-rate="4">Liked it</button>
      <button data-save>${library.has(m.id) ? '✓ In your library' : '＋ Add to library'}</button>
    </div>
  `;

  $('#movie-modal').classList.add('open');

  $$('[data-rate]').forEach(b => b.onclick = () => {
    rated[id] = Number(b.dataset.rate);
    library.add(id);
    renderLibrary();
    toast(`Rated ${m.title} ${b.dataset.rate}/5`);
    $('#movie-modal').classList.remove('open');
  });

  $('[data-save]').onclick = () => {
    library.has(id) ? library.delete(id) : library.add(id);
    renderLibrary();
    openMovie(id);
    toast(library.has(id) ? 'Added to your library' : 'Removed from your library');
  };
}

function toast(message) {
  const t = $('#toast');
  t.textContent = message;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2400);
}

function setupNav() {
  $$('.nav-item').forEach(button => button.onclick = () => {
    $$('.nav-item').forEach(x => x.classList.remove('active'));
    button.classList.add('active');
    $$('.view').forEach(v => v.classList.remove('active-view'));
    $(`#${button.dataset.view}-view`).classList.add('active-view');
    if (button.dataset.view === 'network') drawGraph();
    if (innerWidth < 651) $('.sidebar').classList.remove('open');
  });

  $('.mobile-menu').onclick = () => $('.sidebar').classList.toggle('open');
}

function setupUserSelector() {
  const userSelect = $('#user-selector');
  if (userSelect) {
    userSelect.onchange = e => {
      activeUserId = e.target.value;
      const selectedText = userSelect.options[userSelect.selectedIndex].text;
      const initials = selectedText.split(' ').map(n => n[0]).slice(0, 2).join('');
      $('#user-avatar').textContent = initials;
      $('#current-user-breadcrumb').textContent = `PERSONALIZED FOR ${selectedText.toUpperCase()}`;
      toast(`Switched profile to ${selectedText}`);
      renderRecommendations();
    };
  }
}

function drawGraph() {
  const canvas = $('#graph-canvas');
  if (!canvas) return;
  const box = canvas.getBoundingClientRect();
  const d = devicePixelRatio || 1;
  canvas.width = box.width * d;
  canvas.height = box.height * d;
  const ctx = canvas.getContext('2d');
  ctx.scale(d, d);
  const w = box.width, h = box.height;

  const nodes = [
    {x: w * .5, y: h * .48, r: 31, label: activeUserId.toUpperCase(), type: 'user'},
    {x: w * .25, y: h * .28, r: 25, label: 'Past Lives', type: 'movie'},
    {x: w * .74, y: h * .25, r: 25, label: 'Aftersun', type: 'movie'},
    {x: w * .8, y: h * .66, r: 25, label: 'Perfect Days', type: 'movie'},
    {x: w * .27, y: h * .76, r: 25, label: 'Drama', type: 'genre'},
    {x: w * .5, y: h * .12, r: 22, label: 'Romance', type: 'genre'},
    {x: w * .12, y: h * .53, r: 22, label: 'Celine Song', type: 'genre'},
    {x: w * .94, y: h * .43, r: 22, label: 'Wim Wenders', type: 'genre'}
  ];
  const links = [[0,1],[0,2],[0,3],[1,4],[1,5],[1,6],[2,4],[2,5],[3,4],[3,7]];

  ctx.lineWidth = 1;
  links.forEach(([a, b]) => {
    ctx.strokeStyle = '#4c535d';
    ctx.beginPath();
    ctx.moveTo(nodes[a].x, nodes[a].y);
    ctx.lineTo(nodes[b].x, nodes[b].y);
    ctx.stroke();
  });

  nodes.forEach(n => {
    ctx.shadowBlur = n.type === 'user' ? 18 : 8;
    ctx.shadowColor = n.type === 'user' ? '#e66b4e' : 'transparent';
    ctx.fillStyle = n.type === 'user' ? '#e66b4e' : n.type === 'movie' ? '#b3a9dc' : '#f0ba55';
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#fff';
    ctx.font = `${n.type === 'user' ? 11 : 9}px Manrope`;
    ctx.textAlign = 'center';
    ctx.fillText(n.label, n.x, n.y + n.r + 16);
  });
}

// Mode change buttons
$$('.segment').forEach(b => {
  b.onclick = () => {
    $$('.segment').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    currentMode = b.dataset.mode;
    renderRecommendations();
  };
});

// Scroll buttons (e.g. Explore AI Picks)
$$('[data-scroll]').forEach(btn => {
  btn.onclick = e => {
    e.preventDefault();
    const targetId = btn.dataset.scroll;
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };
});

// Click on hero movie card to open details
const heroFilmCard = $('.hero .film-card');
if (heroFilmCard) {
  heroFilmCard.style.cursor = 'pointer';
  heroFilmCard.onclick = () => openMovie('m1');
}

$('#search-input').oninput = e => renderCatalog(e.target.value);
$('.modal-close').onclick = () => $('#movie-modal').classList.remove('open');
$('#movie-modal').onclick = e => {
  if (e.target.id === 'movie-modal') $('#movie-modal').classList.remove('open');
};
$('#reset-graph').onclick = drawGraph;

setupNav();
setupUserSelector();
renderRecommendations();
renderCatalog();
renderLibrary();

window.onresize = () => {
  if ($('#network-view').classList.contains('active-view')) drawGraph();
};

