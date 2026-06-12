const CATEGORY_ORDER = [
  "리뷰 및 서베이",
  "다중재료 적층제조",
  "기능성 구배 적층제조",
  "Blended FDM / Digital Material Filament",
  "계산설계",
  "재료분포 최적화",
  "툴패스 계획",
  "재료 전환 / 퍼지 감소",
  "그래프 탐색 / 경로 계획 알고리즘",
  "적층제조를 위한 AI 및 머신러닝",
];

const FEATURED_TOPICS = [
  "MMAM",
  "FGAM",
  "DM filament",
  "계산설계",
  "재료분포",
  "툴패스",
  "퍼지 감소",
  "AI/ML",
];

const TARGET_VENUES = [
  "Nature",
  "Nature Communications",
  "Nature Materials",
  "Nature Reviews Materials",
  "Science",
  "Science Advances",
  "Science Robotics",
  "Additive Manufacturing",
];

const state = {
  papers: [],
  filtered: [],
  activeTopic: "",
  activeTargetVenue: "",
  matrixCategory: "",
  matrixVenue: "",
  venueColumns: [],
};

const els = {
  list: document.querySelector("#paper-list"),
  empty: document.querySelector("#empty-state"),
  count: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  category: document.querySelector("#category-filter"),
  tag: document.querySelector("#tag-filter"),
  venue: document.querySelector("#venue-filter"),
  year: document.querySelector("#year-filter"),
  sort: document.querySelector("#sort-select"),
  topicNav: document.querySelector(".topic-nav"),
  venueNav: document.querySelector(".venue-nav"),
  sideTopicNav: document.querySelector("#side-topic-nav"),
  sideVenueNav: document.querySelector("#side-venue-nav"),
  matrix: document.querySelector("#venue-matrix"),
  matrixClear: document.querySelector("#matrix-clear"),
  total: document.querySelector("#stat-total"),
  categories: document.querySelector("#stat-categories"),
  updated: document.querySelector("#stat-updated"),
  week: document.querySelector("#stat-week"),
};

async function init() {
  try {
    const response = await fetch(`data/papers.json?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.papers = await response.json();
  } catch (error) {
    console.error("Failed to load papers.json", error);
    state.papers = [];
  }

  buildFilters();
  buildTopicNav();
  buildVenueNav();
  buildSideNav();
  buildVenueMatrix();
  updateStats();
  applyFilters();

  [els.search, els.category, els.tag, els.venue, els.year, els.sort].forEach((el) => {
    el.addEventListener("input", applyFilters);
    el.addEventListener("change", applyFilters);
  });

  els.matrixClear.addEventListener("click", () => {
    state.matrixCategory = "";
    state.matrixVenue = "";
    applyFilters();
  });
}

function buildFilters() {
  const categories = new Set();
  const tags = new Set();
  const venues = new Set(TARGET_VENUES);
  const years = new Set();

  state.papers.forEach((paper) => {
    (paper.categories || []).forEach((category) => categories.add(category));
    (paper.tags || []).forEach((tag) => tags.add(tag));
    venues.add(normalizeVenue(paper.venue));
    if (paper.year) years.add(String(paper.year));
  });

  [...CATEGORY_ORDER, ...categories]
    .filter((category, index, array) => category && array.indexOf(category) === index)
    .forEach((category) => {
      if (categories.has(category)) els.category.append(new Option(category, category));
    });

  [...tags].sort((a, b) => a.localeCompare(b, "ko")).forEach((tag) => {
    els.tag.append(new Option(tag, tag));
  });

  [...venues].sort((a, b) => a.localeCompare(b, "ko")).forEach((venue) => {
    els.venue.append(new Option(venue, venue));
  });

  [...years]
    .sort((a, b) => Number(b) - Number(a))
    .forEach((year) => els.year.append(new Option(year, year)));
}

function buildTopicNav() {
  const availableTags = new Set(flatten(state.papers.map((paper) => paper.tags || [])));
  const availableCategories = new Set(flatten(state.papers.map((paper) => paper.categories || [])));
  const topics = FEATURED_TOPICS.filter((topic) => availableTags.has(topic) || availableCategories.has(topic));

  topics.forEach((topic) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "topic-pill";
    button.dataset.topic = topic;
    button.textContent = topic;
    els.topicNav.append(button);
  });

  els.topicNav.addEventListener("click", (event) => {
    const button = event.target.closest("[data-topic]");
    if (!button) return;
    state.activeTopic = button.dataset.topic;
    els.topicNav.querySelectorAll(".topic-pill").forEach((pill) => {
      pill.classList.toggle("is-active", pill.dataset.topic === state.activeTopic);
    });
    applyFilters();
  });
}

function buildVenueNav() {
  TARGET_VENUES.forEach((venue) => {
    const count = state.papers.filter((paper) => matchesTargetVenue(normalizeVenue(paper.venue), venue)).length;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "venue-pill";
    button.dataset.targetVenue = venue;
    button.textContent = `${shortVenue(venue)} ${count}`;
    button.disabled = count === 0;
    button.title = count === 0 ? "아직 수집된 논문이 없습니다." : `${venue} 논문만 보기`;
    els.venueNav.append(button);
  });

  els.venueNav.addEventListener("click", (event) => {
    const button = event.target.closest("[data-target-venue]");
    if (!button) return;
    state.activeTargetVenue = button.dataset.targetVenue;
    if (state.activeTargetVenue) {
      els.venue.value = "";
    }
    els.venueNav.querySelectorAll(".venue-pill").forEach((pill) => {
      pill.classList.toggle("is-active", pill.dataset.targetVenue === state.activeTargetVenue);
    });
    applyFilters();
  });
}

function buildSideNav() {
  const categories = CATEGORY_ORDER.filter((category) =>
    state.papers.some((paper) => (paper.categories || []).includes(category))
  );
  const venueCounts = venueCountEntries();
  els.sideTopicNav.innerHTML = categories
    .map((category) => `<a href="#${escapeAttribute(sectionId(category))}">${escapeHtml(category)}</a>`)
    .join("");
  els.sideVenueNav.innerHTML = [
    '<button type="button" data-side-venue="">All venues <span>' + state.papers.length + "</span></button>",
    ...venueCounts.map(([venue, count]) => {
      return `<button type="button" data-side-venue="${escapeAttribute(venue)}">${escapeHtml(shortVenue(venue))} <span>${count}</span></button>`;
    }),
  ].join("");

  els.sideVenueNav.querySelectorAll("[data-side-venue]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeTargetVenue = button.dataset.sideVenue;
      els.venue.value = state.activeTargetVenue && !isPriorityVenue(state.activeTargetVenue) ? state.activeTargetVenue : "";
      els.venueNav.querySelectorAll(".venue-pill").forEach((pill) => {
        pill.classList.toggle("is-active", pill.dataset.targetVenue === state.activeTargetVenue);
      });
      applyFilters();
      const paperList = document.querySelector("#paper-list");
      if (paperList) {
        paperList.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

function venueCountEntries() {
  const counts = new Map();
  state.papers.forEach((paper) => {
    const venue = normalizeVenue(paper.venue);
    counts.set(venue, (counts.get(venue) || 0) + 1);
  });
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "ko"));
}

function buildVenueMatrix() {
  const venueCounts = new Map();
  state.papers.forEach((paper) => {
    const venue = normalizeVenue(paper.venue);
    venueCounts.set(venue, (venueCounts.get(venue) || 0) + 1);
  });

  const targetColumns = TARGET_VENUES.filter((venue) => venueCounts.has(venue));
  const otherColumns = [...venueCounts.entries()]
    .filter(([venue]) => !targetColumns.includes(venue))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "ko"))
    .slice(0, Math.max(0, 8 - targetColumns.length))
    .map(([venue]) => venue);

  state.venueColumns = [...targetColumns, ...otherColumns];
  const uncategorizedVenues = [...venueCounts.keys()].filter((venue) => !state.venueColumns.includes(venue));
  if (uncategorizedVenues.length) state.venueColumns.push("Other venues");
}

function updateStats() {
  const categories = new Set(flatten(state.papers.map((paper) => paper.categories || [])));
  const updatedDates = state.papers
    .map((paper) => paper.last_updated || paper.first_added)
    .filter(Boolean)
    .sort();
  const latestDate = updatedDates.length ? updatedDates[updatedDates.length - 1] : "";
  const weekAgo = new Date();
  weekAgo.setDate(weekAgo.getDate() - 7);
  const weekCount = state.papers.filter((paper) => {
    if (!paper.first_added) return false;
    return new Date(`${paper.first_added}T00:00:00`) >= weekAgo;
  }).length;

  els.total.textContent = state.papers.length.toLocaleString("ko-KR");
  els.categories.textContent = categories.size.toLocaleString("ko-KR");
  els.updated.textContent = latestDate || "-";
  els.week.textContent = weekCount.toLocaleString("ko-KR");
}

function applyFilters() {
  const query = normalize(els.search.value);
  const category = els.category.value;
  const tag = els.tag.value;
  const venue = els.venue.value;
  const year = els.year.value;
  const sort = els.sort.value;

  state.filtered = state.papers.filter((paper) => {
    const paperCategories = paper.categories || [];
    const paperTags = paper.tags || [];
    const paperVenue = normalizeVenue(paper.venue);
    const haystack = normalize(
      [
        paper.title,
        (paper.authors || []).join(" "),
        paper.venue,
        paper.doi,
        paperCategories.join(" "),
        paperTags.join(" "),
        paper.ai_summary_ko,
        paper.relevance_note_ko,
      ].join(" ")
    );

    const matchesQuery = !query || haystack.includes(query);
    const matchesCategory = !category || paperCategories.includes(category);
    const matchesTag = !tag || paperTags.includes(tag);
    const matchesVenue = !venue || paperVenue === venue;
    const matchesTarget = !state.activeTargetVenue || matchesTargetVenue(paperVenue, state.activeTargetVenue);
    const matchesTopic = !state.activeTopic || paperTags.includes(state.activeTopic) || paperCategories.includes(state.activeTopic);
    const matchesMatrixCategory = !state.matrixCategory || paperCategories.includes(state.matrixCategory);
    const matchesMatrixVenue = !state.matrixVenue || venueBucket(paperVenue) === state.matrixVenue;
    const matchesYear = !year || String(paper.year || "") === year;
    return (
      matchesQuery &&
      matchesCategory &&
      matchesTag &&
      matchesVenue &&
      matchesTarget &&
      matchesTopic &&
      matchesMatrixCategory &&
      matchesMatrixVenue &&
      matchesYear
    );
  });

  state.filtered.sort((a, b) => {
    if (sort === "newest") {
      return Number(b.year || 0) - Number(a.year || 0) || dateValue(b.last_updated) - dateValue(a.last_updated);
    }
    if (sort === "title") {
      return (a.title || "").localeCompare(b.title || "", "ko");
    }
    return Number(b.relevance_score || 0) - Number(a.relevance_score || 0) || Number(b.year || 0) - Number(a.year || 0);
  });

  renderMatrix();
  render();
}

function renderMatrix() {
  els.matrix.innerHTML = "";

  const categories = CATEGORY_ORDER.filter((category) =>
    state.papers.some((paper) => (paper.categories || []).includes(category))
  );
  const table = document.createElement("table");
  table.className = "matrix-table";
  table.innerHTML = `
    <thead>
      <tr>
        <th scope="col">주제</th>
        ${state.venueColumns.map((venue) => `<th scope="col">${escapeHtml(shortVenue(venue))}</th>`).join("")}
        <th scope="col">합계</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;

  const tbody = table.querySelector("tbody");
  categories.forEach((category) => {
    const rowPapers = state.papers.filter((paper) => (paper.categories || []).includes(category));
    const row = document.createElement("tr");
    row.innerHTML = `
      <th scope="row">${escapeHtml(category)}</th>
      ${state.venueColumns.map((venue) => matrixCell(category, venue)).join("")}
      <td class="matrix-total">${rowPapers.length}</td>
    `;
    tbody.append(row);
  });

  els.matrix.append(table);
  els.matrix.querySelectorAll("[data-matrix-category]").forEach((button) => {
    button.addEventListener("click", () => {
      state.matrixCategory = button.dataset.matrixCategory;
      state.matrixVenue = button.dataset.matrixVenue;
      applyFilters();
    });
  });

  els.matrixClear.hidden = !(state.matrixCategory || state.matrixVenue);
}

function matrixCell(category, venue) {
  const papers = state.papers.filter((paper) => {
    const categories = paper.categories || [];
    return categories.includes(category) && venueBucket(normalizeVenue(paper.venue)) === venue;
  });
  const active = state.matrixCategory === category && state.matrixVenue === venue;
  if (!papers.length) return '<td class="matrix-empty">-</td>';
  return `
    <td>
      <button class="matrix-count ${active ? "is-active" : ""}" type="button" data-matrix-category="${escapeAttribute(category)}" data-matrix-venue="${escapeAttribute(venue)}">
        ${papers.length}
      </button>
    </td>
  `;
}

function render() {
  els.count.textContent = `${state.filtered.length.toLocaleString("ko-KR")}편 표시 중`;
  els.list.innerHTML = "";
  els.empty.hidden = state.filtered.length > 0;

  const fragment = document.createDocumentFragment();
  const groups = groupByPrimaryCategory(state.filtered);
  groups.forEach(([category, papers]) => {
    fragment.append(renderGroup(category, papers));
  });
  els.list.append(fragment);
}

function groupByPrimaryCategory(papers) {
  const grouped = new Map();
  papers.forEach((paper) => {
    const category = (paper.categories || [])[0] || "기타";
    if (!grouped.has(category)) grouped.set(category, []);
    grouped.get(category).push(paper);
  });
  return [...grouped.entries()].sort((a, b) => categoryIndex(a[0]) - categoryIndex(b[0]));
}

function renderGroup(category, papers) {
  const section = document.createElement("section");
  section.className = "paper-group";
  section.id = sectionId(category);
  section.innerHTML = `
    <div class="group-heading">
      <h3>${escapeHtml(category)}</h3>
      <span>${papers.length.toLocaleString("ko-KR")} papers</span>
    </div>
  `;
  papers.forEach((paper) => section.append(renderPaperRow(paper)));
  return section;
}

function renderPaperRow(paper) {
  const article = document.createElement("article");
  article.className = "paper-card";

  const doiUrl = paper.url || (paper.doi ? `https://doi.org/${paper.doi}` : "");
  const sourceText = (paper.source || []).join(", ") || "Metadata API";
  const authors = formatAuthors(paper.authors || []);
  const categoryBadges = (paper.categories || []).map((category) => badge(category, "category")).join("");
  const tagBadges = (paper.tags || []).map((tag) => tagButton(tag)).join("");

  article.innerHTML = `
    <div class="card-content">
      <div class="card-topline">
        <span>${escapeHtml(String(paper.year || "연도 미상"))}</span>
        <span>관련성 ${escapeHtml(String(paper.relevance_score || "-"))}/10</span>
      </div>
      <h4 class="paper-title">${escapeHtml(paper.title || "Untitled")}</h4>
      <p class="meta">${escapeHtml(authors)}${authors ? " · " : ""}${escapeHtml(String(paper.year || "연도 미상"))} · ${escapeHtml(paper.venue || "Venue unknown")} · ${escapeHtml(sourceText)}</p>
      <p class="summary">${escapeHtml(paper.ai_summary_ko || "요약이 아직 생성되지 않았습니다.")}</p>
      <p class="relevance-note">${escapeHtml(paper.relevance_note_ko || "")}</p>
      <div class="tag-line">${categoryBadges}${tagBadges}</div>
      <div class="card-links">
        ${doiUrl ? `<a class="link-pill primary" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">Paper</a>` : ""}
        ${doiUrl ? `<a class="link-pill" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">DOI</a>` : ""}
        <button class="link-pill" type="button" data-citation>Copy Cite</button>
      </div>
      <p class="policy-mini">No abstract/PDF hosted · updated ${escapeHtml(paper.last_updated || "-")}</p>
    </div>
  `;

  article.querySelector("[data-citation]").addEventListener("click", async (event) => {
    const citation = buildCitation(paper);
    await navigator.clipboard.writeText(citation);
    event.currentTarget.textContent = "Copied";
    window.setTimeout(() => {
      event.currentTarget.textContent = "Copy Cite";
    }, 1400);
  });

  article.querySelectorAll("[data-tag-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      els.tag.value = button.dataset.tagFilter;
      applyFilters();
    });
  });

  return article;
}

function badge(text, className = "") {
  return `<span class="badge ${className}">${escapeHtml(text)}</span>`;
}

function tagButton(text) {
  return `<button class="badge tag" type="button" data-tag-filter="${escapeAttribute(text)}">${escapeHtml(text)}</button>`;
}

function buildCitation(paper) {
  const authors = (paper.authors || []).join(", ");
  const year = paper.year ? `(${paper.year})` : "";
  const venue = paper.venue ? ` ${paper.venue}.` : "";
  const doi = paper.doi ? ` https://doi.org/${paper.doi}` : "";
  return `${authors} ${year}. ${paper.title || "Untitled"}.${venue}${doi}`.replace(/\s+/g, " ").trim();
}

function formatAuthors(authors) {
  if (!authors.length) return "";
  if (authors.length <= 3) return authors.join(", ");
  return `${authors.slice(0, 3).join(", ")} 외 ${authors.length - 3}명`;
}

function categoryIndex(category) {
  const index = CATEGORY_ORDER.indexOf(category);
  return index === -1 ? CATEGORY_ORDER.length : index;
}

function sectionId(value) {
  return `section-${normalize(value).replace(/[^a-z0-9가-힣]+/g, "-").replace(/^-|-$/g, "") || "unknown"}`;
}

function normalizeVenue(venue) {
  return String(venue || "Venue unknown").trim() || "Venue unknown";
}

function normalizeVenueKey(venue) {
  return normalize(venue).replace(/&/g, "and");
}

function matchesTargetVenue(venue, target) {
  return normalizeVenueKey(venue) === normalizeVenueKey(target);
}

function isPriorityVenue(venue) {
  return TARGET_VENUES.some((target) => matchesTargetVenue(venue, target));
}

function venueBucket(venue) {
  return state.venueColumns.includes(venue) ? venue : "Other venues";
}

function shortVenue(venue) {
  const replacements = {
    "Nature Communications": "Nat. Commun.",
    "Nature Materials": "Nat. Mater.",
    "Nature Reviews Materials": "Nat. Rev. Mater.",
    "Science Advances": "Sci. Adv.",
    "Science Robotics": "Sci. Robot.",
    "Additive Manufacturing": "Addit. Manuf.",
    "Rapid Prototyping Journal": "Rapid Prototyping",
    "Journal of Manufacturing Processes": "J. Manufacturing",
    "Physics in Medicine and Biology": "Phys. Med. Biol.",
    "Advanced Engineering Materials": "Adv. Eng. Mater.",
    "Engineering With Computers": "Eng. with Computers",
    "npj Artificial Intelligence": "npj AI",
  };
  return replacements[venue] || venue;
}

function normalize(value) {
  return String(value || "").toLowerCase().trim();
}

function dateValue(value) {
  return value ? new Date(`${value}T00:00:00`).getTime() : 0;
}

function flatten(items) {
  return items.reduce((acc, item) => acc.concat(item), []);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}

init();
