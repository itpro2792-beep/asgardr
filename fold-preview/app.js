"use strict";

const baseServices = [
  { name: "demo-api-01", host: "demo-node-a", status: "online", cpu: 12, memory: 318, role: "Fixture API renderer" },
  { name: "demo-worker-01", host: "demo-node-a", status: "online", cpu: 31, memory: 522, role: "Synthetic queue worker" },
  { name: "demo-worker-03", host: "demo-node-b", status: "warning", cpu: 72, memory: 684, role: "Intentional warning canary" },
  { name: "demo-events-01", host: "demo-node-b", status: "online", cpu: 8, memory: 211, role: "Frozen event renderer" },
  { name: "demo-jobs-02", host: "demo-node-c", status: "online", cpu: 23, memory: 405, role: "Lifecycle fixture" },
  { name: "demo-archive-01", host: "demo-node-c", status: "offline", cpu: 0, memory: 0, role: "Intentional offline sample" },
  { name: "demo-siren-text", host: "browser-only", status: "online", cpu: 4, memory: 96, role: "Deterministic text simulator" },
  { name: "demo-audit-01", host: "demo-node-d", status: "online", cpu: 15, memory: 274, role: "Local activity renderer" }
];

const fixtures = [
  {
    id: "A-01",
    label: "Balanced baseline",
    heading: "Synthetic fleet is nominal",
    health: 96,
    memory: 61,
    disk: 74,
    queue: { running: 4, pending: 7, done: 128, failed: 1 },
    alert: ["Worker latency above fixture baseline", "demo-worker-03 · synthetic warning · no action available"],
    serviceOverrides: {},
    jobs: [
      { title: "Render synthetic health digest", id: "DEMO-JOB-1042", state: "running", note: "42% · fixture artifact" },
      { title: "Index fictional event bundle", id: "DEMO-JOB-1043", state: "pending", note: "queued locally" },
      { title: "Validate sample identity tuples", id: "DEMO-JOB-1039", state: "succeeded", note: "completed fixture" },
      { title: "Generate visual latency study", id: "DEMO-JOB-1038", state: "failed", note: "intentional demo failure" }
    ],
    events: [
      { severity: "info", type: "FIXTURE_READY", source: "demo-node-a", message: "Synthetic service matrix loaded from browser memory." },
      { severity: "warning", type: "LATENCY_STUDY", source: "demo-node-b", message: "Visual threshold crossed by a fictional worker." },
      { severity: "info", type: "QUEUE_SAMPLE", source: "demo-node-c", message: "Pending fixture count changed for layout testing." },
      { severity: "critical", type: "DRILL_ONLY", source: "demo-node-d", message: "Intentional critical styling sample; no incident exists." }
    ]
  },
  {
    id: "B-02",
    label: "Queue pressure study",
    heading: "Synthetic queue pressure is elevated",
    health: 88,
    memory: 78,
    disk: 65,
    queue: { running: 8, pending: 19, done: 142, failed: 2 },
    alert: ["Demo workers are above fixture baseline", "demo-worker-01 · simulated saturation · no action available"],
    serviceOverrides: {
      "demo-worker-01": { status: "warning", cpu: 88, memory: 792 },
      "demo-worker-03": { status: "warning", cpu: 84, memory: 746 },
      "demo-jobs-02": { status: "warning", cpu: 67, memory: 622 }
    },
    jobs: [
      { title: "Reflow synthetic queue board", id: "DEMO-JOB-2048", state: "running", note: "76% · visual scenario" },
      { title: "Stage fictional event batch", id: "DEMO-JOB-2049", state: "running", note: "31% · browser memory" },
      { title: "Compare queue thresholds", id: "DEMO-JOB-2050", state: "pending", note: "11 items ahead" },
      { title: "Render intentional retry", id: "DEMO-JOB-2041", state: "failed", note: "controlled demo state" }
    ],
    events: [
      { severity: "info", type: "FIXTURE_ROTATED", source: "demo-node-a", message: "Queue-pressure scenario selected locally." },
      { severity: "warning", type: "WORKER_PRESSURE", source: "demo-node-a", message: "Fictional CPU crossed the visual warning line." },
      { severity: "warning", type: "QUEUE_DEPTH", source: "demo-node-c", message: "Pending sample increased to nineteen." },
      { severity: "critical", type: "RETRY_DRILL", source: "demo-node-d", message: "Failure badge is intentional and cannot trigger action." }
    ]
  },
  {
    id: "C-03",
    label: "Recovery baseline",
    heading: "Synthetic recovery is stable",
    health: 98,
    memory: 54,
    disk: 81,
    queue: { running: 2, pending: 1, done: 164, failed: 0 },
    alert: ["No active fixture warnings", "All displayed values remain fictional and local"],
    serviceOverrides: {
      "demo-worker-03": { status: "online", cpu: 34, memory: 501 },
      "demo-archive-01": { status: "online", cpu: 6, memory: 128 },
      "demo-jobs-02": { status: "online", cpu: 14, memory: 338 }
    },
    jobs: [
      { title: "Confirm synthetic recovery", id: "DEMO-JOB-3061", state: "running", note: "92% · fixture artifact" },
      { title: "Archive fictional drill", id: "DEMO-JOB-3060", state: "succeeded", note: "completed locally" },
      { title: "Refresh visual baseline", id: "DEMO-JOB-3059", state: "succeeded", note: "layout sample ready" },
      { title: "Verify empty failure lane", id: "DEMO-JOB-3058", state: "succeeded", note: "zero demo failures" }
    ],
    events: [
      { severity: "info", type: "RECOVERY_READY", source: "demo-node-a", message: "Recovery fixture loaded from browser memory." },
      { severity: "info", type: "QUEUE_DRAINED", source: "demo-node-c", message: "Pending sample returned to one." },
      { severity: "info", type: "CANARY_NOMINAL", source: "demo-node-b", message: "All fictional service badges are online." },
      { severity: "warning", type: "DRILL_CLOSED", source: "demo-node-d", message: "Historical warning retained only for visual comparison." }
    ]
  }
];

const state = {
  fixtureIndex: 0,
  jobState: "all",
  activitySequence: 0,
  activity: [],
  lastInspectorTrigger: null
};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (typeof text === "string") node.textContent = text;
  return node;
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = String(value);
}

function currentFixture() {
  return fixtures[state.fixtureIndex];
}

function currentServices() {
  const overrides = currentFixture().serviceOverrides;
  return baseServices.map((service) => ({ ...service, ...(overrides[service.name] || {}) }));
}

function percent(value) {
  const numeric = Number(value);
  return Math.max(0, Math.min(100, Number.isFinite(numeric) ? numeric : 0));
}

function recordActivity(title, detail) {
  state.activitySequence += 1;
  state.activity.unshift({ sequence: state.activitySequence, title, detail });
  state.activity = state.activity.slice(0, 6);
  renderActivity();
}

function renderActivity() {
  const list = document.getElementById("activity-list");
  list.replaceChildren();
  state.activity.forEach((entry) => {
    const item = element("li", "activity-item");
    const marker = element("span", "activity-marker", `L+${String(entry.sequence).padStart(2, "0")}`);
    const copy = element("div");
    copy.append(element("strong", "", entry.title), element("p", "", entry.detail));
    item.append(marker, copy);
    list.append(item);
  });
}

function renderServices() {
  const grid = document.getElementById("service-grid");
  const empty = document.getElementById("service-empty");
  const search = document.getElementById("service-search").value.trim().toLowerCase();
  const status = document.getElementById("status-filter").value;
  const services = currentServices();
  grid.replaceChildren();
  const matches = services.filter((service) => {
    const textMatch = service.name.includes(search) || service.host.includes(search) || service.role.toLowerCase().includes(search);
    const statusMatch = status === "all" || service.status === status;
    return textMatch && statusMatch;
  });
  matches.forEach((service) => {
    const card = element("button", "service-card");
    card.type = "button";
    card.dataset.serviceName = service.name;
    card.setAttribute("aria-label", `Inspect ${service.name}, ${service.status}`);
    const dot = element("span", `service-dot ${service.status}`);
    dot.setAttribute("aria-hidden", "true");
    const identity = element("span", "service-identity");
    identity.append(element("span", "service-name", service.name), element("span", "service-meta", `${service.host} · ${service.status}`));
    const numbers = element("span", "service-numbers");
    numbers.append(element("strong", "", `${service.cpu}%`), element("strong", "", `${service.memory} MB`), element("span", "", "CPU"), element("span", "", "RAM"));
    card.append(dot, identity, numbers, element("span", "inspect-cue", "Inspect"));
    grid.append(card);
  });
  empty.hidden = matches.length !== 0;
  setText("service-result-status", `${matches.length} synthetic service${matches.length === 1 ? "" : "s"} shown.`);
}

function renderJobs() {
  const list = document.getElementById("job-list");
  const fixture = currentFixture();
  list.replaceChildren();
  fixture.jobs.filter((job) => state.jobState === "all" || job.state === state.jobState).forEach((job) => {
    const row = element("button", "job-row");
    row.type = "button";
    row.dataset.jobId = job.id;
    row.setAttribute("aria-label", `Inspect ${job.title}, ${job.state}`);
    const copy = element("span", "job-copy");
    copy.append(element("strong", "", job.title), element("span", "", `${job.id} · ${job.note}`));
    row.append(copy, element("span", `state-badge ${job.state}`, job.state));
    list.append(row);
  });
  if (!list.childElementCount) list.append(element("p", "empty-state", `No ${state.jobState} jobs in fixture ${fixture.id}.`));
}

function renderEvents() {
  const severity = document.getElementById("event-filter").value;
  const list = document.getElementById("event-list");
  list.replaceChildren();
  const matches = currentFixture().events
    .map((event, index) => ({ ...event, fixtureTime: `T+00:${String(index * 7 + 3).padStart(2, "0")}` }))
    .filter((event) => severity === "all" || event.severity === severity);
  matches.forEach((event) => {
    const row = element("article", "event-row");
    const copy = element("div");
    copy.append(element("strong", "", event.type), element("p", "", `${event.fixtureTime} · ${event.source} · ${event.message}`));
    row.append(element("span", `severity-badge ${event.severity}`, event.severity), copy);
    list.append(row);
  });
  if (!list.childElementCount) list.append(element("p", "empty-state", `No ${severity} events in this fixture.`));
  setText("event-result-status", `${matches.length} synthetic event${matches.length === 1 ? "" : "s"} shown.`);
}

function renderVitals() {
  const fixture = currentFixture();
  const vitals = [
    ["Memory", fixture.memory, `${fixture.memory}%`],
    ["Disk", fixture.disk, `${fixture.disk}%`],
    ["Health", fixture.health, `${fixture.health}%`],
    ["Queue", Math.min(fixture.queue.pending * 5, 100), String(fixture.queue.pending)]
  ];
  const list = document.getElementById("vital-list");
  list.replaceChildren();
  vitals.forEach(([name, value, label]) => {
    const row = element("div", "vital-row");
    const meter = element("div", "mini-meter");
    const fill = element("span");
    const bounded = percent(value);
    fill.style.setProperty("--value", `${bounded}%`);
    fill.setAttribute("role", "progressbar");
    fill.setAttribute("aria-label", `Synthetic ${name.toLowerCase()}`);
    fill.setAttribute("aria-valuemin", "0");
    fill.setAttribute("aria-valuemax", "100");
    fill.setAttribute("aria-valuenow", String(bounded));
    meter.append(fill);
    row.append(element("span", "", name), meter, element("strong", "", label));
    list.append(row);
  });
}

function updateFixture({ announce = false } = {}) {
  const fixture = currentFixture();
  setText("cover-heading", fixture.heading);
  setText("health-score", fixture.health);
  setText("memory-label", `${fixture.memory}%`);
  setText("disk-label", `${fixture.disk}%`);
  setText("memory-copy", `${(fixture.memory * 0.3).toFixed(1)} / 30.0 GB fixture`);
  setText("disk-copy", `${Math.round(fixture.disk * 3)} / 300 GB fixture`);
  const memory = percent(fixture.memory);
  const disk = percent(fixture.disk);
  document.getElementById("memory-meter").style.setProperty("--value", `${memory}%`);
  document.getElementById("memory-meter").setAttribute("aria-valuenow", String(memory));
  document.getElementById("disk-meter").style.setProperty("--value", `${disk}%`);
  document.getElementById("disk-meter").setAttribute("aria-valuenow", String(disk));
  setText("queue-running", fixture.queue.running);
  setText("queue-pending", fixture.queue.pending);
  setText("queue-done", fixture.queue.done);
  setText("queue-failed", fixture.queue.failed);
  setText("cover-alert-title", fixture.alert[0]);
  setText("cover-alert-copy", fixture.alert[1]);
  setText("fixture-number", `${fixture.id} · ${fixture.label}`);
  document.getElementById("health-ring").setAttribute("aria-label", `Demo health score ${fixture.health} percent`);
  renderServices();
  renderJobs();
  renderEvents();
  renderVitals();
  if (announce) recordActivity("Fixture rotated", `${fixture.id} · ${fixture.label}; every synthetic panel refreshed.`);
  scheduleLayoutScan();
}

function addMessage(text, role) {
  const transcript = document.getElementById("transcript");
  transcript.append(element("div", `message ${role}`, text));
  while (transcript.childElementCount > 40) transcript.firstElementChild.remove();
  transcript.scrollTop = transcript.scrollHeight;
}

function simulateSiren(query) {
  const clean = query.trim();
  if (!clean) return;
  const fixture = currentFixture();
  addMessage(clean, "user");
  let response = `Fixture ${fixture.id} is a ${fixture.label.toLowerCase()} with ${fixture.queue.pending} pending demo jobs.`;
  const normalized = clean.toLowerCase();
  if (normalized.includes("health")) response = `Fixture ${fixture.id} health is ${fixture.health}%. Memory is ${fixture.memory}% and disk headroom is ${fixture.disk}%.`;
  if (normalized.includes("warning")) response = `${fixture.alert[0]}. ${fixture.alert[1]}.`;
  if (normalized.includes("privacy")) response = "This preview contains no live identifiers, credentials, API or background connections, persistent storage, microphone access, or controller functions.";
  if (normalized.includes("layout")) response = "Use Device QA to scan visible rails for horizontal overflow. The scan reads local element dimensions only.";
  addMessage(`SIMULATED RESPONSE — ${response}`, "assistant");
  document.getElementById("siren-input").value = "";
  recordActivity("Siren simulated", `Answered a local query against fixture ${fixture.id}.`);
}

function setLayout(layout, { announce = true } = {}) {
  const shell = document.getElementById("app-shell");
  shell.dataset.layout = layout;
  document.querySelectorAll("[data-layout-choice]").forEach((peer) => {
    const active = peer.dataset.layoutChoice === layout;
    peer.classList.toggle("is-active", active);
    peer.setAttribute("aria-pressed", String(active));
  });
  const label = layout === "auto" ? "Auto layout" : `${layout === "inner" ? "Unfolded" : "Cover"} preview forced`;
  setText("viewport-note", label);
  if (announce) recordActivity("Layout changed", label);
  scheduleLayoutScan();
}

function activateJobTab(button, { focus = false, announce = true } = {}) {
  document.querySelectorAll("[data-job-state]").forEach((peer) => {
    const active = peer === button;
    peer.classList.toggle("is-active", active);
    peer.setAttribute("aria-selected", String(active));
    peer.tabIndex = active ? 0 : -1;
  });
  state.jobState = button.dataset.jobState;
  document.getElementById("job-list").setAttribute("aria-labelledby", button.id);
  renderJobs();
  if (focus) button.focus();
  if (announce) recordActivity("Job view filtered", `${button.textContent} jobs selected.`);
}

function inspectorField(term, description) {
  const wrapper = element("div");
  wrapper.append(element("dt", "", term), element("dd", "", description));
  return wrapper;
}

function showInspector({ kicker, title, summary, fields }, trigger) {
  const dialog = document.getElementById("inspector-dialog");
  setText("inspector-kicker", kicker);
  setText("inspector-title", title);
  setText("inspector-summary", summary);
  const grid = document.getElementById("inspector-grid");
  grid.replaceChildren(...fields.map(([term, description]) => inspectorField(term, String(description))));
  state.lastInspectorTrigger = trigger;
  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "");
  document.getElementById("close-inspector").focus();
}

function inspectService(name, trigger) {
  const service = currentServices().find((item) => item.name === name);
  if (!service) return;
  showInspector({
    kicker: "SERVICE FIXTURE",
    title: service.name,
    summary: service.role,
    fields: [["State", service.status], ["Fixture host", service.host], ["CPU sample", `${service.cpu}%`], ["Memory sample", `${service.memory} MB`], ["Scenario", currentFixture().label], ["Capability", "Display only"]]
  }, trigger);
  recordActivity("Service inspected", `${service.name} opened in the read-only fixture inspector.`);
}

function inspectJob(id, trigger) {
  const job = currentFixture().jobs.find((item) => item.id === id);
  if (!job) return;
  showInspector({
    kicker: "JOB FIXTURE",
    title: job.title,
    summary: "A fictional lifecycle artifact with no scheduler or execution path.",
    fields: [["Fixture ID", job.id], ["State", job.state], ["Detail", job.note], ["Scenario", currentFixture().label], ["Queue source", "Browser memory"], ["Capability", "Display only"]]
  }, trigger);
  recordActivity("Job inspected", `${job.id} opened in the read-only fixture inspector.`);
}

function effectiveView() {
  const shell = document.getElementById("app-shell");
  if (shell.dataset.layout === "cover") return "Cover (forced)";
  if (shell.dataset.layout === "inner") return "Unfolded (forced)";
  return shell.clientWidth >= 720 ? "Unfolded (auto)" : "Cover (auto)";
}

function visible(node) {
  return Boolean(node && node.getClientRects().length);
}

function runLayoutScan({ announce = true } = {}) {
  const root = document.documentElement;
  const visual = window.visualViewport;
  const checks = [
    ["Truth banner", ".safety-banner"],
    ["Preview toolbar", ".preview-toolbar"],
    ["Cover canvas", ".cover-view"],
    ["Service matrix", ".service-grid"],
    ["Service filters", ".filter-row"],
    ["Job tabs", ".tab-list"],
    ["Siren query", ".query-row"],
    ["Device stats", ".device-stats"]
  ];
  const issues = [];
  let checked = 1;
  if (root.scrollWidth > root.clientWidth + 1) issues.push("Page root");
  checks.forEach(([label, selector]) => {
    const node = document.querySelector(selector);
    if (!visible(node)) return;
    checked += 1;
    if (node.scrollWidth > node.clientWidth + 1) issues.push(label);
  });
  const passed = issues.length === 0;
  setText("layout-viewport", `${root.clientWidth} × ${root.clientHeight} CSS px`);
  setText("visual-viewport", visual ? `${Math.round(visual.width)} × ${Math.round(visual.height)} CSS px` : "Not exposed");
  setText("effective-view", effectiveView());
  setText("page-fit", passed ? `PASS · ${checked} checks` : `REVIEW · ${issues.length} issue${issues.length === 1 ? "" : "s"}`);
  const badge = document.getElementById("fit-badge");
  badge.className = `fit-badge ${passed ? "pass" : "review"}`;
  badge.textContent = passed ? "FIT PASS" : "REVIEW";
  const results = document.getElementById("scan-results");
  results.replaceChildren();
  if (passed) results.append(element("p", "scan-pass", `PASS — all ${checked} visible layout rails fit this viewport.`));
  else {
    results.append(element("p", "scan-review", "Review horizontal fit for:"));
    const list = element("ul");
    issues.forEach((issue) => list.append(element("li", "", issue)));
    results.append(list);
  }
  setText("cover-fit-result", passed ? `PASS · ${root.clientWidth}px viewport` : `REVIEW · ${issues.join(", ")}`);
  if (announce) recordActivity("Device fit scanned", `${passed ? "PASS" : "REVIEW"} at ${root.clientWidth} × ${root.clientHeight} CSS px.`);
  return passed;
}

let scanTimer = 0;
function scheduleLayoutScan() {
  window.clearTimeout(scanTimer);
  scanTimer = window.setTimeout(() => runLayoutScan({ announce: false }), 120);
}

document.querySelectorAll("[data-layout-choice]").forEach((button) => {
  button.addEventListener("click", () => setLayout(button.dataset.layoutChoice));
});

document.getElementById("rotate-fixture").addEventListener("click", () => {
  state.fixtureIndex = (state.fixtureIndex + 1) % fixtures.length;
  updateFixture({ announce: true });
});

document.getElementById("service-search").addEventListener("input", renderServices);
document.getElementById("status-filter").addEventListener("change", (event) => {
  renderServices();
  recordActivity("Service status filtered", `${event.target.options[event.target.selectedIndex].text} selected.`);
});
document.getElementById("event-filter").addEventListener("change", (event) => {
  renderEvents();
  recordActivity("Event severity filtered", `${event.target.options[event.target.selectedIndex].text} selected.`);
});

document.querySelectorAll("[data-job-state]").forEach((button) => {
  button.addEventListener("click", () => activateJobTab(button));
  button.addEventListener("keydown", (event) => {
    const tabs = [...document.querySelectorAll("[data-job-state]")];
    const current = tabs.indexOf(event.currentTarget);
    let next = null;
    if (event.key === "ArrowRight") next = (current + 1) % tabs.length;
    if (event.key === "ArrowLeft") next = (current - 1 + tabs.length) % tabs.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = tabs.length - 1;
    if (next !== null) {
      event.preventDefault();
      activateJobTab(tabs[next], { focus: true });
    }
  });
});

document.getElementById("service-grid").addEventListener("click", (event) => {
  const card = event.target.closest("[data-service-name]");
  if (card) inspectService(card.dataset.serviceName, card);
});
document.getElementById("job-list").addEventListener("click", (event) => {
  const row = event.target.closest("[data-job-id]");
  if (row) inspectJob(row.dataset.jobId, row);
});

document.getElementById("open-siren").addEventListener("click", () => {
  setLayout("inner");
  document.getElementById("siren-panel").scrollIntoView({ behavior: "auto", block: "center" });
  document.getElementById("siren-input").focus({ preventScroll: true });
});

document.getElementById("siren-send").addEventListener("click", () => simulateSiren(document.getElementById("siren-input").value));
document.getElementById("siren-input").addEventListener("keydown", (event) => {
  if (event.key === "Enter") simulateSiren(event.currentTarget.value);
});
document.querySelectorAll("[data-query]").forEach((button) => button.addEventListener("click", () => simulateSiren(button.dataset.query)));

const dialog = document.getElementById("inspector-dialog");
document.getElementById("close-inspector").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});
dialog.addEventListener("close", () => {
  if (state.lastInspectorTrigger && document.contains(state.lastInspectorTrigger)) state.lastInspectorTrigger.focus();
});

document.getElementById("run-scan").addEventListener("click", () => runLayoutScan());
document.getElementById("cover-scan").addEventListener("click", () => runLayoutScan());
window.addEventListener("resize", scheduleLayoutScan, { passive: true });
if (window.visualViewport) window.visualViewport.addEventListener("resize", scheduleLayoutScan, { passive: true });

recordActivity("Preview ready", "Synthetic canary V2 loaded; all state is browser-memory only.");
addMessage("Siren text simulator ready. Everything here is fictional and stays in this tab.", "assistant");
activateJobTab(document.getElementById("job-tab-all"), { announce: false });
updateFixture();
scheduleLayoutScan();
