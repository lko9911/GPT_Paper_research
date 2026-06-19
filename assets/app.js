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
  "생산/제조": ["복합재/소재 제조", "공정 최적화"],
  "3D 프린팅": ["MMAM", "FGAM", "Volumetric AM", "DLP", "SLA", "Vat photopolymerization", "FDM/Material extrusion", "Toolpath", "Material Switching", "Additive manufacturing"],
  "4D 프린팅": ["LCE", "메타물질", "Active materials"],
  "로봇틱스(생산제조)": ["Soft robotics", "제조 자동화", "Robot-based Manufacturing"],
  "AI 생산제조": ["Self-driving Labs", "Digital Twins", "Machine Learning", "Design Automation", "제조 자동화"],
};

const SIDEBAR_OTHER_TOPIC = "__field_other__";

const LOW_SIGNAL_CARD_TAGS = new Set([
  "Additive manufacturing",
  "Review",
  "Sustainability",
  "Digital fabrication",
  "Material behavior",
  "Reusability",
]);

const CARD_TAG_PRIORITY = new Map([
  ["MMAM", 1],
  ["FGAM", 1],
  ["Volumetric AM", 1],
  ["Soft robotics", 1],
  ["LCE", 1],
  ["Digital Twins", 1],
  ["Self-driving Labs", 1],
  ["Toolpath strategy", 2],
  ["Material switching", 2],
  ["FDM/Material extrusion", 2],
  ["DLP", 2],
  ["SLA", 2],
  ["Vat photopolymerization", 2],
  ["Robot-based Manufacturing", 2],
  ["Manufacturing automation", 2],
  ["Machine learning", 2],
  ["Design automation", 2],
  ["Metamaterials", 2],
  ["Active materials", 2],
  ["Process optimization", 3],
  ["Composites/Materials", 3],
]);

const TARGET_VENUES = [
  "Nature",
  "Nature Communications",
  "Nature Materials",
  "Nature Reviews Materials",
  "Science",
  "Science Advances",
  "Science Robotics",
  "Additive Manufacturing",
  "ACS Applied Materials & Interfaces",
  "Materials & Design",
];

const UI_TEXT = {

  en: {
    themeDark: "Dark",
    themeLight: "Light",
    heroStatusLoading: "Loading curated papers...",
    heroStatus:
      "{papers} curated papers - {venues} venues - {years} - updated {updated} KST",
    subtitle: "An AI-assisted research tracker for manufacturing, 3D/4D printing, robotics, and AI-driven production.",
    noticeMain: "This repository provides DOI links and AI-generated summaries only. It does not host copyrighted PDFs or publisher abstract text.",
    noticeSoft:
      "Summaries on this site are newly written AI summaries based on public paper metadata and abstracts. Check the DOI link for the original and authoritative content.",
    sideTitle: "Fields and Subtopics",
    totalPapers: "Papers",
    latestRunAdded: "this update",
    weeklyAddedShort: "weekly new",
    venueCount: "Venues",
    yearRange: "Years",
    currentUpdate: "Now / Updated",
    subtopicCount: "Collected Candidates",
    latestUpdate: "Last Collection",
    weekAdded: "Hidden Candidates",
    search: "Search",
    searchPlaceholder: "Search keywords, authors, tags, summaries",
    field: "Field",
    tagSubtopic: "Tag/Subtopic",
    venue: "Venue",
    summaryProvider: "Summary type",
    year: "Year",
    sort: "Sort",
    all: "All",
    allSummaries: "All",
    newest: "Newest",
    relevance: "Relevance",
    title: "Title",
    resetFilters: "Reset",
    venuesTitle: "Venues",
    allVenues: "All venues",
    papersByField: "Papers by Field",
    curatedPapers: "Curated Papers",
    emptyTitle: "No papers to display.",
    emptyText: "Adjust the search or filters, or run the GitHub Actions update.",
    footer:
      "Metadata from OpenAlex, Crossref, and optionally Semantic Scholar. Summaries are generated and do not reproduce publisher abstracts.",
    contactLabel: "Contact",
    papers: "papers",
    priority: "Core",
    others: "Others",
    lowCountVenue: "Non-core",
    showing: "curated results",
    unknownYear: "Year unknown",
    relevanceLabel: "Relevance",
    openaiApplied: "AI summary",
    openaiNotApplied: "Metadata summary",
    openaiAppliedTitle: "This summary was generated with the OpenAI API.",
    openaiNotAppliedTitle: "This summary was written without the OpenAI API, using title, abstract-availability, DOI, and public metadata signals.",
    fallbackSummary: "Metadata-based summary",
    summaryMissing: "Summary has not been generated yet.",
    authorsLabel: "Authors",
    correspondingAuthorsLabel: "Corresponding authors",
    correspondingAuthorBadge: "Corresponding",
    openPaper: "Open Paper",
    doiButton: "DOI",
    copyCitation: "Copy Cite",
    copiedCitation: "Copied",
    summaryQuestions: [
      "Topic",
      "Problem",
      "Method",
      "Key Result",
      "Takeaway",
    ],
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
    "건설/대형 제조": "Construction/Large-scale",
    "복합재/소재 제조": "Composites/Materials",
    "툴패스": "Toolpath",
    "퍼지/재료전환": "Purge/Material Switching",
    "제조 자동화": "Manufacturing Automation",
    "경로계획": "Path Planning",
    "메타물질": "Metamaterials",
    "AI 공정제어": "AI Process Control",
    "디지털 트윈": "Digital Twins",
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

const TAG_LABELS = {

  en: {
    "Additive manufacturing": "Additive Manufacturing",
    "Volumetric AM": "Volumetric AM",
    "Soft robotics": "Soft Robotics",
    MMAM: "Multi-material AM",
    FGAM: "Functionally Graded AM",
    "DM filament": "DM Filament",
    "FDM/Material extrusion": "FDM",
    DLP: "Digital Light Processing (DLP)",
    SLA: "Stereolithography (SLA)",
    "Vat photopolymerization": "Vat Photopolymerization",
    LCE: "LCE",
    "4D printing": "4D Printing",
    Metamaterials: "Metamaterials",
    "Active materials": "Active Materials",
    "Digital fabrication": "Digital Fabrication",
    "Toolpath strategy": "Toolpath Strategy",
    "Material behavior": "Material Behavior",
    "Computational design": "Computational Design",
    "Material distribution": "Material Distribution",
    "Material switching": "Material Switching",
    "Path planning": "Path Planning",
    "Process optimization": "Process Optimization",
    "Manufacturing automation": "Manufacturing Automation",
    "Self-driving Labs": "Self-driving Labs",
    "Digital Twins": "Digital Twins",
    "Robotic autonomous experimentation": "Self-driving Labs",
    "Design automation": "Design Automation",
    "Machine learning": "Machine Learning",
    "Robot-based Manufacturing": "Robot-based Manufacturing",
    "Composites/Materials": "Composites/Materials",
    Sustainability: "Sustainability",
    "Material property control": "Material Property Control",
    "Micro/Nano manufacturing": "Micro/Nano Manufacturing",
    "Shape morphing": "Shape Morphing",
    "Stimuli-responsive": "Stimuli-responsive",
    "Deep Learning": "Deep Learning",
    "Reinforcement Learning": "Reinforcement Learning",
    "AI Process Control": "AI Process Control",
    Honeycomb: "Honeycomb",
    "Energy absorption": "Energy Absorption",
    Reusability: "Reusability",
  },
};

const TAG_CATEGORY_ALIASES = {
  "Toolpath strategy": "툴패스 계획",
  "Path planning": "그래프 탐색 / 경로 계획 알고리즘",
  "Material distribution": "재료분포 최적화",
  "Material switching": "재료 전환 / 퍼지 감소",
  "Computational design": "계산설계",
  MMAM: "다중재료 적층제조",
  FGAM: "기능성 구배 적층제조",
  "Machine learning": "적층제조를 위한 AI 및 머신러닝",
};

const DEFAULT_THEME = "dark";
const DEFAULT_LANGUAGE = "en";
const PREFERENCE_VERSION = "20260618-english-comfort";
const UPDATE_STATUS_URLS = [
  "https://raw.githubusercontent.com/lko9911/GPT_Paper_research/main/data/update_status.json",
  "data/update_status.json",
];
const AML_RECOMMENDATIONS_URL = "public/data/aml_recommended_papers.json";
const PAPERS_INDEX_URL = "data/papers_index.json";
const PAPERS_FALLBACK_URL = "data/papers.json";
const DETAIL_MANIFEST_URL = "data/detail_manifest.json";
const DETAILS_BASE_URL = "data/details/";
const INITIAL_RENDER_LIMIT = 80;
const RENDER_INCREMENT = 80;
const FILTER_DEBOUNCE_MS = 120;

if (localStorage.getItem("preferenceVersion") !== PREFERENCE_VERSION) {
  localStorage.setItem("theme", DEFAULT_THEME);
  localStorage.setItem("preferenceVersion", PREFERENCE_VERSION);
}
localStorage.removeItem("language");

const state = {
  papers: [],
  amlRecommendations: [],
  siteMeta: null,
  updateStatus: null,
  filtered: [],
  renderLimit: INITIAL_RENDER_LIMIT,
  activeTargetVenue: "",
  activeVenueGroup: "",
  activeSubtopic: "",
  amlPanelRequested: false,
  theme: localStorage.getItem("theme") || DEFAULT_THEME,
  language: DEFAULT_LANGUAGE,
  collapsedFields: new Set(readStoredArray("collapsedFields")),
  paperDetails: new Map(),
  detailManifest: null,
  detailChunks: new Map(),
  detailLoading: new Set(),
  detailErrors: new Map(),
  filterTimer: null,
};

function readStoredArray(key) {
  try {
    const value = JSON.parse(localStorage.getItem(key) || "[]");
    return Array.isArray(value) ? value : [];
  } catch (error) {
    return [];
  }
}

const els = {
  list: document.querySelector("#paper-list"),
  empty: document.querySelector("#empty-state"),
  count: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  category: document.querySelector("#category-filter"),
  tag: document.querySelector("#tag-filter"),
  venue: document.querySelector("#venue-filter"),
  summaryProvider: document.querySelector("#summary-provider-filter"),
  year: document.querySelector("#year-filter"),
  sort: document.querySelector("#sort-select"),
  resetFilters: document.querySelector("#reset-filters"),
  sideTopicNav: document.querySelector("#side-topic-nav"),
  venueBoard: document.querySelector("#venue-board"),
  total: document.querySelector("#stat-total"),
  venues: document.querySelector("#stat-venues"),
  years: document.querySelector("#stat-years"),
  updated: document.querySelector("#stat-updated"),
  opsNote: document.querySelector("#ops-note"),
  heroStatus: document.querySelector("#hero-status"),
  themeToggle: document.querySelector("#theme-toggle"),
  amlSection: document.querySelector("#aml-recommendations"),
  amlList: document.querySelector("#aml-recommendation-list"),
  amlCount: document.querySelector("#aml-result-count"),
  loadMore: document.querySelector("#load-more-papers"),
};

async function init() {
  setupPreferences();
  state.papers = await loadPaperIndex();
  preparePaperRuntimeCache(state.papers);
  try {
    const response = await fetch(`data/site_meta.json?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.siteMeta = await response.json();
  } catch (error) {
    console.warn("Failed to load site_meta.json", error);
    state.siteMeta = null;
  }
  state.amlRecommendations = await loadAmlRecommendations();
  state.updateStatus = await loadUpdateStatus();

  buildFilters();
  buildSideNav();
  renderVenueBoard();
  renderAmlRecommendations();
  updateStats();
  applyFilters();

  [els.search, els.category, els.tag, els.venue, els.summaryProvider, els.year, els.sort].forEach((el) => {
    if (!el) return;
    el.addEventListener("input", () => {
      if (el === els.category) state.activeSubtopic = "";
      if (el === els.venue) clearVenueQuickFilters();
      if (el === els.search) {
        scheduleApplyFilters();
      } else {
        applyFilters();
      }
    });
    el.addEventListener("change", () => {
      if (el === els.category) state.activeSubtopic = "";
      if (el === els.venue) clearVenueQuickFilters();
      applyFilters();
    });
  });

  if (els.resetFilters) {
    els.resetFilters.addEventListener("click", resetFilters);
  }
  if (els.loadMore) {
    els.loadMore.addEventListener("click", () => {
      state.renderLimit += RENDER_INCREMENT;
      render();
    });
  }
}

async function loadPaperIndex() {
  try {
    const response = await fetch(`${PAPERS_INDEX_URL}?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed to load papers_index.json", error);
    showDataLoadError("Could not load the lightweight paper index. Trying local fallback data.");
  }

  try {
    const response = await fetch(`${PAPERS_FALLBACK_URL}?ts=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    console.warn("Using full papers.json fallback. Production should serve papers_index.json.");
    return await response.json();
  } catch (error) {
    console.error("Failed to load fallback papers.json", error);
    showDataLoadError("Paper data could not be loaded. Please regenerate split data files.");
    return [];
  }
}

function showDataLoadError(message) {
  if (!els.empty) return;
  els.empty.hidden = false;
  els.empty.innerHTML = `<strong>Data loading problem.</strong><p>${escapeHtml(message)}</p>`;
}

function preparePaperRuntimeCache(papers) {
  papers.forEach(preparePaperRuntime);
}

function preparePaperRuntime(paper) {
  const visible = visibleTags(paper);
  const subtopics = deriveSubtopics(paper);
  const field = deriveField(paper);
  const canonicalTags = [...(paper.tags || []), ...visible, ...subtopics]
    .map(canonicalTopicLabel)
    .filter((topic) => topic !== "Digital Twins" || paperHasCuratedDigitalTwinTag(paper));
  const searchText = normalize(
    [
      field,
      paper.title,
      (paper.authors || []).join(" "),
      authorSearchText(paper),
      paper.venue,
      paper.doi,
      (paper.categories || []).join(" "),
      visible.join(" "),
      subtopics.join(" "),
      paper.ai_summary_en,
      paper.relevance_note_en,
    ].join(" ")
  );

  paper._runtime = {
    field,
    visibleTags: visible,
    subtopics,
    canonicalTagSet: new Set(canonicalTags),
    venue: normalizeVenue(paper.venue),
    searchText,
    summaryProvider: summaryProviderForFilter(paper),
  };
  return paper._runtime;
}

function runtimeForPaper(paper) {
  return paper._runtime || preparePaperRuntime(paper);
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
  window.setInterval(() => {
    updateStats();
  }, 60000);
}

function applyPreferences() {
  document.documentElement.dataset.theme = state.theme;
  document.documentElement.lang = "en";
  if (els.themeToggle) {
    els.themeToggle.textContent = state.theme === "dark" ? t("themeLight") : t("themeDark");
  }
  applyStaticLanguage();
}

function applyStaticLanguage() {
  setText(".subtitle", t("subtitle"));
  setText(".notice", t("noticeMain"));
  setText(".notice-soft", t("noticeSoft"));
  setText(".sidebar strong", t("sideTitle"));
  setText(".stats article:nth-child(1) strong", t("totalPapers"));
  setText(".stats article:nth-child(2) strong", t("venueCount"));
  setText(".stats article:nth-child(3) strong", t("yearRange"));
  setText(".stats article:nth-child(4) strong", t("currentUpdate"));
  setText(".search-label-text", t("search"));
  setText(".controls label:nth-child(2) span", t("field"));
  setText(".controls label:nth-child(3) span", t("tagSubtopic"));
  setText(".controls label:nth-child(4) span", t("venue"));
  setText(".controls label:nth-child(5) span", t("summaryProvider"));
  setText(".controls label:nth-child(6) span", t("year"));
  setText(".controls label:nth-child(7) span", t("sort"));
  setText("#category-filter option[value='']", t("all"));
  setText("#tag-filter option[value='']", t("all"));
  setText("#venue-filter option[value='']", t("all"));
  setText("#summary-provider-filter option[value='']", t("allSummaries"));
  setText("#summary-provider-filter option[value='openai']", t("openaiApplied"));
  setText("#summary-provider-filter option[value='metadata']", t("openaiNotApplied"));
  setText("#year-filter option[value='']", t("all"));
  setText("#sort-select option[value='newest']", t("newest"));
  setText("#sort-select option[value='relevance']", t("relevance"));
  setText("#sort-select option[value='title']", t("title"));
  setText("#reset-filters", t("resetFilters"));
  setText(".venue-section-head h2", t("venuesTitle"));
  setText(".results-head .section-kicker", t("papersByField"));
  setText(".results-head h2", t("curatedPapers"));
  setText("#empty-state strong", t("emptyTitle"));
  setText("#empty-state p", t("emptyText"));
  setText("#footer-policy", t("footer"));
  setText("#contact-label", t("contactLabel"));
  if (!state.papers.length) {
    setText("#hero-status", t("heroStatusLoading"));
  }
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

function buildFilters() {
  const fields = new Set();
  const tags = new Set();
  const venues = new Set();
  const years = new Set();

  state.papers.forEach((paper) => {
    const runtime = runtimeForPaper(paper);
    fields.add(runtime.field);
    runtime.visibleTags.forEach((tag) => tags.add(tag));
    runtime.subtopics.forEach((subtopic) => tags.add(canonicalTopicLabel(subtopic)));
    venues.add(runtime.venue);
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

function buildSideNav() {
  const fieldCounts = countBy(state.papers, (paper) => runtimeForPaper(paper).field);
  const amlCount = amlVisibleRecommendations().length;
  const amlShortcut = `<button class="side-top-link" type="button" data-side-target="aml-recommendations">
    <span class="side-label">AML Recommendations</span>
    <span class="side-count">${amlCount ? amlCount.toLocaleString("en-US") : "Open"}</span>
  </button>`;
  const fieldGroups = FIELD_ORDER.filter((field) => fieldCounts.get(field))
    .map((field) => {
      const subtopics = FIELD_SUBTOPICS[field] || [];
      const fieldPapers = state.papers.filter((paper) => runtimeForPaper(paper).field === field);
      const bucketCounts = sidebarBucketCounts(fieldPapers, subtopics);
      const isCollapsed = state.collapsedFields.has(field);
      const subtopicButtons = [...subtopics, SIDEBAR_OTHER_TOPIC]
        .map((subtopic) => sideSubtopicButton(field, subtopic, bucketCounts.get(subtopic) || 0))
        .join("");
      return `<div class="side-field-group${isCollapsed ? " is-collapsed" : ""}">
        <button class="side-field" type="button" data-side-field="${escapeAttribute(field)}" aria-expanded="${isCollapsed ? "false" : "true"}">
          <span class="side-caret" aria-hidden="true"></span>
          <span class="side-label">${escapeHtml(displayLabel(field))}</span>
          <span class="side-count">${fieldCounts.get(field)}</span>
        </button>
        <div class="side-subtopics" ${isCollapsed ? "hidden" : ""}>${subtopicButtons}</div>
      </div>`;
    })
    .join("");
  els.sideTopicNav.innerHTML = `${amlShortcut}${fieldGroups}`;

  els.sideTopicNav.querySelectorAll("[data-side-target]").forEach((button) => {
    button.addEventListener("click", () => {
      state.amlPanelRequested = true;
      renderAmlRecommendations();
      const target = document.querySelector(`#${button.dataset.sideTarget}`);
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  els.sideTopicNav.querySelectorAll("[data-side-field]").forEach((button) => {
    button.addEventListener("click", (event) => {
      const field = button.dataset.sideField;
      const subtopic = button.dataset.sideSubtopic || "";
      if (!subtopic && event.target.closest(".side-caret")) {
        toggleSideField(field);
        return;
      }
      els.category.value = field;
      state.activeSubtopic = subtopic;
      syncSideNavActive();
      applyFilters();
      scrollToPapers();
    });
  });
}

function toggleSideField(field) {
  if (state.collapsedFields.has(field)) {
    state.collapsedFields.delete(field);
  } else {
    state.collapsedFields.add(field);
  }
  localStorage.setItem("collapsedFields", JSON.stringify([...state.collapsedFields]));
  buildSideNav();
  syncSideNavActive();
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
    const venue = runtimeForPaper(paper).venue;
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
  const visibleVenueKeys = new Set(priorityEntries.map(([venue]) => normalizeVenueKey(venue)));
  const hiddenEntries = entries.filter(([venue]) => !visibleVenueKeys.has(normalizeVenueKey(venue)));
  const hiddenPaperCount = hiddenEntries.reduce((sum, [, count]) => sum + count, 0);

  const mainCards = [
    `<button class="venue-card is-all is-active" type="button" data-board-venue="">
      <strong>${escapeHtml(t("allVenues"))}</strong>
      <span>${state.papers.length} ${escapeHtml(t("papers"))}</span>
    </button>`,
    ...priorityEntries.map(([venue, count]) => venueCard(venue, count, t("priority"))),
    hiddenPaperCount ? otherVenueCard(hiddenPaperCount) : "",
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

async function loadAmlRecommendations() {
  try {
    const response = await fetch(`${AML_RECOMMENDATIONS_URL}?ts=${Date.now()}`);
    if (!response.ok) return [];
    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.warn("AML recommendations are not available yet", error);
    return [];
  }
}

function renderAmlRecommendations() {
  if (!els.amlSection || !els.amlList || !els.amlCount) return;
  const items = state.amlRecommendations || [];
  if (!items.length) {
    if (!state.amlPanelRequested) {
      els.amlSection.hidden = true;
      return;
    }
    els.amlSection.hidden = false;
    els.amlCount.textContent = "No published recommendations";
    els.amlList.innerHTML = amlEmptyMessage();
    return;
  }
  const visible = amlVisibleRecommendations();
  if (!visible.length) {
    if (!state.amlPanelRequested) {
      els.amlSection.hidden = true;
      return;
    }
    els.amlSection.hidden = false;
    els.amlCount.textContent = "0 recommendations";
    els.amlList.innerHTML = amlEmptyMessage("The AML recommendation file exists, but no public recommendations are available.");
    return;
  }
  els.amlSection.hidden = false;
  els.amlCount.textContent = `${visible.length.toLocaleString("en-US")} recommendations`;
  els.amlList.innerHTML = visible.map(renderAmlRecommendationCard).join("");
  attachAmlCitationHandlers(visible);
}

function amlEmptyMessage(message = "No public AML recommendation file is available yet. Run the manual AML Recommendation workflow to publish related papers here.") {
  return `<div class="aml-empty-card">
    <strong>AML recommendation papers are not published yet.</strong>
    <p>${escapeHtml(message)}</p>
  </div>`;
}

function amlVisibleRecommendations() {
  return (state.amlRecommendations || [])
    .filter((item) => ["High", "Possible", "Watch"].includes(item.recommendation_level))
    .sort((a, b) => Number(b.aml_score || 0) - Number(a.aml_score || 0))
    .slice(0, 24);
}

function renderAmlRecommendationCard(item) {
  const doiUrl = item.url || (item.doi ? `https://doi.org/${item.doi}` : "");
  const publicationLabel = [item.journal || "Venue unknown", item.year].filter(Boolean).join(" ");
  const score = Math.round(Number(item.aml_score || 0) * 100);
  const topics = (item.matched_topics || [])
    .slice(0, 3)
    .map((topic) => badge(displayLabel(topic), "tag"))
    .join("");
  const routes = (item.discovery_routes || []).slice(0, 3).map((route) => String(route).replace(/_/g, " ")).join(", ");
  const seed = (item.related_seed_papers || [])[0];
  const seedText = seed && seed.title ? `Closest seed: ${seed.title}` : "";
  const summaryHtml = renderAmlSummaryBlock(item);
  const relevanceNote = formatAmlRelevanceNote(item);
  const authorDetailsHtml = renderAuthorDetails({
    authors: Array.isArray(item.authors) ? item.authors : [],
    author_details: Array.isArray(item.author_details) ? item.author_details : [],
  });
  return `<article class="paper-card aml-card">
    <div class="card-content">
      <div class="card-topline">
        <span class="publication-badge">${escapeHtml(publicationLabel)}</span>
        <span class="relevance-badge">AML ${escapeHtml(String(score))}/100</span>
      </div>
      <h4 class="paper-title">${escapeHtml(item.title || "Untitled")}</h4>
      ${authorDetailsHtml}
      ${summaryHtml}
      <p class="relevance-note">${escapeHtml(relevanceNote)}</p>
      ${seedText ? `<p class="policy-mini">${escapeHtml(seedText)}</p>` : ""}
      <div class="tag-line">${topics}</div>
      <div class="card-links">
        ${doiUrl ? `<a class="link-pill primary" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">Open Paper</a>` : ""}
        ${doiUrl ? `<a class="link-pill subtle" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">DOI</a>` : ""}
        <button class="link-pill subtle" type="button" data-aml-citation="${escapeAttribute(item.doi || item.title || "")}">${escapeHtml(t("copyCitation"))}</button>
      </div>
      <p class="policy-mini">AML recommendation - ${escapeHtml(routes ? `routes: ${routes}` : "manual recommendation output")} - updated ${escapeHtml(formatAmlUpdatedAt(item.updated_at))}</p>
    </div>
  </article>`;
}

function scheduleApplyFilters() {
  window.clearTimeout(state.filterTimer);
  state.filterTimer = window.setTimeout(applyFilters, FILTER_DEBOUNCE_MS);
}

function formatAmlRelevanceNote(item) {
  const topics = amlMatchedTopicLabels(item);
  const topicPhrase = formatEnglishList(topics) || "the AML recommendation profile";
  const score = Math.max(0, Math.min(100, Math.round(Number(item.aml_score || 0) * 100)));
  const routes = (item.discovery_routes || [])
    .slice(0, 2)
    .map((route) => String(route).replace(/_/g, " "))
    .filter(Boolean);
  const routePhrase = routes.length ? ` and found through ${formatEnglishList(routes)}` : "";
  const seed = (item.related_seed_papers || [])[0];
  const seedPhrase = seed && seed.title ? `; closest seed: ${seed.title}` : "";
  return `Relevant to the tracker through ${topicPhrase}; AML score: ${score}/100. Why this score: matched ${topicPhrase}${routePhrase}${seedPhrase}.`;
}

function amlMatchedTopicLabels(item) {
  const labels = [];
  const seen = new Set();
  (item.matched_topics || []).forEach((topic) => {
    const label = normalizeAmlTopicLabel(displayLabel(topic));
    const key = label.toLowerCase();
    if (label && !seen.has(key)) {
      seen.add(key);
      labels.push(label);
    }
  });
  return labels.slice(0, 3);
}

function normalizeAmlTopicLabel(label) {
  const value = String(label || "").trim();
  const lower = value.toLowerCase();
  if (!value) return "";
  if (lower === "liquid crystal elastomer" || lower === "liquid crystal elastomers") return "LCE";
  if (lower === "soft robotics") return "Soft Robotics";
  return value;
}

function renderAmlSummaryBlock(item) {
  return `<dl class="summary summary-qa">
    ${amlSummarySections(item)
      .map(
        (section, index) => `<div class="${index === 4 ? "is-takeaway" : ""}">
          <dt>${escapeHtml(section.question)}</dt>
          <dd>${escapeHtml(section.answer)}</dd>
        </div>`
      )
      .join("")}
  </dl>`;
}

function amlSummarySections(item) {
  const labels = UI_TEXT.en.summaryQuestions;
  const title = item.title || "This paper";
  const venue = item.journal || "an unknown venue";
  const year = item.year || "undated";
  const topics = (item.matched_topics || []).slice(0, 4).map(displayLabel);
  const topicPhrase = formatEnglishList(topics) || "the AML recommendation profile";
  const routes = (item.discovery_routes || []).slice(0, 3).map((route) => String(route).replace(/_/g, " "));
  const routePhrase = formatEnglishList(routes) || "the current recommendation pool";
  const seed = (item.related_seed_papers || [])[0];
  const score = Math.round(Number(item.aml_score || 0) * 100);
  const reason = item.why_recommended || `It matches ${topicPhrase} in the AML recommendation profile.`;

  return [
    {
      question: labels[0],
      answer: `${title} is a ${year} paper from ${venue} recommended for its connection to ${topicPhrase}.`,
    },
    {
      question: labels[1],
      answer: "It is included because the recommendation engine detected overlap with the lab's target manufacturing and design interests.",
    },
    {
      question: labels[2],
      answer: `It was selected through ${routePhrase} using metadata, curated topic signals, and AML profile scoring; the detailed method should be checked in the DOI source.`,
    },
    {
      question: labels[3],
      answer: seed && seed.title
        ? `The strongest recommendation signal is its similarity to the seed paper "${seed.title}".`
        : reason,
    },
    {
      question: labels[4],
      answer: `${reason} Current AML recommendation score is ${score}/100.`,
    },
  ];
}

function attachAmlCitationHandlers(items) {
  const citationMap = new Map(items.map((item) => [String(item.doi || item.title || ""), buildAmlCitation(item)]));
  els.amlList.querySelectorAll("[data-aml-citation]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const key = event.currentTarget.dataset.amlCitation || "";
      await navigator.clipboard.writeText(citationMap.get(key) || "");
      event.currentTarget.textContent = t("copiedCitation");
      window.setTimeout(() => {
        event.currentTarget.textContent = t("copyCitation");
      }, 1400);
    });
  });
}

function buildAmlCitation(item) {
  if (item.citation) return item.citation;
  const authors = Array.isArray(item.authors) ? item.authors.join(", ") : "";
  const year = item.year ? `(${item.year})` : "";
  const venue = item.journal ? ` ${item.journal}.` : "";
  const doi = item.doi ? ` https://doi.org/${item.doi}` : "";
  return `${authors} ${year}. ${item.title || "Untitled"}.${venue}${doi}`.replace(/\s+/g, " ").trim();
}

function formatAmlUpdatedAt(value) {
  const formatted = formatRunTime(value);
  return formatted ? `${formatted.date} ${formatted.time} KST` : "-";
}

function clearVenueQuickFilters() {
  state.activeTargetVenue = "";
  state.activeVenueGroup = "";
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
  const displayVenue = displayText(shortVenue(venue));
  return `<button class="venue-card" type="button" data-board-venue="${escapeAttribute(displayText(venue))}">
    <strong>${escapeHtml(displayVenue)}</strong>
    <span><b>${count}</b> ${escapeHtml(t("papers"))}</span>
    ${badge}
  </button>`;
}

function otherVenueCard(paperCount) {
  return `<button class="venue-card venue-card-muted" type="button" data-board-venue="" data-board-venue-group="other">
    <strong>${escapeHtml(t("others"))}</strong>
    <span><b>${paperCount}</b> ${escapeHtml(t("papers"))}</span>
    <em class="venue-chip">${escapeHtml(t("lowCountVenue"))}</em>
  </button>`;
}

function updateStats() {
  const meta = state.siteMeta || {};
  const rawCount = meta.raw_candidate_count || state.papers.length;
  const archivedCount = meta.archived_count || Math.max(0, rawCount - state.papers.length);
  const lastRunAt = state.siteMeta && state.siteMeta.last_run_at_utc;
  const locale = "en-US";

  renderTotalStat(lastRunAt);
  const venues = new Set(state.papers.map((paper) => runtimeForPaper(paper).venue).filter(Boolean));
  if (els.venues) {
    els.venues.textContent = venues.size.toLocaleString(locale);
  }
  const yearRange = formatYearRange(state.papers);
  if (els.years) {
    els.years.textContent = yearRange;
  }
  renderUpdatedStat(lastRunAt);
  renderHeroStatus({
    paperCount: state.papers.length,
    venueCount: venues.size,
    yearRange,
    lastRunAt,
  });
  renderOpsNote(rawCount, archivedCount, lastRunAt);
}

function renderHeroStatus({ paperCount, venueCount, yearRange, lastRunAt }) {
  if (!els.heroStatus) return;
  const locale = "en-US";
  const lastRun = formatRunTime(lastRunAt);
  const updated = lastRun ? `${lastRun.date} ${lastRun.time}` : "-";
  els.heroStatus.textContent = t("heroStatus")
    .replace("{papers}", paperCount.toLocaleString(locale))
    .replace("{venues}", venueCount.toLocaleString(locale))
    .replace("{years}", yearRange)
    .replace("{updated}", updated);
}

function renderOpsNote(rawCount, archivedCount, lastRunAt) {
  if (!els.opsNote) return;
  const locale = "en-US";
  const shownCount = state.papers.length.toLocaleString(locale);
  const rawText = rawCount.toLocaleString(locale);
  const archivedText = archivedCount.toLocaleString(locale);
  const lastRun = formatRunTime(lastRunAt);
  const timeText = lastRun ? `${lastRun.date} ${lastRun.time} KST` : "-";
  els.opsNote.textContent = `Ops note: ${shownCount} shown / ${rawText} collected candidates / ${archivedText} hidden at the bottom layer - last collection ${timeText}`;
}

function renderUpdatedStat(lastRunAt) {
  if (!els.updated) return;
  const now = formatKstTime(new Date());
  const lastRun = formatRunTime(lastRunAt);
  const attempt = updateAttemptDisplay();
  els.updated.classList.add("stat-datetime");
  if (!lastRun) {
    els.updated.innerHTML = `${escapeHtml(now.date)}<small>${escapeHtml(now.time)} KST${attempt ? ` - ${escapeHtml(attempt)}` : ""}</small>`;
    return;
  }
  const updatedLabel = "updated";
  els.updated.innerHTML = `${escapeHtml(now.date)}<small>${escapeHtml(now.time)} KST - ${escapeHtml(updatedLabel)} ${escapeHtml(lastRun.time)} KST${attempt ? ` - ${escapeHtml(attempt)}` : ""}</small>`;
}

async function loadUpdateStatus() {
  for (const url of UPDATE_STATUS_URLS) {
    try {
      const response = await fetch(`${url}?ts=${Date.now()}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.warn(`Failed to load update status from ${url}`, error);
    }
  }
  return null;
}

function updateAttemptDisplay() {
  const status = state.updateStatus || {};
  const phase = String(status.update_phase || "").toLowerCase();
  const jobStatus = String(status.job_status || "").toLowerCase();
  const updateStep = String(status.update_step_outcome || "").toLowerCase();
  if (phase === "in_progress" || jobStatus === "in_progress" || updateStep === "running") {
    return "updating now";
  }
  const missedSchedule = missedScheduleDisplay(status);
  if (missedSchedule) return missedSchedule;
  const checked = formatRunTime(status.checked_at_utc);
  const checkedText = checked ? checked.time : "";
  if (jobStatus === "failure" || jobStatus === "failed" || updateStep === "failure") {
    return `last attempt failed${checkedText ? ` ${checkedText}` : ""}`;
  }
  if (jobStatus === "cancelled" || updateStep === "cancelled") {
    return `last attempt cancelled${checkedText ? ` ${checkedText}` : ""}`;
  }
  if (jobStatus === "success" && checkedText) {
    return `checked ${checkedText}`;
  }
  return "";
}

function missedScheduleDisplay(status) {
  const dueAt = latestScheduledRunUtc(status.schedule);
  if (!dueAt) return "";
  const checkedAt = parseDate(status.checked_at_utc);
  if (checkedAt && checkedAt.getTime() >= dueAt.getTime()) return "";
  const due = formatRunTime(dueAt.toISOString());
  const dueText = due ? due.time : "";
  return `${dueText} run not seen yet`;
}

function latestScheduledRunUtc(schedule) {
  const knownSchedules = new Set(["17 1,7,13,19 * * *", "17 1,13 * * *", "17 */12 * * *"]);
  if (schedule && !knownSchedules.has(schedule)) return null;
  const now = new Date();
  const candidates = [1, 7, 13, 19].map((hour) => {
    const date = new Date(now);
    date.setUTCSeconds(0, 0);
    date.setUTCMinutes(17);
    date.setUTCHours(hour);
    if (date.getTime() > now.getTime()) {
      date.setUTCDate(date.getUTCDate() - 1);
    }
    return date;
  });
  return candidates.sort((a, b) => b.getTime() - a.getTime())[0];
}

function parseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function renderTotalStat(lastRunAt) {
  if (!els.total) return;
  const locale = "en-US";
  const total = state.papers.length;
  const weeklyCount = countRecentlyAddedPapers(state.papers, lastRunAt, 7);
  const latestAdded = Number(state.siteMeta && state.siteMeta.papers_added);
  const deltaText = formatPaperDeltaText(total, weeklyCount, latestAdded, locale);
  els.total.classList.add("stat-with-note");
  els.total.innerHTML = `${escapeHtml(total.toLocaleString(locale))}${deltaText ? `<small>${escapeHtml(deltaText)}</small>` : ""}`;
}

function formatPaperDeltaText(total, weeklyCount, latestAdded, locale) {
  const parts = [];
  if (Number.isFinite(latestAdded) && latestAdded > 0) {
    const countText = latestAdded.toLocaleString(locale);
    parts.push(`+${countText} ${t("latestRunAdded")}`);
  }
  if (weeklyCount > 0) {
    const countText = weeklyCount.toLocaleString(locale);
    parts.push(`+${countText} ${t("weeklyAddedShort")}`);
  }
  return parts.join(" - ");
}

function countRecentlyAddedPapers(papers, lastRunAt, days) {
  const referenceDate = referenceDateOnly(lastRunAt);
  if (!referenceDate) return 0;
  const startDate = new Date(referenceDate);
  startDate.setUTCDate(startDate.getUTCDate() - Math.max(0, days - 1));
  return papers.filter((paper) => {
    const addedDate = parseDateOnly(paper.first_added);
    return addedDate && addedDate >= startDate && addedDate <= referenceDate;
  }).length;
}

function referenceDateOnly(lastRunAt) {
  const lastRun = formatRunTime(lastRunAt);
  if (lastRun && lastRun.date) return parseDateOnly(lastRun.date);
  const now = formatKstTime(new Date());
  return parseDateOnly(now.date);
}

function parseDateOnly(value) {
  const match = String(value || "").match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return null;
  const date = new Date(Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3])));
  return Number.isNaN(date.getTime()) ? null : date;
}

function formatYearRange(papers) {
  const years = papers.map((paper) => Number(paper.year)).filter((year) => Number.isInteger(year) && year > 0);
  if (!years.length) return "-";
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  return minYear === maxYear ? String(maxYear) : `${minYear}-${maxYear}`;
}

function applyFilters() {
  const query = normalize(els.search.value);
  const category = els.category.value;
  const tag = els.tag.value;
  const venue = els.venue.value;
  const summaryProvider = els.summaryProvider ? els.summaryProvider.value : "";
  const year = els.year.value;
  const sort = els.sort.value;

  if (!category) state.activeSubtopic = "";
  state.renderLimit = INITIAL_RENDER_LIMIT;
  syncSideNavActive();

  state.filtered = state.papers.filter((paper) => {
    const runtime = runtimeForPaper(paper);
    const paperVenue = runtime.venue;
    const paperField = runtime.field;

    const matchesQuery = !query || runtime.searchText.includes(query);
    const matchesCategory = !category || paperField === category;
    const matchesTag = !tag || runtime.canonicalTagSet.has(canonicalTopicLabel(tag));
    const matchesVenue = !venue || paperVenue === venue;
    const matchesTarget = !state.activeTargetVenue || matchesTargetVenue(paperVenue, state.activeTargetVenue);
    const matchesVenueGroup = !state.activeVenueGroup || isOtherVenuePaper(paper);
    const matchesSubtopic = !state.activeSubtopic || paperMatchesSidebarSubtopic(paper, paperField, state.activeSubtopic);
    const matchesSummaryProvider = !summaryProvider || runtime.summaryProvider === summaryProvider;
    const matchesYear = !year || String(paper.year || "") === year;
    return (
      matchesQuery &&
      matchesCategory &&
      matchesTag &&
      matchesVenue &&
      matchesTarget &&
      matchesVenueGroup &&
      matchesSubtopic &&
      matchesSummaryProvider &&
      matchesYear
    );
  });

  state.filtered.sort((a, b) => {
    if (sort === "newest") {
      return Number(b.year || 0) - Number(a.year || 0) || dateValue(b.last_updated) - dateValue(a.last_updated);
    }
    if (sort === "title") {
      return (a.title || "").localeCompare(b.title || "", "en");
    }
    return Number(b.relevance_score || 0) - Number(a.relevance_score || 0) || Number(b.year || 0) - Number(a.year || 0);
  });

  render();
}

function resetFilters() {
  if (els.search) els.search.value = "";
  if (els.category) els.category.value = "";
  if (els.tag) els.tag.value = "";
  if (els.venue) els.venue.value = "";
  if (els.summaryProvider) els.summaryProvider.value = "";
  if (els.year) els.year.value = "";
  if (els.sort) els.sort.value = "newest";
  state.activeTargetVenue = "";
  state.activeVenueGroup = "";
  state.activeSubtopic = "";
  clearVenueQuickFilters();
  syncSideNavActive();
  applyFilters();
}

function summaryProviderForFilter(paper) {
  return paper.openai_summary_applied === true || paper.summary_provider === "openai"
    ? "openai"
    : "metadata";
}

function isOtherVenuePaper(paper) {
  const venue = normalizeVenue(paper.venue);
  return !isPriorityVenue(venue);
}

function render() {
  const visiblePapers = state.filtered.slice(0, state.renderLimit);
  const totalCount = state.filtered.length;
  els.count.textContent = `${Math.min(visiblePapers.length, totalCount).toLocaleString("en-US")} / ${totalCount.toLocaleString("en-US")} ${t("showing")}`;
  els.list.innerHTML = "";
  els.empty.hidden = totalCount > 0;
  if (els.loadMore) {
    els.loadMore.hidden = visiblePapers.length >= totalCount;
    els.loadMore.textContent = `Load more papers (${visiblePapers.length.toLocaleString("en-US")} / ${totalCount.toLocaleString("en-US")})`;
  }

  const fragment = document.createDocumentFragment();
  const groups = groupByPrimaryCategory(visiblePapers);
  groups.forEach(([category, papers]) => {
    fragment.append(renderGroup(category, papers));
  });
  els.list.append(fragment);
}

function groupByPrimaryCategory(papers) {
  const grouped = new Map();
  papers.forEach((paper) => {
    const category = runtimeForPaper(paper).field;
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
      <span>${papers.length.toLocaleString("en-US")} ${escapeHtml(t("papers"))}</span>
    </div>
  `;
  papers.forEach((paper) => section.append(renderPaperRow(paper)));
  return section;
}

function renderPaperRow(paper) {
  const article = document.createElement("article");
  article.className = "paper-card";
  const displayPaper = paperWithDetails(paper);
  const isDetailLoaded = state.paperDetails.has(paper.id);
  const isDetailLoading = state.detailLoading.has(paper.id);
  const detailError = state.detailErrors.get(paper.id) || "";

  const doiUrl = displayPaper.url || (displayPaper.doi ? `https://doi.org/${displayPaper.doi}` : "");
  const authorDetailsHtml = renderAuthorDetails(displayPaper);
  const publicationLabel = formatPublicationLabel(displayPaper);
  const summaryProviderLabel = formatSummaryProviderLabel(displayPaper);
  const summaryHtml = renderSummaryBlock(displayPaper);
  const relevanceNote = formatRelevanceNote(displayPaper);
  const representativeBadges = representativeTags(displayPaper)
    .map((tag) => badge(displayLabel(tag), "tag"))
    .join("");
  const detailButton = isDetailLoaded
    ? `<button class="link-pill subtle" type="button" disabled>Details loaded</button>`
    : `<button class="link-pill subtle" type="button" data-load-detail="${escapeAttribute(paper.id)}">${escapeHtml(isDetailLoading ? "Loading details..." : "Load details")}</button>`;
  const detailErrorHtml = detailError ? `<p class="policy-mini detail-error">${escapeHtml(detailError)}</p>` : "";

  article.innerHTML = `
    <div class="card-content">
      <div class="card-topline">
        <span class="publication-badge">${escapeHtml(publicationLabel)}</span>
        <span class="${escapeAttribute(summaryProviderLabel.className)}" title="${escapeAttribute(summaryProviderLabel.title)}">${escapeHtml(summaryProviderLabel.text)}</span>
        <span class="relevance-badge">${escapeHtml(t("relevanceLabel"))} ${escapeHtml(String(displayPaper.relevance_score || "-"))}/10</span>
      </div>
      <h4 class="paper-title">${escapeHtml(displayText(displayPaper.title || "Untitled"))}</h4>
      ${authorDetailsHtml}
      ${summaryHtml}
      <p class="relevance-note">${escapeHtml(relevanceNote)}</p>
      <div class="tag-line">${representativeBadges}</div>
      <div class="card-links">
        ${doiUrl ? `<a class="link-pill primary" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t("openPaper"))}</a>` : ""}
        ${doiUrl ? `<a class="link-pill subtle" href="${escapeAttribute(doiUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t("doiButton"))}</a>` : ""}
        <button class="link-pill subtle" type="button" data-citation>${escapeHtml(t("copyCitation"))}</button>
        ${detailButton}
      </div>
      ${detailErrorHtml}
      <p class="policy-mini">No abstract/PDF hosted - updated ${escapeHtml(displayPaper.last_updated || "-")}</p>
    </div>
  `;

  article.querySelector("[data-citation]").addEventListener("click", async (event) => {
    const citation = buildCitation(displayPaper);
    await navigator.clipboard.writeText(citation);
    event.currentTarget.textContent = t("copiedCitation");
    window.setTimeout(() => {
      event.currentTarget.textContent = t("copyCitation");
    }, 1400);
  });

  const loadDetailButton = article.querySelector("[data-load-detail]");
  if (loadDetailButton) {
    loadDetailButton.addEventListener("click", async () => {
      await loadPaperDetail(paper.id);
      render();
    });
  }

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

function renderAuthorDetails(paper) {
  const details = Array.isArray(paper.author_details) ? paper.author_details : [];
  const fallbackAuthors = Array.isArray(paper.authors) ? paper.authors : [];
  const corresponding = Array.isArray(paper.corresponding_authors) ? paper.corresponding_authors : [];
  if (!details.length && !fallbackAuthors.length && !corresponding.length) return "";
  const correspondingNames = new Set(corresponding.map((author) => normalizeAuthorName(author && author.name)).filter(Boolean));
  const visibleLimit = 8;
  const visibleDetails = details.length
    ? details.slice(0, visibleLimit).map((author) => ({
        name: author.name || "",
        tooltip: [author.name, author.position, primaryInstitution(author)].filter(Boolean).join(" - "),
        isCorresponding: Boolean(author.is_corresponding),
      }))
    : fallbackAuthors.slice(0, visibleLimit).map((name) => ({
        name,
        tooltip: name,
        isCorresponding: correspondingNames.has(normalizeAuthorName(name)),
      }));
  const visibleNames = new Set(visibleDetails.map((author) => normalizeAuthorName(author.name)));
  const hiddenCorresponding = details.length
    ? details.slice(visibleLimit).filter((author) => author && author.is_corresponding && !visibleNames.has(normalizeAuthorName(author.name)))
    : corresponding.filter((author) => author && author.name && !visibleNames.has(normalizeAuthorName(author.name)));
  const supplementalCorresponding = hiddenCorresponding.slice(0, 2).map((author) => ({
    name: author.name || "",
    tooltip: [author.name, author.position, primaryInstitution(author)].filter(Boolean).join(" - "),
    isCorresponding: true,
  }));
  const allChips = [...visibleDetails, ...supplementalCorresponding];
  const chips = allChips.map((author) => {
    const name = author.name || "";
    if (!name) return "";
    const corrBadge = author.isCorresponding
      ? `<span class="author-chip-badge">${escapeHtml(t("correspondingAuthorBadge"))}</span>`
      : "";
    const className = `author-chip${author.isCorresponding ? " is-corresponding" : ""}`;
    return `<span class="${escapeAttribute(className)}" title="${escapeAttribute(author.tooltip)}"><span class="author-chip-name">${escapeHtml(name)}</span>${corrBadge}</span>`;
  }).join("");
  if (!chips) return "";
  const total = details.length || fallbackAuthors.length;
  const remainingCount = Math.max(0, total - visibleLimit - supplementalCorresponding.length);
  const remaining = remainingCount > 0 ? `<span class="author-chip muted">+${remainingCount}</span>` : "";
  return `<div class="author-line author-detail-line" aria-label="Author details"><span>${escapeHtml(t("authorsLabel"))}</span><div>${chips}${remaining}</div></div>`;
}

function normalizeAuthorName(name) {
  return String(name || "").trim().toLowerCase();
}

function primaryInstitution(author) {
  const institutions = Array.isArray(author.institutions) ? author.institutions : [];
  const institution = institutions.find((item) => item && item.name);
  return institution ? institution.name : "";
}

function authorSearchText(paper) {
  const details = Array.isArray(paper.author_details) ? paper.author_details : [];
  const corresponding = Array.isArray(paper.corresponding_authors) ? paper.corresponding_authors : [];
  return [...details, ...corresponding].map((author) => {
    const institutions = Array.isArray(author.institutions) ? author.institutions : [];
    return [
      author.name,
      author.orcid,
      author.openalex_author_id,
      author.position,
      institutions.map((institution) => institution.name).join(" "),
      institutions.map((institution) => institution.country_code).join(" "),
      (author.raw_affiliation_strings || []).join(" "),
    ].filter(Boolean).join(" ");
  }).join(" ");
}


function formatSummary(paper) {
  const yearPhrase = paper.year ? `${paper.year}` : "undated";
  const venue = paper.venue || "an unknown venue";
  const tags = representativeTags(paper).map((tag) => displayLabel(tag));
  const tagPhrase = formatEnglishList(tags);
  const score = paper.relevance_score ? `${paper.relevance_score}/10` : "not yet scored";
  const title = paper.title || "This work";

  return `${title} is tracked as a ${yearPhrase} paper from ${venue} related to ${tagPhrase || "manufacturing research"}. Based on public metadata and curated topic signals, its current relevance score for this tracker is ${score}.`;
}

function renderSummaryBlock(paper) {
  const sections = formatSummarySections(paper);
  if (!sections.length) {
    return `<p class="summary">${escapeHtml(formatSummary(paper))}</p>`;
  }

  return `<dl class="summary summary-qa">
    ${sections
      .map(
        (item, index) => `<div class="${index === 4 ? "is-takeaway" : ""}">
          <dt>${escapeHtml(item.question)}</dt>
          <dd>${escapeHtml(item.answer)}</dd>
        </div>`
      )
      .join("")}
  </dl>`;
}

function formatSummarySections(paper) {
  const storedEnglish = parseStoredSummarySections(paper.ai_summary_en || "");
  if (storedEnglish.length) {
    return storedEnglish.map((section, index) => ({
      question: UI_TEXT.en.summaryQuestions[index] || section.question,
      answer: section.answer,
    }));
  }
  return englishSummarySections(paper);
}

function formatSummaryProviderLabel(paper) {
  if (paper.openai_summary_applied === true || paper.summary_provider === "openai") {
    return { text: t("openaiApplied"), title: t("openaiAppliedTitle"), className: "summary-provider-badge is-openai" };
  }
  return { text: t("openaiNotApplied"), title: t("openaiNotAppliedTitle"), className: "summary-provider-badge is-fallback" };
}

function parseStoredSummarySections(summary) {
  const labels = UI_TEXT.en.summaryQuestions;
  const lines = String(summary || "")
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean);
  const sections = [];

  labels.forEach((label, index) => {
    const line = lines.find((item) => item.startsWith(`${index + 1}.`));
    if (!line) return;
    const answer = line
      .replace(/^\d+\.\s*/, "")
      .replace(/^.*?\?\s*/, "")
      .replace(/^(Topic|Problem|Method|Key Result|Takeaway)\s*(?:[-:]\s*)?/i, "")
      .trim();
    if (answer) {
      sections.push({ question: label, answer });
    }
  });

  return sections.length >= 3 ? sections : [];
}

function englishSummarySections(paper) {
  const labels = UI_TEXT.en.summaryQuestions;
  const title = paper.title || "This paper";
  const venue = paper.venue || "an unknown venue";
  const year = paper.year || "undated";
  const tags = representativeTags(paper).map((tag) => displayLabel(tag));
  const tagPhrase = formatEnglishList(tags) || "manufacturing and design";
  const score = paper.relevance_score ? `${paper.relevance_score}/10` : "pending";

  return [
    {
      question: labels[0],
      answer: `${title} is a ${year} paper from ${venue} about ${tagPhrase}.`,
    },
    {
      question: labels[1],
      answer: `It is tracked because it addresses a design or manufacturing limitation related to ${tagPhrase}.`,
    },
    {
      question: labels[2],
      answer: "The detailed method should be checked in the DOI source; this site does not reproduce publisher abstracts.",
    },
    {
      question: labels[3],
      answer: "The key result should be confirmed in the original paper, while this tracker records its topic-level relevance.",
    },
    {
      question: labels[4],
      answer: `The takeaway is that this work is useful comparison literature for ${tagPhrase}; current relevance score is ${score}.`,
    },
  ];
}

function formatRelevanceNote(paper) {
  if (paper.relevance_note_en) return paper.relevance_note_en;
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
    if (!isKnownCanonicalTag(canonical)) return;
    if (canonical === "Digital Twins" && !paperHasCuratedDigitalTwinTag(paper)) return;
    const key = normalizeTopicKey(canonical);
    if (!canonical || seen.has(key)) return;
    seen.add(key);
    picked.push(canonical);
  });

  return rankRepresentativeTags(collapseMaterialExtrusionTags(picked, paper)).slice(0, 3);
}

function rankRepresentativeTags(tags) {
  const specific = tags.filter((tag) => !LOW_SIGNAL_CARD_TAGS.has(tag));
  const broad = tags.filter((tag) => LOW_SIGNAL_CARD_TAGS.has(tag));
  const pool = specific.length >= 3 ? specific : [...specific, ...broad];
  return pool.sort((a, b) => {
    const priorityA = CARD_TAG_PRIORITY.get(a) || 9;
    const priorityB = CARD_TAG_PRIORITY.get(b) || 9;
    if (priorityA !== priorityB) return priorityA - priorityB;
    return a.localeCompare(b, "en");
  });
}

function paperMatchesSidebarSubtopic(paper, field, topic) {
  if (!topic) return true;
  const subtopics = FIELD_SUBTOPICS[field] || [];
  return sidebarBucketForPaper(paper, subtopics) === topic;
}

function paperHasRepresentativeTopic(paper, topic) {
  const target = normalizeTopicKey(canonicalTopicLabel(topic));
  if (target === normalizeTopicKey("Digital Twins")) return paperHasCuratedDigitalTwinTag(paper);
  const candidates = [
    ...(paper.tags || []),
    ...visibleTags(paper),
    ...deriveSubtopics(paper),
  ];
  return candidates.some((tag) => normalizeTopicKey(canonicalTopicLabel(tag)) === target);
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

function paperWithDetails(paper) {
  return { ...paper, ...(state.paperDetails.get(paper.id) || {}) };
}

async function loadPaperDetail(paperId) {
  if (!paperId || state.paperDetails.has(paperId) || state.detailLoading.has(paperId)) return;
  state.detailLoading.add(paperId);
  state.detailErrors.delete(paperId);
  render();
  try {
    const manifest = await loadDetailManifest();
    const chunkName = manifest[paperId];
    if (!chunkName) throw new Error("Detail chunk not found for this paper.");
    const chunk = await loadDetailChunk(chunkName);
    const detail = chunk[paperId];
    if (!detail) throw new Error("Paper detail not found in chunk.");
    state.paperDetails.set(paperId, detail);
  } catch (error) {
    console.error(`Failed to load detail for ${paperId}`, error);
    state.detailErrors.set(paperId, "Could not load details. Try again later.");
  } finally {
    state.detailLoading.delete(paperId);
  }
}

async function loadDetailManifest() {
  if (state.detailManifest) return state.detailManifest;
  const response = await fetch(`${DETAIL_MANIFEST_URL}?ts=${Date.now()}`);
  if (!response.ok) throw new Error(`Detail manifest HTTP ${response.status}`);
  state.detailManifest = await response.json();
  return state.detailManifest;
}

async function loadDetailChunk(chunkName) {
  if (state.detailChunks.has(chunkName)) return state.detailChunks.get(chunkName);
  const response = await fetch(`${DETAILS_BASE_URL}${encodeURIComponent(chunkName)}?ts=${Date.now()}`);
  if (!response.ok) throw new Error(`Detail chunk HTTP ${response.status}`);
  const chunk = await response.json();
  state.detailChunks.set(chunkName, chunk);
  return chunk;
}

function explicitCanonicalAlias(value, text) {
  const raw = String(value || "").trim().toLowerCase();
  if (!raw) return "";

  const checks = [
    [["적층 제조", "additive manufacturing", "3d printing", "3d 프린팅"], "Additive manufacturing"],
    [["디지털 트윈", "digital twin", "digital twins", "digital twinning", "virtual twin", "real-to-twin", "twin-enabled", "twin-driven", "process twin", "machine twin"], "Digital Twins"],
    [["액정 엘라스토머", "액정 고무", "액정 고무체", "liquid crystal elastomer", "lce"], "LCE"],
    [["4d 프린팅", "4d printing", "4d print"], "4D printing"],
    [["메타재료", "메타물질", "metamaterial"], "Metamaterials"],
    [["능동 재료", "능동 소재", "active material", "active materials"], "Active materials"],
    [["스마트 재료", "자극 반응", "stimuli", "stimulus", "responsive"], "Stimuli-responsive"],
    [["형태 변형", "형태 변화", "형상 변형", "shape morph", "morphing"], "Shape morphing"],
    [["툴패스", "toolpath", "tool path"], "Toolpath strategy"],
    [["경로 계획", "path planning", "trajectory"], "Path planning"],
    [["공정 최적화", "제조 최적화", "최적화", "process optimization", "parameter optimization"], "Process optimization"],
    [["재료 전환", "material switching", "purge"], "Material switching"],
    [["소재 분포", "재료 분포", "material distribution"], "Material distribution"],
    [["계산 설계", "계산설계", "설계 자동화", "computational design", "design automation", "generative design"], "Design automation"],
    [["머신러닝", "머신 러닝", "기계 학습", "딥러닝", "강화 학습", "machine learning", "deep learning", "neural", "reinforcement learning"], "Machine learning"],
    [["인공지능", "ai", "artificial intelligence"], "Machine learning"],
    [["제조 자동화", "자동화", "스마트 제조", "manufacturing automation", "automated manufacturing"], "Manufacturing automation"],
    [["자율 실험", "자율 실험실", "self-driving lab", "autonomous laboratory", "bayesian optimization"], "Self-driving Labs"],
    [["로봇 기반 생산제조", "로봇 기반 제조", "robot-based manufacturing", "robotic manufacturing", "robotic fabrication", "robot-assisted manufacturing", "robotic additive manufacturing", "robotic am", "robot-assisted additive", "robotic 3d printing", "robotic 4d printing"], "Robot-based Manufacturing"],
    [["복합재", "복합재료", "복합 재료", "composite", "composites"], "Composites/Materials"],
    [["지속 가능성", "지속가능성", "재활용", "sustainability", "recycling", "circular"], "Sustainability"],
    [["stereolithography", "stereo lithography"], "SLA"],
    [["vat photopolymerization", "vat photopolymerisation", "vat polymerization", "vat polymerisation"], "Vat photopolymerization"],
    [["디지털 광 처리", "digital light process", "digital light processing", "digital light projection", "dlp"], "DLP"],
    [["물성 제어", "property control", "crystallinity", "결정화도"], "Material property control"],
    [["나노", "마이크로", "nanowriting", "micro", "nano"], "Micro/Nano manufacturing"],
    [["기능성 구배", "구배 재료", "functionally graded", "fgam"], "FGAM"],
    [["다중재료", "다중 재료", "multi-material", "multimaterial", "mmam"], "MMAM"],
    [["volumetric additive manufacturing", "volumetric am", "volumetric printing", "computed axial lithography", "tomographic printing", "tomographic volumetric", "xolography"], "Volumetric AM"],
    [["소프트 로보틱스", "소프트 로봇", "소프트 액추에이터", "soft robotics", "soft robotic", "soft gripper", "soft finger", "fin-ray", "fin ray", "pneumatic actuator"], "Soft robotics"],
    [["fdm", "fused deposition", "material extrusion", "filament"], "FDM/Material extrusion"],
    [["dm filament", "digital material", "blended fdm"], "DM filament"],
    [["리뷰", "review", "survey"], "Review"],
  ];

  for (const [needles, canonical] of checks) {
    if (needles.some((needle) => raw.includes(needle) || text.includes(normalize(needle)))) {
      return canonical;
    }
  }
  return "";
}

function canonicalTopicLabel(tag) {
  const value = String(tag || "").trim();
  const text = normalize(value);
  if (!value) return "";
  const explicit = explicitCanonicalAlias(value, text);
  if (explicit) return explicit;
  if (hasAny(text, ["multi-material", "multi material", "multimaterial", "mmam", "다중재료", "다중 재료"])) return "MMAM";
  if (hasAny(text, ["volumetric additive manufacturing", "volumetric am", "volumetric printing", "computed axial lithography", "tomographic printing", "tomographic volumetric", "xolography"])) return "Volumetric AM";
  if (hasAny(text, ["소프트 로보틱스", "소프트 로봇", "소프트 액추에이터", "soft robotics", "soft robotic", "soft gripper", "soft finger", "fin-ray", "fin ray", "pneumatic actuator"])) return "Soft robotics";
  if (hasAny(text, ["functionally graded", "functional gradient", "graded material", "fgam", "기능성 구배", "구배"])) return "FGAM";
  if (hasAny(text, ["dm filament", "digital material", "blended fdm"])) return "DM filament";
  if (hasAny(text, ["fdm", "fused deposition", "material extrusion"])) return "FDM/Material extrusion";
  if (hasSlaSignal(text)) return "SLA";
  if (hasAny(text, ["vat photopolymerization", "vat photopolymerisation", "vat polymerization", "vat polymerisation"])) return "Vat photopolymerization";
  if (hasAny(text, ["dlp", "digital light process", "digital light processing", "digital light projection", "디지털 광 처리"])) return "DLP";
  if (hasAny(text, ["lce", "liquid crystal elastomer", "liquid-crystal elastomer"])) return "LCE";
  if (hasAny(text, ["metamaterial", "metamaterials", "mechanical metamaterial", "메타물질"])) return "Metamaterials";
  if (hasAny(text, ["4d printing", "4d printed", "4d-printed", "4d print", "4d 프린팅"])) return "4D printing";
  if (hasAny(text, ["active material", "active materials", "actuator", "actuation", "능동 재료"])) return "Active materials";
  if (hasAny(text, ["digital fabrication", "digital tectonics", "digital craftsmanship", "디지털 제작"])) return "Digital fabrication";
  if (hasAny(text, ["toolpath strategy", "toolpath", "툴패스", "툴패스 전략"])) return "Toolpath strategy";
  if (hasAny(text, ["material behavior", "material behaviour", "material intelligence", "재료 거동"])) return "Material behavior";
  if (hasAny(text, ["path planning", "trajectory", "graph search", "경로계획", "경로 계획", "그래프 탐색"])) return "Path planning";
  if (hasAny(text, ["process optimization", "process optimisation", "parameter optimization", "parameter optimisation", "공정 최적화"])) return "Process optimization";
  if (hasAny(text, ["robotic autonomous experimentation", "self-driving lab", "self driving lab", "self-driving laboratory", "autonomous laboratory", "autonomous lab", "autonomous experimentation", "autonomous experiment", "closed-loop experimentation", "closed loop experimentation", "closed-loop experiment", "robotic experiment", "robot scientist", "active learning", "bayesian optimization", "자율 실험실", "자동화 실험", "로봇 자율 실험"])) {
    return "Self-driving Labs";
  }
  if (hasAny(text, ["digital twin", "digital twins", "digital-twin", "digital-twins", "digital twinning", "virtual twin", "real-to-twin", "twin-enabled", "twin-driven", "process twin", "machine twin", "디지털 트윈"])) return "Digital Twins";
  if (hasAny(text, ["design automation", "computational design", "generative design", "topology optimization", "계산설계", "설계 자동화"])) return "Design automation";
  if (hasAny(text, ["manufacturing automation", "automated manufacturing", "factory automation", "process automation", "production automation", "automation", "automated", "autonomous", "closed-loop", "closed loop", "monitoring", "in-situ", "in situ", "제조 자동화", "생산 자동화", "공정 자동화", "자동화", "자율", "모니터링"])) return "Manufacturing automation";
  if (hasAny(text, ["machine learning", "deep learning", "reinforcement learning", "ai/ml", "머신러닝", "머신 러닝", "기계 학습", "딥러닝", "강화 학습", "인공지능"])) return "Machine learning";
  if (hasAny(text, ["review", "survey", "리뷰", "서베이"])) return "Review";
  if (hasAny(text, ["material distribution", "재료분포", "재료 분포"])) return "Material distribution";
  if (hasAny(text, ["material switching", "purge", "재료 전환", "퍼지"])) return "Material switching";
  if (hasAny(text, ["honeycomb", "벌집"])) return "Honeycomb";
  if (hasAny(text, ["energy absorption", "energy dissipation", "에너지 소산", "에너지 흡수"])) return "Energy absorption";
  if (hasAny(text, ["reusable", "reusability", "재사용"])) return "Reusability";
  if (hasAny(text, ["additive manufacturing", "3d printing", "3d 프린팅", "적층제조"])) return "Additive manufacturing";
  return value;
}

function isKnownCanonicalTag(tag) {
  return Boolean(TAG_LABELS.en && TAG_LABELS.en[tag]);
}

function normalizeTopicKey(tag) {
  return normalize(tag).replace(/[^a-z0-9가-힣]+/g, "");
}

function visibleTags(paper) {
  const categories = new Set(paper.categories || []);
  const seen = new Set();
  const cleaned = [];
  (paper.tags || []).forEach((tag) => {
    const canonical = canonicalTopicLabel(tag);
    if (!isKnownCanonicalTag(canonical)) return;
    if (canonical === "Digital Twins" && !paperHasCuratedDigitalTwinTag(paper)) return;
    const key = normalizeTopicKey(canonical);
    if (!canonical || seen.has(key)) return;
    seen.add(key);
    if (categories.has(canonical)) return;
    const aliasCategory = TAG_CATEGORY_ALIASES[canonical];
    if (aliasCategory && categories.has(aliasCategory)) return false;
    cleaned.push(canonical);
  });
  return cleaned;
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
  return `${authors.slice(0, 3).join(", ")} et al.`;
}

function categoryIndex(category) {
  const index = FIELD_ORDER.indexOf(category);
  return index === -1 ? FIELD_ORDER.length : index;
}

function deriveField(paper) {
  const titleText = normalize([paper.title, paper.venue].join(" "));
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
  if (
    titleText.includes("ai/ml") ||
    titleText.includes("machine learning") ||
    titleText.includes("deep learning") ||
    titleText.includes("reinforcement learning") ||
    titleText.includes("artificial intelligence") ||
    titleText.includes("neural") ||
    titleText.includes("self-driving lab") ||
    titleText.includes("self driving lab") ||
    titleText.includes("self-driving laboratory") ||
    titleText.includes("autonomous laboratory") ||
    titleText.includes("autonomous lab") ||
    titleText.includes("closed-loop experimentation") ||
    titleText.includes("closed loop experimentation") ||
    titleText.includes("autonomous experimentation") ||
    titleText.includes("active learning") ||
    titleText.includes("bayesian optimization") ||
    titleText.includes("digital twin") ||
    titleText.includes("digital twins") ||
    titleText.includes("virtual twin") ||
    titleText.includes("디지털 트윈") ||
    titleText.includes("머신러닝") ||
    titleText.includes("인공지능") ||
    categoryText.includes("ai")
  ) {
    return "AI 생산제조";
  }
  if (
    titleText.includes("robot") ||
    titleText.includes("soft robotic") ||
    titleText.includes("soft gripper") ||
    titleText.includes("soft finger") ||
    titleText.includes("fin-ray") ||
    titleText.includes("fin ray") ||
    titleText.includes("pneumatic actuator") ||
    titleText.includes("로봇")
  ) {
    return "로봇틱스(생산제조)";
  }
  if (
    titleText.includes("additive manufacturing") ||
    titleText.includes("volumetric additive manufacturing") ||
    titleText.includes("volumetric printing") ||
    titleText.includes("computed axial lithography") ||
    titleText.includes("tomographic printing") ||
    titleText.includes("tomographic volumetric") ||
    titleText.includes("xolography") ||
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
    titleText.includes("digital light process") ||
    titleText.includes("digital light processing") ||
    titleText.includes("digital light projection") ||
    titleText.includes("dlp") ||
    titleText.includes("vat photopolymerization") ||
    titleText.includes("vat photopolymerisation") ||
    titleText.includes("vat polymerization") ||
    titleText.includes("vat polymerisation") ||
    titleText.includes("stereolithography") ||
    hasSlaSignal(titleText) ||
    titleText.includes("다중재료") ||
    titleText.includes("기능성 구배") ||
    titleText.includes("툴패스") ||
    titleText.includes("재료 전환") ||
    titleText.includes("3d 프린팅")
  ) {
    return "3D 프린팅";
  }
  if (
    titleText.includes("design automation") ||
    titleText.includes("computational design") ||
    titleText.includes("generative design") ||
    titleText.includes("topology optimization") ||
    titleText.includes("설계 자동화") ||
    titleText.includes("계산설계")
  ) {
    return "AI 생산제조";
  }
  if (
    text.includes("manufacturing") ||
    text.includes("production") ||
    text.includes("process") ||
    text.includes("construction") ||
    text.includes("fabrication") ||
    text.includes("제조") ||
    text.includes("생산")
  ) {
    return "생산/제조";
  }
  return "생산/제조";
}

function paperHasDigitalTwinSignal(paper) {
  const text = normalize([paper.title, paper.venue].join(" "));
  return hasAny(text, [
    "digital twin",
    "digital twins",
    "digital-twin",
    "digital-twins",
    "digital twinning",
    "virtual twin",
    "real-to-twin",
    "twin-enabled",
    "twin-driven",
    "process twin",
    "machine twin",
    "디지털 트윈",
  ]);
}

function paperHasCuratedDigitalTwinTag(paper) {
  return (paper.tags || []).some((tag) => String(tag || "").trim() === "Digital Twins");
}

function paperHasManufacturingDigitalTwinSignal(paper) {
  if (!paperHasDigitalTwinSignal(paper)) return false;
  const text = normalize([paper.title, paper.venue].join(" "));
  const excludedNonManufacturing = hasAny(text, [
    "urban",
    "city",
    "cities",
    "mobility",
    "supply chain",
    "pharma",
    "healthcare",
    "medical",
    "agricultural",
    "agriculture",
    "wheat",
    "crop",
    "air handling",
    "indoor",
  ]);
  const domainSignal = hasAny(text, [
    "manufacturing",
    "production",
    "additive manufacturing",
    "3d printing",
    "3-d printing",
    "4d printing",
    "4-d printing",
    "printing",
    "printed",
    "fabrication",
    "robot",
    "robotic",
    "automation",
    "automated",
    "assembly",
    "machining",
    "welding",
    "factory",
    "industrial",
    "quality",
    "powder bed",
    "laser powder",
    "lpbf",
    "fused filament",
    "fff",
    "fdm",
    "material extrusion",
    "wire arc",
    "waam",
    "directed energy",
    "ded",
    "binder jet",
    "vat photopolymer",
    "stereolithography",
    "dlp",
    "cnc",
  ]);
  return domainSignal && !excludedNonManufacturing;
}

function deriveSubtopics(paper) {
  const text = normalize(
    [
      paper.title,
      paper.venue,
      (paper.tags || []).join(" "),
    ].join(" ")
  );
  const subtopics = new Set();

  if (hasAny(text, ["process", "parameter", "optimization", "path planning", "trajectory", "공정", "최적화", "경로계획", "경로 계획"])) {
    subtopics.add("공정 최적화");
  }
  if (hasAny(text, ["construction", "large-scale", "concrete", "building", "건설", "대형"])) subtopics.add("건설/대형 제조");
  if (hasAny(text, ["composite", "fiber", "polymer", "복합재", "섬유", "고분자"])) subtopics.add("복합재/소재 제조");

  if (hasAny(text, ["multi-material", "multimaterial", "mmam", "multi material", "다중재료"])) subtopics.add("MMAM");
  if (hasAny(text, ["functionally graded", "fgam", "graded", "gradient", "기능성 구배", "구배"])) subtopics.add("FGAM");
  if (hasAny(text, ["volumetric additive manufacturing", "volumetric am", "volumetric printing", "computed axial lithography", "tomographic printing", "tomographic volumetric", "xolography"])) subtopics.add("Volumetric AM");
  if (hasAny(text, ["dm filament", "digital material", "blended fdm", "디지털 재료"])) subtopics.add("DM filament");
  if (hasAny(text, ["fdm", "fused deposition", "material extrusion", "filament", "압출"])) subtopics.add("FDM/Material extrusion");
  if (hasAny(text, ["dlp", "digital light process", "digital light processing", "digital light projection", "디지털 광 처리"])) subtopics.add("DLP");
  if (hasSlaSignal(text)) subtopics.add("SLA");
  if (hasAny(text, ["vat photopolymerization", "vat photopolymerisation", "vat polymerization", "vat polymerisation"])) subtopics.add("Vat photopolymerization");
  if (hasAny(text, ["toolpath", "path planning", "graph search", "trajectory", "툴패스", "경로계획", "경로 계획"])) subtopics.add("툴패스");
  if (hasAny(text, ["purge", "switching", "transition", "waste", "퍼지", "재료 전환", "전환"])) subtopics.add("퍼지/재료전환");

  if (hasAny(text, ["4d printing", "4d printed", "4d-printed", "4d print", "4d 프린팅"])) subtopics.add("4D printing");
  if (hasAny(text, ["lce", "liquid crystal elastomer", "liquid-crystal elastomer"])) subtopics.add("LCE");
  if (hasAny(text, ["metamaterial", "metamaterials", "mechanical metamaterial", "메타물질"])) subtopics.add("메타물질");
  if (hasAny(text, ["active material", "active materials", "actuator", "actuation", "액추에이터", "능동 재료"])) subtopics.add("Active materials");
  if (hasAny(text, ["shape morph", "morphing", "shape change", "shape-changing", "형상 변화", "변형"])) subtopics.add("Shape morphing");
  if (hasAny(text, ["stimuli", "stimulus", "responsive", "temperature-responsive", "자극 반응", "반응형"])) subtopics.add("Stimuli-responsive");

  if (
    hasAny(text, ["robot", "robotic", "robot-assisted", "로봇"]) &&
    hasAny(text, ["manufacturing", "production", "fabrication", "assembly", "machining", "welding", "printing", "additive", "제조", "생산", "제작", "조립", "가공"])
  ) {
    subtopics.add("Robot-based Manufacturing");
  }
  if (hasAny(text, ["soft robotics", "soft robotic", "soft gripper", "soft finger", "fin-ray", "fin ray", "pneumatic actuator"])) {
    subtopics.add("Soft robotics");
  }
  if (hasAny(text, ["self-driving lab", "self driving lab", "self-driving laboratory", "autonomous laboratory", "autonomous lab", "autonomous experiment", "autonomous experimentation", "closed-loop experimentation", "closed loop experimentation", "closed-loop experiment", "closed loop experiment", "robot scientist", "active learning", "bayesian optimization", "자율 실험실", "자동화 실험", "자율 실험", "로봇 자율 실험"])) {
    subtopics.add("Self-driving Labs");
  }
  if (hasAny(text, ["automation", "automated", "autonomous", "closed-loop", "closed loop", "monitoring", "in-situ", "in situ", "자동화", "자율", "모니터링"])) {
    subtopics.add("제조 자동화");
  }
  if (hasAny(text, ["path planning", "graph search", "trajectory", "경로계획", "경로 계획"])) subtopics.add("경로계획");

  if (hasAny(text, ["machine learning", "ml", "머신러닝"])) subtopics.add("Machine Learning");
  if (hasAny(text, ["deep learning", "neural", "딥러닝"])) subtopics.add("Deep Learning");
  if (hasAny(text, ["reinforcement learning", "강화학습"])) subtopics.add("Reinforcement Learning");
  if (hasAny(text, ["process control", "monitoring", "closed-loop", "공정제어", "모니터링"])) subtopics.add("AI 공정제어");
  if (paperHasCuratedDigitalTwinTag(paper)) {
    subtopics.add("Digital Twins");
  }
  if (hasAny(text, ["computational design", "generative design", "topology optimization", "design automation", "계산설계", "설계 자동화"])) {
    subtopics.add("설계 자동화");
  }

  return [...subtopics];
}

function hasAny(text, terms) {
  return terms.some((term) => text.includes(normalize(term)));
}

function hasSlaSignal(text) {
  return text.includes("stereolithography") || text.includes("stereo lithography") || /\bsla\b/.test(text);
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
  return (UI_TEXT.en && UI_TEXT.en[key]) || key;
}

function displayLabel(value) {
  if (FIELD_ORDER.includes(value)) {
    return (LABEL_TRANSLATIONS.en && LABEL_TRANSLATIONS.en[value]) || value;
  }
  if (CATEGORY_ORDER.includes(value)) {
    return (LABEL_TRANSLATIONS.en && LABEL_TRANSLATIONS.en[value]) || value;
  }
  const canonical = canonicalTopicLabel(value);
  const tagLabel = TAG_LABELS.en && TAG_LABELS.en[canonical];
  if (tagLabel) return tagLabel;
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
  return displayText(venue || "Venue unknown").trim() || "Venue unknown";
}

function normalizeVenueKey(venue) {
  return normalize(venue).replace(/&amp;/g, "and").replace(/&/g, "and");
}

function matchesTargetVenue(venue, target) {
  return normalizeVenueKey(venue) === normalizeVenueKey(target);
}

function isPriorityVenue(venue) {
  return TARGET_VENUES.some((target) => matchesTargetVenue(venue, target));
}

function shortVenue(venue) {
  venue = displayText(venue);
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
  const parts = new Intl.DateTimeFormat("en-US", {
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

function formatKstTime(value) {
  return formatRunTime(value);
}

function flatten(items) {
  return items.reduce((acc, item) => acc.concat(item), []);
}

function escapeHtml(value) {
  return displayText(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}

function displayText(value) {
  return String(value || "")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#039;|&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}

init();
