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
  "4D 프린팅",
  "로봇틱스(생산제조)",
  "AI 생산제조",
];

const FIELD_SUBTOPICS = {
  "생산/제조": ["공정 최적화", "금속/합금 제조", "복합재/소재 제조"],
  "3D 프린팅": ["DLP", "Toolpath", "Material Switching"],
  "4D 프린팅": ["LCE", "메타물질", "Active materials"],
  "로봇틱스(생산제조)": ["로봇 AM", "제조 자동화", "Path Planning"],
  "AI 생산제조": ["Machine Learning", "Design Automation"],
};

const SIDEBAR_OTHER_TOPIC = "__field_other__";

const FEATURED_TOPICS = [
  "MMAM",
  "FGAM",
  "DM filament",
  "DLP",
  "4D printing",
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

const UI_TEXT = {
  ko: {
    themeDark: "Dark",
    themeLight: "Light",
    langToggle: "EN",
    subtitle: "생산·제조, 3D/4D 프린팅, 로봇틱스, AI 제조 분야를 위한 AI 기반 논문 큐레이션 저장소",
    noticeMain: "본 저장소는 DOI 링크와 AI 생성 요약만 제공합니다. 저작권이 있는 PDF나 출판사 초록 원문을 호스팅하지 않습니다.",
    noticeSoft:
      "본 사이트의 요약은 공개된 논문 메타데이터 및 초록을 바탕으로 AI가 새로 작성한 한글 요약입니다. 원문 및 정확한 내용은 DOI 링크를 통해 확인하세요.",
    sideTitle: "분야 및 서브 토픽",
    totalPapers: "전체 논문 수",
    subtopicCount: "서브토픽 수",
    latestUpdate: "현재 / 갱신",
    weekAdded: "이번 주 추가",
    search: "검색",
    searchPlaceholder: "키워드, 저자, 태그, 요약 검색",
    field: "분야",
    tagSubtopic: "태그/서브 토픽",
    venue: "게재지",
    year: "연도",
    sort: "정렬",
    all: "전체",
    newest: "최신순",
    relevance: "관련성 점수순",
    title: "제목순",
    venuesTitle: "주요 게재지",
    allVenues: "All venues",
    papersByField: "Papers by Field",
    curatedPapers: "Curated Papers",
    emptyTitle: "표시할 논문이 없습니다.",
    emptyText: "검색어와 필터를 조정하거나 GitHub Actions 업데이트를 실행해 보세요.",
    footer:
      "Metadata from OpenAlex, Crossref, and optionally Semantic Scholar. Summaries are generated and do not reproduce publisher abstracts.",
    papers: "papers",
    priority: "Core",
    others: "Others",
    lowCountVenue: "2편 이하 게재지",
    showing: "편 표시 중",
    unknownYear: "연도 미상",
    relevanceLabel: "관련성",
    summaryMissing: "요약이 아직 생성되지 않았습니다.",
  },
  en: {
    themeDark: "Dark",
    themeLight: "Light",
    langToggle: "KO",
    subtitle: "An AI-assisted research tracker for manufacturing, 3D/4D printing, robotics, and AI-driven production.",
    noticeMain: "This repository provides DOI links and AI-generated summaries only. It does not host copyrighted PDFs or publisher abstract text.",
    noticeSoft:
      "Summaries on this site are newly written AI summaries based on public paper metadata and abstracts. Check the DOI link for the original and authoritative content.",
    sideTitle: "Fields and Subtopics",
    totalPapers: "Total Papers",
    subtopicCount: "Subtopics",
    latestUpdate: "Now / Updated",
    weekAdded: "Added This Week",
    search: "Search",
    searchPlaceholder: "Search keywords, authors, tags, summaries",
    field: "Field",
    tagSubtopic: "Tag/Subtopic",
    venue: "Venue",
    year: "Year",
    sort: "Sort",
    all: "All",
    newest: "Newest",
    relevance: "Relevance",
    title: "Title",
    venuesTitle: "Key Venues",
    allVenues: "All venues",
    papersByField: "Papers by Field",
    curatedPapers: "Curated Papers",
    emptyTitle: "No papers to display.",
    emptyText: "Adjust the search or filters, or run the GitHub Actions update.",
    footer:
      "Metadata from OpenAlex, Crossref, and optionally Semantic Scholar. Summaries are generated and do not reproduce publisher abstracts.",
    papers: "papers",
    priority: "Core",
    others: "Others",
    lowCountVenue: "2 or fewer papers",
    showing: "papers shown",
    unknownYear: "Year unknown",
    relevanceLabel: "Relevance",
    summaryMissing: "Summary has not been generated yet.",
  },
};

const LABEL_TRANSLATIONS = {
  en: {
    "생산/제조": "Production / Manufacturing",
    "3D 프린팅": "3D Printing",
    "4D 프린팅": "4D Printing",
    "로봇틱스(생산제조)": "Robotics for Manufacturing",
    "AI 생산제조": "AI Manufacturing",
    "공정 최적화": "Process Optimization",
    "금속/합금 제조": "Metals/Alloys",
    "건설/대형 제조": "Construction/Large-scale",
    "복합재/소재 제조": "Composites/Materials",
    "툴패스": "Toolpath",
    "퍼지/재료전환": "Purge/Material Switching",
    "로봇 AM": "Robotic AM",
    "제조 자동화": "Manufacturing Automation",
    "경로계획": "Path Planning",
    "메타물질": "Metamaterials",
    "AI 공정제어": "AI Process Control",
    "설계 자동화": "Design Automation",
    "리뷰 및 서베이": "Reviews and Surveys",
    "다중재료 적층제조": "Multi-material AM",
    "기능성 구배 적층제조": "Functionally Graded AM",
    "계산설계": "Computational Design",
    "재료분포 최적화": "Material Distribution Optimization",
    "툴패스 계획": "Toolpath Planning",
    "재료 전환 / 퍼지 감소": "Material Switching / Purge Reduction",
    "그래프 탐색 / 경로 계획 알고리즘": "Graph Search / Path Planning",
    "적층제조를 위한 AI 및 머신러닝": "AI and ML for AM",
    "재료분포": "Material Distribution",
    "퍼지 감소": "Purge Reduction",
    "툴패스": "Toolpath",
    "툴패스 전략": "Toolpath Strategy",
    "경로계획": "Path Planning",
    "공정 최적화": "Process Optimization",
    "재료 전환": "Material Switching",
    "퍼지/재료전환": "Purge/Material Switching",
    "리뷰": "Review",
    "서베이": "Survey",
    "메타물질": "Metamaterials",
    "디지털 제작": "Digital Fabrication",
    "재료 거동": "Material Behavior",
  },
};

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

const DEFAULT_THEME = "dark";
const DEFAULT_LANGUAGE = "en";
const PREFERENCE_VERSION = "20260612-en-dark";

if (localStorage.getItem("preferenceVersion") !== PREFERENCE_VERSION) {
  localStorage.setItem("theme", DEFAULT_THEME);
  localStorage.setItem("language", DEFAULT_LANGUAGE);
  localStorage.setItem("preferenceVersion", PREFERENCE_VERSION);
}

const state = {
  papers: [],
  siteMeta: null,
  filtered: [],
  activeTopic: "",
  activeTargetVenue: "",
  activeVenueGroup: "",
  activeSubtopic: "",
  theme: localStorage.getItem("theme") || DEFAULT_THEME,
  language: localStorage.getItem("language") || DEFAULT_LANGUAGE,
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
  themeToggle: document.querySelector("#theme-toggle"),
  languageToggle: document.querySelector("#language-toggle"),
};

async function init() {
  setupPreferences();
  try {
    const response = await fetch(`data/papers.json?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.papers = await response.json();
  } catch (error) {
    console.error("Failed to load papers.json", error);
    state.papers = [];
  }
  try {
    const response = await fetch(`data/site_meta.json?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.siteMeta = await response.json();
  } catch (error) {
    console.warn("Failed to load site_meta.json", error);
    state.siteMeta = null;
  }

  buildFilters();
  buildTopicNav();
  buildVenueNav();
  buildSideNav();
  renderVenueBoard();
  updateStats();
  applyFilters();

  [els.search, els.category, els.tag, els.venue, els.year, els.sort].forEach((el) => {
    el.addEventListener("input", () => {
      if (el === els.category) state.activeSubtopic = "";
      if (el === els.venue) clearVenueQuickFilters();
      applyFilters();
    });
    el.addEventListener("change", () => {
      if (el === els.category) state.activeSubtopic = "";
      if (el === els.venue) clearVenueQuickFilters();
      applyFilters();
    });
  });
}

function setupPreferences() {
  applyPreferences();
  if (els.themeToggle) {
    els.themeToggle.addEventListener("click", () => {
      state.theme = state.theme === "dark" ? "light" : "dark";
      localStorage.setItem("theme", state.theme);
      applyPreferences();
    });
  }
  if (els.languageToggle) {
    els.languageToggle.addEventListener("click", () => {
      state.language = state.language === "ko" ? "en" : "ko";
      localStorage.setItem("language", state.language);
      applyPreferences();
      buildFiltersReset();
      buildTopicNavReset();
      buildVenueNavReset();
      buildSideNav();
      renderVenueBoard();
      updateStats();
      applyFilters();
    });
  }
  window.setInterval(() => {
    updateStats();
  }, 60000);
}

function applyPreferences() {
  document.documentElement.dataset.theme = state.theme;
  document.documentElement.lang = state.language === "ko" ? "ko" : "en";
  if (els.themeToggle) {
    els.themeToggle.textContent = state.theme === "dark" ? t("themeLight") : t("themeDark");
  }
  if (els.languageToggle) {
    els.languageToggle.textContent = t("langToggle");
  }
  applyStaticLanguage();
}

function applyStaticLanguage() {
  setText(".subtitle", t("subtitle"));
  setText(".notice", t("noticeMain"));
  setText(".notice-soft", t("noticeSoft"));
  setText(".sidebar strong", t("sideTitle"));
  setText(".stats article:nth-child(1) strong", t("totalPapers"));
  setText(".stats article:nth-child(2) strong", t("subtopicCount"));
  setText(".stats article:nth-child(3) strong", t("latestUpdate"));
  setText(".stats article:nth-child(4) strong", t("weekAdded"));
  setText(".controls label:nth-child(1) span", t("search"));
  setText(".controls label:nth-child(2) span", t("field"));
  setText(".controls label:nth-child(3) span", t("tagSubtopic"));
  setText(".controls label:nth-child(4) span", t("venue"));
  setText(".controls label:nth-child(5) span", t("year"));
  setText(".controls label:nth-child(6) span", t("sort"));
  setText("#category-filter option[value='']", t("all"));
  setText("#tag-filter option[value='']", t("all"));
  setText("#venue-filter option[value='']", t("all"));
  setText("#year-filter option[value='']", t("all"));
  setText("#sort-select option[value='newest']", t("newest"));
  setText("#sort-select option[value='relevance']", t("relevance"));
  setText("#sort-select option[value='title']", t("title"));
  setText(".venue-section-head h2", t("venuesTitle"));
  setText(".results-head .section-kicker", t("papersByField"));
  setText(".results-head h2", t("curatedPapers"));
  setText("#empty-state strong", t("emptyTitle"));
  setText("#empty-state p", t("emptyText"));
  setText(".site-footer p", t("footer"));
  if (els.search) {
    els.search.placeholder = t("searchPlaceholder");
  }
}

function buildFiltersReset() {
  resetSelect(els.category, t("all"));
  resetSelect(els.tag, t("all"));
  resetSelect(els.venue, t("all"));
  resetSelect(els.year, t("all"));
  buildFilters();
}

function buildTopicNavReset() {
  els.topicNav.innerHTML = `<button type="button" class="topic-pill is-active" data-topic="">All</button>`;
  buildTopicNav();
}

function buildVenueNavReset() {
  els.venueNav.innerHTML = `<button type="button" class="venue-pill is-active" data-target-venue="">${escapeHtml(t("allVenues"))}</button>`;
  buildVenueNav();
}

function buildFilters() {
  const fields = new Set();
  const tags = new Set();
  const venues = new Set();
  const years = new Set();

  state.papers.forEach((paper) => {
    fields.add(deriveField(paper));
    visibleTags(paper).forEach((tag) => tags.add(tag));
    deriveSubtopics(paper).forEach((subtopic) => tags.add(subtopic));
    venues.add(normalizeVenue(paper.venue));
    if (paper.year) years.add(String(paper.year));
  });

  FIELD_ORDER.forEach((field) => {
    if (fields.has(field)) {
      els.category.append(new Option(displayLabel(field), field));
    }
  });
  [...fields]
    .filter((field) => !FIELD_ORDER.includes(field))
    .sort((a, b) => a.localeCompare(b, "ko"))
    .forEach((field) => {
      els.category.append(new Option(displayLabel(field), field));
    });

  [...tags].sort((a, b) => a.localeCompare(b, "ko")).forEach((tag) => {
    els.tag.append(new Option(displayLabel(tag), tag));
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
  const availableSubtopics = new Set(flatten(state.papers.map((paper) => deriveSubtopics(paper))));
  const topics = FEATURED_TOPICS.filter(
    (topic) => availableTags.has(topic) || availableCategories.has(topic) || availableSubtopics.has(topic)
  );

  topics.forEach((topic) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "topic-pill";
    button.dataset.topic = topic;
    button.textContent = displayLabel(topic);
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
    if (count === 0) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "venue-pill";
    button.dataset.targetVenue = venue;
    button.innerHTML = `${escapeHtml(shortVenue(venue))} <span>${count}</span>`;
    button.title = `${venue} 논문만 보기`;
    els.venueNav.append(button);
  });

  els.venueNav.addEventListener("click", (event) => {
    const button = event.target.closest("[data-target-venue]");
    if (!button) return;
    state.activeTargetVenue = button.dataset.targetVenue;
    state.activeVenueGroup = "";
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
  const fieldCounts = countBy(state.papers, deriveField);
  els.sideTopicNav.innerHTML = FIELD_ORDER.filter((field) => fieldCounts.get(field))
    .map((field) => {
      const subtopics = FIELD_SUBTOPICS[field] || [];
      const fieldPapers = state.papers.filter((paper) => deriveField(paper) === field);
      const bucketCounts = sidebarBucketCounts(fieldPapers, subtopics);
      const subtopicButtons = [...subtopics, SIDEBAR_OTHER_TOPIC]
        .map((subtopic) => sideSubtopicButton(field, subtopic, bucketCounts.get(subtopic) || 0))
        .join("");
      return `<div class="side-field-group">
        <button class="side-field" type="button" data-side-field="${escapeAttribute(field)}">
          <span class="side-label">${escapeHtml(displayLabel(field))}</span>
          <span class="side-count">${fieldCounts.get(field)}</span>
        </button>
        <div class="side-subtopics">${subtopicButtons}</div>
      </div>`;
    })
    .join("");

  els.sideTopicNav.querySelectorAll("[data-side-field]").forEach((button) => {
    button.addEventListener("click", () => {
      const field = button.dataset.sideField;
      const subtopic = button.dataset.sideSubtopic || "";
      els.category.value = field;
      state.activeSubtopic = subtopic;
      syncSideNavActive();
      applyFilters();
      scrollToPapers();
    });
  });
}

function sidebarBucketCounts(papers, subtopics) {
  const counts = new Map(subtopics.map((subtopic) => [subtopic, 0]));
  counts.set(SIDEBAR_OTHER_TOPIC, 0);

  papers.forEach((paper) => {
    const bucket = sidebarBucketForPaper(paper, subtopics);
    counts.set(bucket, (counts.get(bucket) || 0) + 1);
  });

  return counts;
}

function sidebarBucketForPaper(paper, subtopics) {
  return subtopics.find((subtopic) => paperHasRepresentativeTopic(paper, subtopic)) || SIDEBAR_OTHER_TOPIC;
}

function sideSubtopicButton(field, subtopic, count) {
  const isOther = subtopic === SIDEBAR_OTHER_TOPIC;
  const label = isOther ? t("others") : displayLabel(subtopic);
  const disabled = count ? "" : " disabled";
  return `<button class="side-subtopic${count ? "" : " is-empty"}" type="button" data-side-field="${escapeAttribute(field)}" data-side-subtopic="${escapeAttribute(subtopic)}"${disabled}>
    <span class="side-label">${escapeHtml(label)}</span>
    <span class="side-count">${count}</span>
  </button>`;
}

function syncSideNavActive() {
  els.sideTopicNav.querySelectorAll("[data-side-field]").forEach((button) => {
    const fieldMatches = button.dataset.sideField === els.category.value;
    const subtopicMatches = (button.dataset.sideSubtopic || "") === state.activeSubtopic;
    const isFieldButton = !button.dataset.sideSubtopic;
    button.classList.toggle("is-active", fieldMatches && (isFieldButton ? !state.activeSubtopic : subtopicMatches));
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
  const priorityEntries = TARGET_VENUES.map((target) => {
    const matched = entries.find(([venue]) => matchesTargetVenue(venue, target));
    return matched || [target, 0];
  }).filter(([, count]) => count > 0);
  const discoveredEntries = entries.filter(
    ([venue, count]) => count >= 2 && !isPriorityVenue(venue) && !isNonJournalVenue(venue)
  );
  const visibleVenueKeys = new Set(
    [...priorityEntries, ...discoveredEntries].map(([venue]) => normalizeVenueKey(venue))
  );
  const hiddenEntries = entries.filter(([venue]) => !visibleVenueKeys.has(normalizeVenueKey(venue)));
  const hiddenPaperCount = hiddenEntries.reduce((sum, [, count]) => sum + count, 0);

  const mainCards = [
    `<button class="venue-card is-all is-active" type="button" data-board-venue="">
      <strong>${escapeHtml(t("allVenues"))}</strong>
      <span>${state.papers.length} ${escapeHtml(t("papers"))}</span>
    </button>`,
    ...priorityEntries.map(([venue, count]) => venueCard(venue, count, t("priority"))),
    ...discoveredEntries.map(([venue, count]) => venueCard(venue, count)),
    hiddenPaperCount ? otherVenueCard(hiddenPaperCount, hiddenEntries.length) : "",
  ].join("");

  els.venueBoard.innerHTML = `
    <div class="venue-featured">${mainCards}</div>
  `;

  els.venueBoard.querySelectorAll("[data-board-venue]").forEach((button) => {
    button.addEventListener("click", () => {
      const venue = button.dataset.boardVenue;
      state.activeVenueGroup = button.dataset.boardVenueGroup || "";
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
        const sameVenue = card.dataset.boardVenue === venue;
        const sameGroup = (card.dataset.boardVenueGroup || "") === state.activeVenueGroup;
        card.classList.toggle("is-active", sameVenue && sameGroup);
      });
      applyFilters();
      scrollToPapers();
    });
  });
}

function clearVenueQuickFilters() {
  state.activeTargetVenue = "";
  state.activeVenueGroup = "";
  els.venueNav.querySelectorAll(".venue-pill").forEach((pill) => {
    pill.classList.toggle("is-active", !pill.dataset.targetVenue);
  });
  els.venueBoard.querySelectorAll(".venue-card").forEach((card) => {
    card.classList.toggle("is-active", !card.dataset.boardVenue && !card.dataset.boardVenueGroup);
  });
}

function isNonJournalVenue(venue) {
  const key = normalizeVenueKey(venue);
  return hasAny(key, [
    "unknown",
    "arxiv",
    "research square",
    "chemrxiv",
    "dissertation",
    "vtechworks",
    "osti",
    "shareok",
    "proceedings",
    "repository",
  ]);
}

function venueCard(venue, count, label = "") {
  const badge = label ? `<em class="venue-chip">${escapeHtml(label)}</em>` : "";
  return `<button class="venue-card" type="button" data-board-venue="${escapeAttribute(venue)}">
    <strong>${escapeHtml(shortVenue(venue))}</strong>
    <span><b>${count}</b> ${escapeHtml(t("papers"))}</span>
    ${badge}
  </button>`;
}

function otherVenueCard(paperCount, venueCount) {
  return `<button class="venue-card venue-card-muted" type="button" data-board-venue="" data-board-venue-group="other">
    <strong>${escapeHtml(t("others"))}</strong>
    <span><b>${paperCount}</b> ${escapeHtml(t("papers"))} · ${venueCount} venues</span>
    <em class="venue-chip">${escapeHtml(t("lowCountVenue"))}</em>
  </button>`;
}

function updateStats() {
  const subtopics = new Set(flatten(state.papers.map((paper) => deriveSubtopics(paper))));
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
  els.categories.textContent = subtopics.size.toLocaleString("ko-KR");
  const lastRunAt = state.siteMeta && state.siteMeta.last_run_at_utc;
  renderUpdatedStat(lastRunAt, latestDate);
  els.week.textContent = weekCount.toLocaleString("ko-KR");
}

function renderUpdatedStat(lastRunAt, fallbackDate) {
  const now = formatRunTime(new Date().toISOString());
  const lastRun = formatRunTime(lastRunAt);
  els.updated.classList.add("stat-datetime");
  if (!now) {
    els.updated.textContent = fallbackDate || "-";
    return;
  }
  const updatedText = lastRun
    ? state.language === "ko"
      ? `수집 ${lastRun.time} KST`
      : `Updated ${lastRun.time} KST`
    : fallbackDate || "";
  els.updated.innerHTML = `${escapeHtml(now.date)}<small>${escapeHtml(now.time)} KST${updatedText ? ` · ${escapeHtml(updatedText)}` : ""}</small>`;
}

function applyFilters() {
  const query = normalize(els.search.value);
  const category = els.category.value;
  const tag = els.tag.value;
  const venue = els.venue.value;
  const year = els.year.value;
  const sort = els.sort.value;

  if (!category) state.activeSubtopic = "";
  syncSideNavActive();

  state.filtered = state.papers.filter((paper) => {
    const paperCategories = paper.categories || [];
    const paperTags = paper.tags || [];
    const paperVisibleTags = visibleTags(paper);
    const paperSubtopics = deriveSubtopics(paper);
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
        paperSubtopics.join(" "),
        paper.ai_summary_ko,
        paper.relevance_note_ko,
      ].join(" ")
    );

    const matchesQuery = !query || haystack.includes(query);
    const matchesCategory = !category || paperField === category;
    const matchesTag = !tag || paperTags.includes(tag) || paperVisibleTags.includes(tag) || paperSubtopics.includes(tag);
    const matchesVenue = !venue || paperVenue === venue;
    const matchesTarget = !state.activeTargetVenue || matchesTargetVenue(paperVenue, state.activeTargetVenue);
    const matchesVenueGroup = !state.activeVenueGroup || isOtherVenuePaper(paper);
    const matchesTopic =
      !state.activeTopic ||
      paperTags.includes(state.activeTopic) ||
      paperCategories.includes(state.activeTopic) ||
      paperSubtopics.includes(state.activeTopic);
    const matchesSubtopic = !state.activeSubtopic || paperMatchesSidebarSubtopic(paper, paperField, state.activeSubtopic);
    const matchesYear = !year || String(paper.year || "") === year;
    return (
      matchesQuery &&
      matchesCategory &&
      matchesTag &&
      matchesVenue &&
      matchesTarget &&
      matchesVenueGroup &&
      matchesTopic &&
      matchesSubtopic &&
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

function isOtherVenuePaper(paper) {
  const venue = normalizeVenue(paper.venue);
  const count = state.papers.filter((item) => normalizeVenueKey(item.venue) === normalizeVenueKey(venue)).length;
  return count < 2 || isNonJournalVenue(venue);
}

function render() {
  els.count.textContent =
    state.language === "ko"
      ? `${state.filtered.length.toLocaleString("ko-KR")}${t("showing")}`
      : `${state.filtered.length.toLocaleString("en-US")} ${t("showing")}`;
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
        <h3>${escapeHtml(displayLabel(category))}</h3>
      <span>${papers.length.toLocaleString(state.language === "ko" ? "ko-KR" : "en-US")} ${escapeHtml(t("papers"))}</span>
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
  const publicationLabel = formatPublicationLabel(paper);
  const summaryText = formatSummary(paper);
  const relevanceNote = formatRelevanceNote(paper);
  const representativeBadges = representativeTags(paper)
    .map((tag) => badge(displayLabel(tag), "tag"))
    .join("");

  article.innerHTML = `
    <div class="card-content">
      <div class="card-topline">
        <span class="publication-badge">${escapeHtml(publicationLabel)}</span>
        <span>${escapeHtml(t("relevanceLabel"))} ${escapeHtml(String(paper.relevance_score || "-"))}/10</span>
      </div>
      <h4 class="paper-title">${escapeHtml(paper.title || "Untitled")}</h4>
      <p class="meta">${escapeHtml(authors)}${authors ? " · " : ""}${escapeHtml(paper.venue || "Venue unknown")} · ${escapeHtml(sourceText)}</p>
      <p class="summary">${escapeHtml(summaryText)}</p>
      <p class="relevance-note">${escapeHtml(relevanceNote)}</p>
      <div class="tag-line">${representativeBadges}</div>
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

function formatSummary(paper) {
  if (state.language !== "en") {
    return paper.ai_summary_ko || t("summaryMissing");
  }

  const yearPhrase = paper.year ? `${paper.year}` : "undated";
  const venue = paper.venue || "an unknown venue";
  const tags = representativeTags(paper).map((tag) => displayLabel(tag));
  const tagPhrase = formatEnglishList(tags);
  const score = paper.relevance_score ? `${paper.relevance_score}/10` : "not yet scored";
  const title = paper.title || "This work";

  return `${title} is tracked as a ${yearPhrase} paper from ${venue} related to ${tagPhrase || "manufacturing research"}. Based on public metadata and curated topic signals, its current relevance score for this tracker is ${score}.`;
}

function formatRelevanceNote(paper) {
  if (state.language !== "en") {
    return paper.relevance_note_ko || "";
  }

  const tags = representativeTags(paper).map((tag) => displayLabel(tag));
  const tagPhrase = formatEnglishList(tags);
  const score = paper.relevance_score ? `${paper.relevance_score}/10` : "pending";
  return `Relevant to the tracker through ${tagPhrase || "its manufacturing and design metadata"}; score: ${score}.`;
}

function formatEnglishList(items) {
  const clean = items.filter(Boolean);
  if (!clean.length) return "";
  if (clean.length === 1) return clean[0];
  if (clean.length === 2) return `${clean[0]} and ${clean[1]}`;
  return `${clean.slice(0, -1).join(", ")}, and ${clean[clean.length - 1]}`;
}

function representativeTags(paper) {
  const candidates = [...deriveSubtopics(paper), ...visibleTags(paper)];
  if (candidates.length < 3) {
    candidates.push(...(paper.categories || []));
  }

  const seen = new Set();
  const picked = [];
  candidates.forEach((tag) => {
    const canonical = canonicalTopicLabel(tag);
    const key = normalizeTopicKey(canonical);
    if (!canonical || seen.has(key)) return;
    seen.add(key);
    picked.push(canonical);
  });

  return collapseMaterialExtrusionTags(picked, paper).slice(0, 3);
}

function paperMatchesSidebarSubtopic(paper, field, topic) {
  if (!topic) return true;
  const subtopics = FIELD_SUBTOPICS[field] || [];
  if (topic === SIDEBAR_OTHER_TOPIC) {
    return sidebarBucketForPaper(paper, subtopics) === SIDEBAR_OTHER_TOPIC;
  }
  return paperHasRepresentativeTopic(paper, topic);
}

function paperHasRepresentativeTopic(paper, topic) {
  const target = normalizeTopicKey(canonicalTopicLabel(topic));
  return representativeTags(paper).some((tag) => normalizeTopicKey(canonicalTopicLabel(tag)) === target);
}

function collapseMaterialExtrusionTags(tags, paper) {
  const cluster = ["DM filament", "FGAM", "MMAM", "FDM/Material extrusion"];
  const present = cluster.filter((tag) => tags.includes(tag));
  if (!present.length) return tags;

  const text = normalize(
    [
      paper.title,
      paper.venue,
      (paper.tags || []).join(" "),
      (paper.categories || []).join(" "),
      paper.ai_summary_ko,
      paper.relevance_note_ko,
    ].join(" ")
  );

  let selected = present[0];
  if (hasAny(text, ["dm filament", "digital material filament", "digital material", "blended fdm"])) {
    selected = "DM filament";
  } else if (hasAny(text, ["functionally graded", "functional gradient", "graded material", "fgam", "gradient", "graded"])) {
    selected = "FGAM";
  } else if (hasAny(text, ["multi-material", "multi material", "multimaterial", "mmam"])) {
    selected = "MMAM";
  } else if (hasAny(text, ["fdm", "fused deposition", "material extrusion", "filament"])) {
    selected = "FDM/Material extrusion";
  }

  if (!selected) return tags;
  return [selected, ...tags.filter((tag) => !cluster.includes(tag))];
}

function canonicalTopicLabel(tag) {
  const value = String(tag || "").trim();
  const text = normalize(value);
  if (!value) return "";
  if (hasAny(text, ["multi-material", "multi material", "multimaterial", "mmam", "다중재료", "다중 재료"])) return "MMAM";
  if (hasAny(text, ["functionally graded", "functional gradient", "graded material", "fgam", "기능성 구배", "구배"])) return "FGAM";
  if (hasAny(text, ["dm filament", "digital material", "blended fdm"])) return "DM filament";
  if (hasAny(text, ["fdm", "fused deposition", "material extrusion"])) return "FDM/Material extrusion";
  if (hasAny(text, ["dlp", "digital light processing", "vat photopolymerization", "vat photopolymerisation", "stereolithography", "sla"])) return "DLP";
  if (hasAny(text, ["lce", "liquid crystal elastomer", "liquid-crystal elastomer"])) return "LCE";
  if (hasAny(text, ["metamaterial", "metamaterials", "mechanical metamaterial", "메타물질"])) return "메타물질";
  if (hasAny(text, ["4d printing", "4d printed", "4d-printed", "4d print", "4d 프린팅"])) return "4D printing";
  if (hasAny(text, ["toolpath", "툴패스", "툴패스 전략"])) return "Toolpath";
  if (hasAny(text, ["path planning", "trajectory", "graph search", "경로계획", "경로 계획", "그래프 탐색"])) return "Path Planning";
  if (hasAny(text, ["process optimization", "process optimisation", "parameter optimization", "parameter optimisation", "공정 최적화"])) return "Process Optimization";
  if (hasAny(text, ["manufacturing automation", "automation", "automated", "제조 자동화"])) return "Manufacturing Automation";
  if (hasAny(text, ["design automation", "computational design", "generative design", "topology optimization", "계산설계", "설계 자동화"])) return "Design Automation";
  if (hasAny(text, ["machine learning", "deep learning", "reinforcement learning", "ai/ml", "머신러닝", "인공지능"])) return "AI/ML";
  if (hasAny(text, ["review", "survey", "리뷰", "서베이"])) return "Review";
  if (hasAny(text, ["material distribution", "재료분포", "재료 분포"])) return "Material Distribution";
  if (hasAny(text, ["material switching", "purge", "재료 전환", "퍼지"])) return "Material Switching";
  return value;
}

function normalizeTopicKey(tag) {
  return normalize(tag).replace(/[^a-z0-9가-힣]+/g, "");
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

function formatPublicationLabel(paper) {
  const year = paper.year ? String(paper.year) : "";
  const venue = normalizeVenue(paper.venue);
  const compactVenue = shortVenue(venue);
  if (!compactVenue || compactVenue === "Venue unknown") {
    return year ? `Venue unknown ${year}` : "Venue unknown";
  }
  return year ? `${compactVenue} ${year}` : compactVenue;
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
  const titleText = normalize([paper.title, paper.venue, (paper.tags || []).join(" ")].join(" "));
  const categoryText = normalize((paper.categories || []).join(" "));
  const text = `${titleText} ${categoryText}`;

  if (
    titleText.includes("4d printing") ||
    titleText.includes("4d printed") ||
    titleText.includes("4d-printed") ||
    titleText.includes("4d print") ||
    titleText.includes("lce") ||
    titleText.includes("liquid crystal elastomer") ||
    titleText.includes("metamaterial") ||
    titleText.includes("4d 프린팅")
  ) {
    return "4D 프린팅";
  }
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
    titleText.includes("digital light processing") ||
    titleText.includes("dlp") ||
    titleText.includes("vat photopolymerization") ||
    titleText.includes("vat photopolymerisation") ||
    titleText.includes("stereolithography") ||
    titleText.includes("sla") ||
    titleText.includes("additive manufacturing") ||
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

function deriveSubtopics(paper) {
  const text = normalize(
    [
      paper.title,
      paper.venue,
      (paper.tags || []).join(" "),
      (paper.categories || []).join(" "),
      paper.ai_summary_ko,
      paper.relevance_note_ko,
    ].join(" ")
  );
  const subtopics = new Set();

  if (hasAny(text, ["process", "parameter", "optimization", "공정", "최적화"])) subtopics.add("공정 최적화");
  if (hasAny(text, ["metal", "metals", "alloy", "steel", "inconel", "ss316", "금속", "합금"])) subtopics.add("금속/합금 제조");
  if (hasAny(text, ["construction", "large-scale", "concrete", "building", "건설", "대형"])) subtopics.add("건설/대형 제조");
  if (hasAny(text, ["composite", "fiber", "polymer", "복합재", "섬유", "고분자"])) subtopics.add("복합재/소재 제조");

  if (hasAny(text, ["multi-material", "multimaterial", "mmam", "multi material", "다중재료"])) subtopics.add("MMAM");
  if (hasAny(text, ["functionally graded", "fgam", "graded", "gradient", "기능성 구배", "구배"])) subtopics.add("FGAM");
  if (hasAny(text, ["dm filament", "digital material", "blended fdm", "디지털 재료"])) subtopics.add("DM filament");
  if (hasAny(text, ["fdm", "fused deposition", "material extrusion", "filament", "압출"])) subtopics.add("FDM/Material extrusion");
  if (hasAny(text, ["dlp", "digital light processing", "vat photopolymerization", "vat photopolymerisation", "stereolithography", "sla"])) subtopics.add("DLP");
  if (hasAny(text, ["toolpath", "path planning", "graph search", "trajectory", "툴패스", "경로계획", "경로 계획"])) subtopics.add("툴패스");
  if (hasAny(text, ["purge", "switching", "transition", "waste", "퍼지", "재료 전환", "전환"])) subtopics.add("퍼지/재료전환");

  if (hasAny(text, ["4d printing", "4d printed", "4d-printed", "4d print", "4d 프린팅"])) subtopics.add("4D printing");
  if (hasAny(text, ["lce", "liquid crystal elastomer", "liquid-crystal elastomer"])) subtopics.add("LCE");
  if (hasAny(text, ["metamaterial", "metamaterials", "mechanical metamaterial", "메타물질"])) subtopics.add("메타물질");
  if (hasAny(text, ["active material", "active materials", "actuator", "actuation", "액추에이터", "능동 재료"])) subtopics.add("Active materials");
  if (hasAny(text, ["shape morph", "morphing", "shape change", "shape-changing", "형상 변화", "변형"])) subtopics.add("Shape morphing");
  if (hasAny(text, ["stimuli", "stimulus", "responsive", "temperature-responsive", "자극 반응", "반응형"])) subtopics.add("Stimuli-responsive");

  if (hasAny(text, ["robot", "robotic", "로봇"])) subtopics.add("로봇 AM");
  if (hasAny(text, ["automation", "automated", "자동화"])) subtopics.add("제조 자동화");
  if (hasAny(text, ["path planning", "graph search", "trajectory", "경로계획", "경로 계획"])) subtopics.add("경로계획");

  if (hasAny(text, ["machine learning", "ml", "머신러닝"])) subtopics.add("Machine Learning");
  if (hasAny(text, ["deep learning", "neural", "딥러닝"])) subtopics.add("Deep Learning");
  if (hasAny(text, ["reinforcement learning", "강화학습"])) subtopics.add("Reinforcement Learning");
  if (hasAny(text, ["process control", "monitoring", "closed-loop", "공정제어", "모니터링"])) subtopics.add("AI 공정제어");
  if (hasAny(text, ["computational design", "generative design", "topology optimization", "design automation", "계산설계", "설계 자동화"])) {
    subtopics.add("설계 자동화");
  }

  return [...subtopics];
}

function hasAny(text, terms) {
  return terms.some((term) => text.includes(normalize(term)));
}

function countBy(items, mapper) {
  const counts = new Map();
  items.forEach((item) => {
    const key = mapper(item);
    counts.set(key, (counts.get(key) || 0) + 1);
  });
  return counts;
}

function scrollToPapers() {
  const paperList = document.querySelector("#paper-list");
  if (paperList) {
    paperList.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function t(key) {
  const table = UI_TEXT[state.language] || UI_TEXT.ko;
  return table[key] || UI_TEXT.ko[key] || key;
}

function displayLabel(value) {
  if (state.language === "ko") return value;
  return (LABEL_TRANSLATIONS.en && LABEL_TRANSLATIONS.en[value]) || value;
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) {
    node.textContent = value;
  }
}

function resetSelect(select, defaultLabel) {
  if (!select) return;
  select.innerHTML = "";
  select.append(new Option(defaultLabel, ""));
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
    "arXiv (Cornell University)": "arXiv",
    "ArXiv.org": "arXiv",
    "International Conference on Learning Representations": "ICLR",
    "The International Conference on Learning Representations": "ICLR",
    "International Conference on Machine Learning": "ICML",
    "International Conference on Machine Learning (ICML)": "ICML",
    "Neural Information Processing Systems": "NeurIPS",
    "Advances in Neural Information Processing Systems": "NeurIPS",
    "Conference on Neural Information Processing Systems": "NeurIPS",
    "Computer Vision and Pattern Recognition": "CVPR",
    "IEEE/CVF Conference on Computer Vision and Pattern Recognition": "CVPR",
    "International Conference on Robotics and Automation": "ICRA",
    "IEEE International Conference on Robotics and Automation": "ICRA",
    "IEEE/RSJ International Conference on Intelligent Robots and Systems": "IROS",
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
  if (replacements[venue]) return replacements[venue];

  const lower = normalize(venue);
  if (lower.includes("arxiv")) return "arXiv";
  if (lower.includes("learning representations") || lower.includes("iclr")) return "ICLR";
  if (lower.includes("international conference on machine learning") || lower.includes("icml")) return "ICML";
  if (lower.includes("neural information processing systems") || lower.includes("neurips")) return "NeurIPS";
  if (lower.includes("computer vision and pattern recognition") || lower.includes("cvpr")) return "CVPR";
  if (lower.includes("international conference on robotics and automation") || lower.includes("icra")) return "ICRA";
  if (lower.includes("intelligent robots and systems") || lower.includes("iros")) return "IROS";
  if (lower === "additive manufacturing") return "Addit. Manuf.";
  if (lower === "nature communications") return "Nat. Commun.";
  if (lower === "science advances") return "Sci. Adv.";
  return venue;
}

function normalize(value) {
  return String(value || "").toLowerCase().trim();
}

function dateValue(value) {
  return value ? new Date(`${value}T00:00:00`).getTime() : 0;
}

function formatRunTime(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const parts = new Intl.DateTimeFormat("ko-KR", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const byType = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return {
    date: `${byType.year}-${byType.month}-${byType.day}`,
    time: `${byType.hour}:${byType.minute}`,
  };
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
