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

const FIELD_ORDER = [
  "생산/제조",
  "3D 프린팅",
  "로봇틱스(생산제조)",
  "AI 생산제조",
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

const TAG_CATEGORY_ALIASES = {
  툴패스: "툴패스 계획",
  경로계획: "그래프 탐색 / 경로 계획 알고리즘",
  재료분포: "재료분포 최적화",
  "퍼지 감소": "재료 전환 / 퍼지 감소",
  계산설계: "계산설계",
  MMAM: "다중재료 적층제조",
  FGAM: "기능성 구배 적층제조",
  "AI/ML": "적층제조를 위한 AI 및 머신러닝",
};

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
  venueBoard: document.querySelector("#venue-board"),
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
  renderVenueBoard();
  updateStats();
  applyFilters();

  [els.search, els.category, els.tag, els.venue, els.year, els.sort].forEach((el) => {
    el.addEventListener("input", applyFilters);
    el.addEventListener("change", applyFilters);
  });

}

function buildFilters() {
  const fields = new Set();
  const tags = new Set();
  const venues = new Set(TARGET_VENUES);
  const years = new Set();

  state.papers.forEach((paper) => {
    fields.add(deriveField(paper));
    visibleTags(paper).forEach((tag) => tags.add(tag));
    venues.add(normalizeVenue(paper.venue));
    if (paper.year) years.add(String(paper.year));
  });

  FIELD_ORDER.forEach((field) => {
    if (fields.has(field)) {
      els.category.append(new Option(field, field));
    }
  });
  [...fields]
    .filter((field) => !FIELD_ORDER.includes(field))
    .sort((a, b) => a.localeCompare(b, "ko"))
    .forEach((field) => {
      els.category.append(new Option(field, field));
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
  const fields = FIELD_ORDER.filter((field) => state.papers.some((paper) => deriveField(paper) === field));
  els.sideTopicNav.innerHTML = fields
    .map((field) => {
      const count = state.papers.filter((paper) => deriveField(paper) === field).length;
      return `<button type="button" data-side-category="${escapeAttribute(field)}">${escapeHtml(field)} <span>${count}</span></button>`;
    })
    .join("");

  els.sideTopicNav.querySelectorAll("[data-side-category]").forEach((button) => {
    button.addEventListener("click", () => {
      els.category.value = button.dataset.sideCategory;
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

function renderVenueBoard() {
  const entries = venueCountEntries();
  els.venueBoard.innerHTML = [
    `<button class="venue-card is-all is-active" type="button" data-board-venue="">
      <strong>All venues</strong>
      <span>${state.papers.length} papers</span>
    </button>`,
    ...entries.map(([venue, count]) => {
      const priority = isPriorityVenue(venue) ? "<em>priority</em>" : "";
      return `<button class="venue-card" type="button" data-board-venue="${escapeAttribute(venue)}">
        <strong>${escapeHtml(shortVenue(venue))}</strong>
        <span>${count} papers</span>
        ${priority}
      </button>`;
    }),
  ].join("");

  els.venueBoard.querySelectorAll("[data-board-venue]").forEach((button) => {
    button.addEventListener("click", () => {
      const venue = button.dataset.boardVenue;
      state.activeTargetVenue = isPriorityVenue(venue) ? venue : "";
      els.venue.value = venue && !isPriorityVenue(venue) ? venue : "";
      if (!venue) {
        state.activeTargetVenue = "";
        els.venue.value = "";
      }
      els.venueNav.querySelectorAll(".venue-pill").forEach((pill) => {
        pill.classList.toggle("is-active", pill.dataset.targetVenue === state.activeTargetVenue);
      });
      els.venueBoard.querySelectorAll(".venue-card").forEach((card) => {
        card.classList.toggle("is-active", card.dataset.boardVenue === venue);
      });
      applyFilters();
      const paperList = document.querySelector("#paper-list");
      if (paperList) {
        paperList.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

function updateStats() {
  const categories = new Set(state.papers.map((paper) => deriveField(paper)));
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
    const paperVisibleTags = visibleTags(paper);
    const paperVenue = normalizeVenue(paper.venue);
    const paperField = deriveField(paper);
    const haystack = normalize(
      [
        paperField,
        paper.title,
        (paper.authors || []).join(" "),
        paper.venue,
        paper.doi,
        paperCategories.join(" "),
        paperVisibleTags.join(" "),
        paper.ai_summary_ko,
        paper.relevance_note_ko,
      ].join(" ")
    );

    const matchesQuery = !query || haystack.includes(query);
    const matchesCategory = !category || paperField === category;
    const matchesTag = !tag || paperTags.includes(tag);
    const matchesVenue = !venue || paperVenue === venue;
    const matchesTarget = !state.activeTargetVenue || matchesTargetVenue(paperVenue, state.activeTargetVenue);
    const matchesTopic = !state.activeTopic || paperTags.includes(state.activeTopic) || paperCategories.includes(state.activeTopic);
    const matchesYear = !year || String(paper.year || "") === year;
    return (
      matchesQuery &&
      matchesCategory &&
      matchesTag &&
      matchesVenue &&
      matchesTarget &&
      matchesTopic &&
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

  render();
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
    const category = deriveField(paper);
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
  const tagBadges = visibleTags(paper).map((tag) => tagButton(tag)).join("");

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

function visibleTags(paper) {
  const categories = new Set(paper.categories || []);
  const seen = new Set();
  return (paper.tags || []).filter((tag) => {
    if (!tag || seen.has(tag)) return false;
    seen.add(tag);
    if (categories.has(tag)) return false;
    const aliasCategory = TAG_CATEGORY_ALIASES[tag];
    if (aliasCategory && categories.has(aliasCategory)) return false;
    return true;
  });
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
  const index = FIELD_ORDER.indexOf(category);
  return index === -1 ? FIELD_ORDER.length : index;
}

function deriveField(paper) {
  const titleText = normalize(
    [
      paper.title,
      paper.venue,
      (paper.tags || []).join(" "),
    ].join(" ")
  );
  const categoryText = normalize((paper.categories || []).join(" "));
  const text = `${titleText} ${categoryText}`;

  if (titleText.includes("robot") || titleText.includes("로봇")) {
    return "로봇틱스(생산제조)";
  }
  if (
    titleText.includes("ai/ml") ||
    titleText.includes("machine learning") ||
    titleText.includes("deep learning") ||
    titleText.includes("reinforcement learning") ||
    titleText.includes("artificial intelligence") ||
    titleText.includes("neural") ||
    titleText.includes("머신러닝") ||
    titleText.includes("인공지능") ||
    categoryText.includes("ai")
  ) {
    return "AI 생산제조";
  }
  if (
    titleText.includes("3d printing") ||
    titleText.includes("3d print") ||
    titleText.includes("fdm") ||
    titleText.includes("dm filament") ||
    titleText.includes("digital material") ||
    titleText.includes("functionally graded") ||
    titleText.includes("fgam") ||
    titleText.includes("multi-material") ||
    titleText.includes("multimaterial") ||
    titleText.includes("toolpath") ||
    titleText.includes("material extrusion") ||
    titleText.includes("다중재료") ||
    titleText.includes("기능성 구배") ||
    titleText.includes("툴패스") ||
    titleText.includes("재료 전환") ||
    titleText.includes("3d 프린팅")
  ) {
    return "3D 프린팅";
  }
  if (
    text.includes("manufacturing") ||
    text.includes("production") ||
    text.includes("process") ||
    text.includes("metals") ||
    text.includes("alloys") ||
    text.includes("construction") ||
    text.includes("fabrication") ||
    text.includes("제조") ||
    text.includes("생산")
  ) {
    return "생산/제조";
  }
  return "생산/제조";
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
