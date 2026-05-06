const state = {
  conferences: [],
  query: "",
  field: "all",
  status: "all",
  lastFetchedAt: null,
};

const statusLabels = {
  live: "Live",
  predicted: "Predicted",
  unknown: "Unknown",
};

const dateFormatter = new Intl.DateTimeFormat(undefined, {
  year: "numeric",
  month: "short",
  day: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  timeZoneName: "short",
});

const relativeFormatter = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" });

async function main() {
  bindControls();
  await loadDeadlineData({ disableRefreshButton: false });
}

async function loadDeadlineData({ disableRefreshButton = true } = {}) {
  setRefreshState(disableRefreshButton, "Refreshing latest generated data...");

  try {
    const response = await fetch(`./data/deadlines.json?ts=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Unable to load deadline data: ${response.status}`);
    }

    const payload = await response.json();
    state.conferences = sortByDeadline(payload.conferences || []);
    state.lastFetchedAt = new Date();
    renderGeneratedAt(payload.generated_at);
    renderFieldFilters(state.conferences);
    render();
    setRefreshState(false, `Loaded at ${dateFormatter.format(state.lastFetchedAt)}`);
  } catch (error) {
    setRefreshState(false, "Refresh failed. Please try again.");
    showError(error);
  }
}

function bindControls() {
  document.querySelector("#search").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
  });

  document.querySelector("#status-filter").addEventListener("change", (event) => {
    state.status = event.target.value;
    render();
  });

  document.querySelector("#refresh-data").addEventListener("click", (event) => {
    event.preventDefault();
    loadDeadlineData();
  });
}

function renderFieldFilters(conferences) {
  const fields = Array.from(new Set(conferences.flatMap((conference) => conference.fields))).sort();
  const fieldFilter = document.querySelector("#field-filter");
  const selectedField = state.field;
  fieldFilter.innerHTML = `<option value="all">All areas</option>${fields
    .map((field) => `<option value="${escapeAttribute(field)}">${escapeHtml(field)}</option>`)
    .join("")}`;
  fieldFilter.value = fields.includes(selectedField) ? selectedField : "all";
  state.field = fieldFilter.value;

  if (!fieldFilter.dataset.bound) {
    fieldFilter.addEventListener("change", (event) => {
      state.field = event.target.value;
      render();
    });
    fieldFilter.dataset.bound = "true";
  }
}

function renderGeneratedAt(value) {
  const generatedAt = value ? new Date(value) : null;
  const text = generatedAt ? dateFormatter.format(generatedAt) : "unknown";
  document.querySelector("#updated-at").textContent = text;
  document.querySelector("#updated-at-summary").textContent = text;
}

function render() {
  const filtered = state.conferences.filter((conference) => {
    const haystack = [conference.slug, conference.name, conference.tier, ...(conference.fields || [])]
      .join(" ")
      .toLowerCase();
    const matchesQuery = !state.query || haystack.includes(state.query);
    const matchesField = state.field === "all" || (conference.fields || []).includes(state.field);
    const matchesStatus = state.status === "all" || conference.status === state.status;
    return matchesQuery && matchesField && matchesStatus;
  });

  renderSummary(filtered);
  renderCards(filtered);
}

function renderSummary(conferences) {
  document.querySelector("#conference-count").textContent = String(conferences.length);

  const upcoming = conferences.find((conference) => conference.deadline_utc);
  document.querySelector("#next-deadline").textContent = upcoming
    ? `${upcoming.slug.toUpperCase()} ${formatDateOnly(upcoming.deadline_utc)}`
    : "-";
}

function renderCards(conferences) {
  const container = document.querySelector("#cards");
  const empty = document.querySelector("#empty-state");
  container.innerHTML = "";
  empty.hidden = conferences.length !== 0;

  const template = document.querySelector("#conference-card-template");
  for (const conference of conferences) {
    container.append(renderCard(conference, template));
  }
}

function renderCard(conference, template) {
  const fragment = template.content.cloneNode(true);
  const card = fragment.querySelector(".card");
  const deadline = conference.deadline_utc ? new Date(conference.deadline_utc) : null;
  const sourceUrl = conference.source_url || conference.official_url;

  card.classList.add(`card--${conference.status || "unknown"}`);
  fragment.querySelector(".tag--tier").textContent = conference.tier;
  const statusTag = fragment.querySelector(".tag--status");
  statusTag.textContent = statusLabels[conference.status] || conference.status || "Unknown";
  statusTag.classList.add(`tag--${conference.status || "unknown"}`);
  fragment.querySelector("h2").textContent = conference.slug.toUpperCase();
  fragment.querySelector(".card__fields").textContent = `${conference.name} | ${(conference.fields || []).join(", ")}`;
  fragment.querySelector(".deadline__date").textContent = deadline
    ? dateFormatter.format(deadline)
    : "Unknown";
  fragment.querySelector(".deadline__countdown").textContent = deadline
    ? formatDistance(deadline)
    : "No deadline";
  fragment.querySelector(".card__explanation").textContent = conference.explanation || "";

  const officialLink = fragment.querySelector(".official-link");
  officialLink.href = conference.official_url;

  const sourceLink = fragment.querySelector(".source-link");
  sourceLink.href = sourceUrl;
  sourceLink.hidden = !sourceUrl;

  return fragment;
}

function sortByDeadline(conferences) {
  return [...conferences].sort((left, right) => {
    const leftTime = left.deadline_utc ? Date.parse(left.deadline_utc) : Number.POSITIVE_INFINITY;
    const rightTime = right.deadline_utc ? Date.parse(right.deadline_utc) : Number.POSITIVE_INFINITY;
    return leftTime - rightTime || left.slug.localeCompare(right.slug);
  });
}

function formatDistance(deadline) {
  const diffDays = Math.ceil((deadline.getTime() - Date.now()) / 86_400_000);
  return relativeFormatter.format(diffDays, "day");
}

function formatDateOnly(value) {
  if (!value) {
    return "Unknown";
  }

  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(value));
}

function showError(error) {
  document.querySelector("#cards").innerHTML = `
    <article class="card">
      <h2>Deadline data is not available</h2>
      <p>${escapeHtml(error.message)}</p>
    </article>
  `;
}

function setRefreshState(isRefreshing, message) {
  const button = document.querySelector("#refresh-data");
  const status = document.querySelector("#refresh-status");
  button.disabled = isRefreshing;
  button.textContent = isRefreshing ? "Refreshing..." : "Refresh latest data";
  status.textContent = message;
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

main();
