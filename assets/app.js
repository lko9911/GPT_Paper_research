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

const state = {
  papers: [],
  filtered: [],
  activeTopic: "",
};

const els = {
  list: document.querySelector("#paper-list"),
  empty: document.querySelector("#empty-state"),
  count: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  category: document.querySelector("#category-filter"),
  tag: document.querySelector("#tag-filter"),
  year: document.querySelector("#year-filter"),
  sort: document.querySelector("#sort-select"),
  topicNav: document.querySelector(".topic-nav"),
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
  updateStats();
  applyFilters();

  [els.search, els.category, els.tag, els.year, els.sort].forEach((el) => {
    el.addEventListener("input", applyFilters);
    el.addEventListener("change", applyFilters);
  });
}

function buildFilters() {
  const categories = new Set();
  const tags = new Set();
  const years = new Set();

  state.papers.forEach((paper) => {
    (paper.categories || []).forEach((category) => categories.add(category));
    (paper.tags || []).forEach((tag) => tags.add(tag));
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

  [...years]
    .sort((a, b) => Number(b) - Number(a))
    .forEach((year) => els.year.append(new Option(year, year)));
}

function buildTopicNav() {
  const availableTags = new Set(state.papers.flatMap((paper) => paper.tags || []));
  const availableCategories = new Set(state.papers.flatMap((paper) => paper.categories || []));
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

function updateStats() {
  const categories = new Set(state.papers.flatMap((paper) => paper.categories || []));
  const latestDate = state.papers
    .map((paper) => paper.last_updated || paper.first_added)
    .filter(Boolean)
    .sort()
    .at(-1);
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
  const year = els.year.value;
  const sort = els.sort.value;

  state.filtered = state.papers.filter((paper) => {
    const paperCategories = paper.categories || [];
    const paperTags = paper.tags || [];
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
    const matchesTopic = !state.activeTopic || paperTags.includes(state.activeTopic) || paperCategories.includes(state.activeTopic);
    const matchesYear = !year || String(paper.year || "") === year;
    return matchesQuery && matchesCategory && matchesTag && matchesTopic && matchesYear;
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
    const category = (paper.categories || [])[0] || "기타";
    if (!grouped.has(category)) grouped.set(category, []);
    grouped.get(category).push(paper);
  });
  return [...grouped.entries()].sort((a, b) => categoryIndex(a[0]) - categoryIndex(b[0]));
}

function renderGroup(category, papers) {
  const section = document.createElement("section");
  section.className = "paper-group";
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
  article.className = "paper-row";

  const doiUrl = paper.url || (paper.doi ? `https://doi.org/${paper.doi}` : "");
  const sourceText = (paper.source || []).join(", ") || "Metadata API";
  const authors = formatAuthors(paper.authors || []);
  const categoryBadges = (paper.categories || []).map((category) => badge(category, "category")).join("");
  const tagBadges = (paper.tags || []).map((tag) => tagButton(tag)).join("");

  article.innerHTML = `
    <div class="paper-main">
      <h4 class="paper-title">${escapeHtml(paper.title || "Untitled")}</h4>
      <p class="meta">${escapeHtml(authors)}${authors ? " · " : ""}${escapeHtml(String(paper.year || "연도 미상"))} · ${escapeHtml(paper.venue || "Venue unknown")} · ${escapeHtml(sourceText)}</p>
      <p class="summary">${escapeHtml(paper.ai_summary_ko || "요약이 아직 생성되지 않았습니다.")}</p>
      <p class="relevance-note">${escapeHtml(paper.relevance_note_ko || "")}</p>
      <div class="tag-line">${categoryBadges}${tagBadges}</div>
    </div>
    <aside class="paper-side">
      <span class="score-badge">${escapeHtml(String(paper.relevance_score || "-"))}<small>/10</small></span>
      <span class="year-badge">${escapeHtml(String(paper.year || "-"))}</span>
      <div class="link-stack">
        ${doiUrl ? `<a class="link-pill primary" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">Paper</a>` : ""}
        ${doiUrl ? `<a class="link-pill" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">DOI</a>` : ""}
        <button class="link-pill" type="button" data-citation>Copy Cite</button>
      </div>
      <p class="policy-mini">No abstract/PDF hosted · updated ${escapeHtml(paper.last_updated || "-")}</p>
    </aside>
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

function normalize(value) {
  return String(value || "").toLowerCase().trim();
}

function dateValue(value) {
  return value ? new Date(`${value}T00:00:00`).getTime() : 0;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

init();
