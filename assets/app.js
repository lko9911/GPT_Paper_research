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

const state = {
  papers: [],
  filtered: [],
};

const els = {
  list: document.querySelector("#paper-list"),
  empty: document.querySelector("#empty-state"),
  count: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  category: document.querySelector("#category-filter"),
  year: document.querySelector("#year-filter"),
  sort: document.querySelector("#sort-select"),
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
  updateStats();
  applyFilters();

  [els.search, els.category, els.year, els.sort].forEach((el) => {
    el.addEventListener("input", applyFilters);
    el.addEventListener("change", applyFilters);
  });
}

function buildFilters() {
  const categories = new Set();
  const years = new Set();

  state.papers.forEach((paper) => {
    (paper.categories || []).forEach((category) => categories.add(category));
    if (paper.year) years.add(String(paper.year));
  });

  [...CATEGORY_ORDER, ...categories]
    .filter((category, index, array) => category && array.indexOf(category) === index)
    .forEach((category) => {
      if (!categories.has(category)) return;
      els.category.append(new Option(category, category));
    });

  [...years]
    .sort((a, b) => Number(b) - Number(a))
    .forEach((year) => els.year.append(new Option(year, year)));
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
  const year = els.year.value;
  const sort = els.sort.value;

  state.filtered = state.papers.filter((paper) => {
    const haystack = normalize(
      [
        paper.title,
        (paper.authors || []).join(" "),
        paper.venue,
        paper.doi,
        (paper.categories || []).join(" "),
        (paper.tags || []).join(" "),
        paper.ai_summary_ko,
        paper.relevance_note_ko,
      ].join(" ")
    );

    const matchesQuery = !query || haystack.includes(query);
    const matchesCategory = !category || (paper.categories || []).includes(category);
    const matchesYear = !year || String(paper.year || "") === year;
    return matchesQuery && matchesCategory && matchesYear;
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
  state.filtered.forEach((paper) => fragment.append(renderCard(paper)));
  els.list.append(fragment);
}

function renderCard(paper) {
  const article = document.createElement("article");
  article.className = "paper-card";

  const doiUrl = paper.url || (paper.doi ? `https://doi.org/${paper.doi}` : "");
  const sourceText = (paper.source || []).join(", ") || "Metadata API";
  const authors = formatAuthors(paper.authors || []);

  article.innerHTML = `
    <h3 class="paper-title">${escapeHtml(paper.title || "Untitled")}</h3>
    <p class="meta">${escapeHtml(authors)}${authors ? " · " : ""}${escapeHtml(String(paper.year || "연도 미상"))} · ${escapeHtml(paper.venue || "Venue unknown")} · ${escapeHtml(sourceText)}</p>
    <div class="badge-row">
      ${badge(String(paper.year || "연도 미상"), "year")}
      ${badge(`관련성 ${paper.relevance_score || "-"} / 10`, "score")}
      ${(paper.categories || []).map((category) => badge(category, "category")).join("")}
      ${(paper.tags || []).map((tag) => badge(tag)).join("")}
    </div>
    <p class="summary">${escapeHtml(paper.ai_summary_ko || "요약이 아직 생성되지 않았습니다.")}</p>
    <p class="relevance-note">${escapeHtml(paper.relevance_note_ko || "")}</p>
    <p class="meta">마지막 업데이트: ${escapeHtml(paper.last_updated || "-")} · Raw abstract displayed: ${paper.raw_abstract_displayed === false ? "false" : "unknown"} · PDF stored: ${paper.pdf_stored === false ? "false" : "unknown"}</p>
    <div class="actions">
      ${doiUrl ? `<a class="button primary" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">DOI 열기</a>` : ""}
      ${doiUrl ? `<a class="button" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">Source 열기</a>` : ""}
      <button class="button" type="button" data-citation>citation 복사</button>
    </div>
  `;

  article.querySelector("[data-citation]").addEventListener("click", async (event) => {
    const citation = buildCitation(paper);
    await navigator.clipboard.writeText(citation);
    event.currentTarget.textContent = "복사됨";
    window.setTimeout(() => {
      event.currentTarget.textContent = "citation 복사";
    }, 1400);
  });

  return article;
}

function badge(text, className = "") {
  return `<span class="badge ${className}">${escapeHtml(text)}</span>`;
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
