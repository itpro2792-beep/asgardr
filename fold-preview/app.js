"use strict";

const fixtures = [
  {
    id: "A-01",
    health: 96,
    memory: 61,
    disk: 74,
    queue: { running: 4, pending: 7, done: 128, failed: 1 },
    alert: ["Worker latency above fixture baseline", "demo-worker-03 · synthetic warning · no action available"]
  },
  {
    id: "B-02",
    health: 91,
    memory: 68,
    disk: 70,
    queue: { running: 6, pending: 11, done: 142, failed: 2 },
    alert: ["Synthetic queue pressure is elevated", "demo-queue-02 · visual scenario · no action available"]
  },
  {
    id: "C-03",
    health: 98,
    memory: 55,
    disk: 77,
    queue: { running: 3, pending: 2, done: 155, failed: 0 },
    alert: ["No active fixture warnings", "All displayed values remain fictional and local"]
  }
];

const services = [
  { name: "demo-api-01", host: "demo-node-a", status: "online", cpu: 12, memory: 318 },
  { name: "demo-worker-01", host: "demo-node-a", status: "online", cpu: 31, memory: 522 },
  { name: "demo-worker-03", host: "demo-node-b", status: "warning", cpu: 72, memory: 684 },
  { name: "demo-events-01", host: "demo-node-b", status: "online", cpu: 8, memory: 211 },
  { name: "demo-jobs-02", host: "demo-node-c", status: "online", cpu: 23, memory: 405 },
  { name: "demo-archive-01", host: "demo-node-c", status: "offline", cpu: 0, memory: 0 },
  { name: "demo-siren-text", host: "browser-only", status: "online", cpu: 4, memory: 96 },
  { name: "demo-audit-01", host: "demo-node-d", status: "online", cpu: 15, memory: 274 }
];

const jobs = [
  { title: "Render synthetic health digest", id: "DEMO-JOB-1042", state: "running", note: "42% · fixture artifact" },
  { title: "Index fictional event bundle", id: "DEMO-JOB-1043", state: "pending", note: "queued locally" },
  { title: "Validate sample identity tuples", id: "DEMO-JOB-1039", state: "succeeded", note: "completed fixture" },
  { title: "Generate visual latency study", id: "DEMO-JOB-1038", state: "failed", note: "intentional demo failure" }
];

const events = [
  { severity: "info", type: "FIXTURE_READY", source: "demo-node-a", message: "Synthetic service matrix loaded from browser memory." },
  { severity: "warning", type: "LATENCY_STUDY", source: "demo-node-b", message: "Visual threshold crossed by a fictional worker." },
  { severity: "info", type: "QUEUE_SAMPLE", source: "demo-node-c", message: "Pending fixture count changed for layout testing." },
  { severity: "critical", type: "DRILL_ONLY", source: "demo-node-d", message: "Intentional critical styling sample; no incident exists." }
];

const vitals = [
  ["Memory", 61, "61%"],
  ["Disk", 74, "74%"],
  ["Commit", 63, "63%"],
  ["Latency", 36, "18ms"]
];

let fixtureIndex = 0;

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

function renderServices() {
  const grid = document.getElementById("service-grid");
  const empty = document.getElementById("service-empty");
  const search = document.getElementById("service-search").value.trim().toLowerCase();
  const status = document.getElementById("status-filter").value;
  grid.replaceChildren();
  const matches = services.filter((service) => {
    const textMatch = service.name.includes(search) || service.host.includes(search);
    const statusMatch = status === "all" || service.status === status;
    return textMatch && statusMatch;
  });
  matches.forEach((service) => {
    const card = element("article", "service-card");
    const dot = element("span", `service-dot ${service.status}`);
    dot.setAttribute("aria-label", service.status);
    const identity = element("div");
    identity.append(element("div", "service-name", service.name), element("p", "service-meta", `${service.host} · fixture`));
    const numbers = element("div", "service-numbers");
    numbers.append(element("strong", "", `${service.cpu}%`), element("strong", "", `${service.memory} MB`), element("span", "", "CPU"), element("span", "", "RAM"));
    card.append(dot, identity, numbers);
    grid.append(card);
  });
  empty.hidden = matches.length !== 0;
}

function renderJobs(state = "all") {
  const list = document.getElementById("job-list");
  list.replaceChildren();
  jobs.filter((job) => state === "all" || job.state === state).forEach((job) => {
    const row = element("article", "job-row");
    const copy = element("div");
    copy.append(element("strong", "", job.title), element("p", "", `${job.id} · ${job.note}`));
    row.append(copy, element("span", `state-badge ${job.state}`, job.state));
    list.append(row);
  });
}

function renderEvents(severity = "all") {
  const list = document.getElementById("event-list");
  list.replaceChildren();
  events.filter((event) => severity === "all" || event.severity === severity).forEach((event, index) => {
    const row = element("article", "event-row");
    const copy = element("div");
    copy.append(element("strong", "", event.type), element("p", "", `T+00:${String(index * 7 + 3).padStart(2, "0")} · ${event.source} · ${event.message}`));
    row.append(element("span", `severity-badge ${event.severity}`, event.severity), copy);
    list.append(row);
  });
}

function renderVitals() {
  const list = document.getElementById("vital-list");
  list.replaceChildren();
  vitals.forEach(([name, value, label]) => {
    const row = element("div", "vital-row");
    const meter = element("div", "mini-meter");
    const fill = element("span");
    fill.style.setProperty("--value", `${value}%`);
    meter.append(fill);
    row.append(element("span", "", name), meter, element("strong", "", label));
    list.append(row);
  });
}

function updateFixture() {
  const fixture = fixtures[fixtureIndex];
  setText("health-score", fixture.health);
  setText("memory-label", `${fixture.memory}%`);
  setText("disk-label", `${fixture.disk}%`);
  document.getElementById("memory-meter").style.setProperty("--value", `${fixture.memory}%`);
  document.getElementById("disk-meter").style.setProperty("--value", `${fixture.disk}%`);
  setText("queue-running", fixture.queue.running);
  setText("queue-pending", fixture.queue.pending);
  setText("queue-done", fixture.queue.done);
  setText("queue-failed", fixture.queue.failed);
  setText("cover-alert-title", fixture.alert[0]);
  setText("cover-alert-copy", fixture.alert[1]);
  setText("fixture-number", fixture.id);
  document.getElementById("health-ring").setAttribute("aria-label", `Demo health score ${fixture.health} percent`);
}

function addMessage(text, role) {
  const transcript = document.getElementById("transcript");
  transcript.append(element("div", `message ${role}`, text));
  transcript.scrollTop = transcript.scrollHeight;
}

function simulateSiren(query) {
  const clean = query.trim();
  if (!clean) return;
  addMessage(clean, "user");
  let response = "This simulator can describe only the fictional values visible on this page.";
  const normalized = clean.toLowerCase();
  if (normalized.includes("health")) response = "Fixture health is visually nominal. One intentional warning remains so you can judge alert hierarchy on the Fold.";
  if (normalized.includes("warning")) response = "The demo warning is attached to demo-worker-03. It is browser-only text and has no operational target.";
  if (normalized.includes("privacy")) response = "This preview contains no live identifiers, credentials, network calls, storage, microphone access, or controller functions.";
  addMessage(response, "assistant");
  document.getElementById("siren-input").value = "";
}

document.querySelectorAll("[data-layout-choice]").forEach((button) => {
  button.addEventListener("click", () => {
    const layout = button.dataset.layoutChoice;
    document.getElementById("app-shell").dataset.layout = layout;
    document.querySelectorAll("[data-layout-choice]").forEach((peer) => {
      const active = peer === button;
      peer.classList.toggle("is-active", active);
      peer.setAttribute("aria-pressed", String(active));
    });
    setText("viewport-note", layout === "auto" ? "Auto layout" : `${layout === "inner" ? "Unfolded" : "Cover"} preview forced`);
  });
});

document.getElementById("rotate-fixture").addEventListener("click", () => {
  fixtureIndex = (fixtureIndex + 1) % fixtures.length;
  updateFixture();
});

document.getElementById("service-search").addEventListener("input", renderServices);
document.getElementById("status-filter").addEventListener("change", renderServices);
document.getElementById("event-filter").addEventListener("change", (event) => renderEvents(event.target.value));

document.querySelectorAll("[data-job-state]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-job-state]").forEach((peer) => {
      const active = peer === button;
      peer.classList.toggle("is-active", active);
      peer.setAttribute("aria-selected", String(active));
    });
    renderJobs(button.dataset.jobState);
  });
});

document.getElementById("open-siren").addEventListener("click", () => {
  document.getElementById("app-shell").dataset.layout = "inner";
  document.querySelectorAll("[data-layout-choice]").forEach((peer) => {
    const active = peer.dataset.layoutChoice === "inner";
    peer.classList.toggle("is-active", active);
    peer.setAttribute("aria-pressed", String(active));
  });
  setText("viewport-note", "Unfolded preview forced");
  document.getElementById("siren-panel").scrollIntoView({ behavior: "auto", block: "center" });
  document.getElementById("siren-input").focus({ preventScroll: true });
});

document.getElementById("siren-send").addEventListener("click", () => simulateSiren(document.getElementById("siren-input").value));
document.getElementById("siren-input").addEventListener("keydown", (event) => {
  if (event.key === "Enter") simulateSiren(event.currentTarget.value);
});
document.querySelectorAll("[data-query]").forEach((button) => button.addEventListener("click", () => simulateSiren(button.dataset.query)));

renderServices();
renderJobs();
renderEvents();
renderVitals();
addMessage("Siren text simulator ready. Everything here is fictional and stays in this tab.", "assistant");
updateFixture();
