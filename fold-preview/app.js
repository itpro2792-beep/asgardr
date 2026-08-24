"use strict";

const baseServices = [
  { name: "demo-api-01", host: "demo-node-a", status: "online", cpu: 12, memory: 318, role: "Fixture API renderer" },
  { name: "demo-worker-01", host: "demo-node-a", status: "online", cpu: 27, memory: 522, role: "Synthetic queue worker" },
  { name: "demo-worker-03", host: "demo-node-b", status: "online", cpu: 24, memory: 484, role: "Compute comparison canary" },
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
    heading: "RF and compute fixtures are nominal",
    summary: "Balanced generated samples across both display-only domains.",
    health: 96,
    rf: { state: "nominal", label: "NOMINAL", copy: "Balanced sample path", rsrp: -78, sinr: 24, vswr: 1.18, optical: -6.4, downlink: 30.0, gain: 65, temperature: 39 },
    compute: { state: "nominal", label: "NOMINAL", copy: "Queue within demo baseline", cpu: 27, memory: 52, pending: 2, p95: 18, oldest: 6 },
    correlation: { label: "NONE", copy: "No shared synthetic fault" },
    queue: { running: 4, pending: 2, done: 128, failed: 1 },
    alert: ["No cross-domain anomaly in this fixture", "Illustrative values only · no action available"],
    serviceOverrides: {},
    path: [
      { id: "demo-donor-01", name: "Donor", status: "nominal", value: "−78 dBm", detail: "Generated over-the-air receive sample" },
      { id: "demo-headend-01", name: "Head-end", status: "nominal", value: "+65 dB", detail: "Fixed display-only gain sample" },
      { id: "demo-fiber-a", name: "Fiber A", status: "nominal", value: "−6.4 dBm", detail: "Generated optical receive sample" },
      { id: "demo-remote-a", name: "Remote A", status: "nominal", value: "+30.0 dBm", detail: "Demo composite downlink monitor point" },
      { id: "demo-zone-1", name: "Zone 1", status: "nominal", value: "24 dB", detail: "Generated signal-quality sample" }
    ],
    remotes: [
      { id: "DEMO-RU-A1", state: "nominal", optical: -6.4, temperature: 39, vswr: 1.18, band: "Demo low-band" },
      { id: "DEMO-RU-A2", state: "nominal", optical: -6.8, temperature: 40, vswr: 1.16, band: "Demo mid-band" },
      { id: "DEMO-RU-B1", state: "nominal", optical: -7.0, temperature: 41, vswr: 1.21, band: "Demo mixed-band" },
      { id: "DEMO-RU-B2", state: "nominal", optical: -6.6, temperature: 38, vswr: 1.19, band: "Demo mid-band" }
    ],
    findings: [
      { id: "DEMO-FIND-101", state: "info", title: "Baseline comparison ready", detail: "RF and compute samples remain intentionally independent." }
    ],
    trend: [-6.7, -6.5, -6.6, -6.4, -6.5, -6.4],
    isolation: "Both RF and compute values remain inside this scenario’s illustrative baseline. No relationship is inferred.",
    jobs: [
      { title: "Render synthetic RF digest", id: "DEMO-JOB-1042", state: "running", note: "42% · fixture artifact" },
      { title: "Index fictional event bundle", id: "DEMO-JOB-1043", state: "pending", note: "queued locally" },
      { title: "Validate sample identity tuples", id: "DEMO-JOB-1039", state: "succeeded", note: "completed fixture" },
      { title: "Generate visual latency study", id: "DEMO-JOB-1038", state: "failed", note: "intentional demo failure" }
    ],
    events: [
      { severity: "info", domain: "RF", type: "RF_FIXTURE_READY", source: "demo-headend-01", message: "Synthetic signal path loaded from browser memory." },
      { severity: "info", domain: "COMPUTE", type: "QUEUE_SAMPLE", source: "demo-node-c", message: "Pending fixture count is two." },
      { severity: "warning", domain: "DRILL", type: "DISPLAY_SAMPLE", source: "demo-node-d", message: "Warning color retained for interface evaluation only." }
    ]
  },
  {
    id: "B-02",
    label: "Optical-path fade",
    heading: "RF fixture is degraded; compute remains nominal",
    summary: "The generated RF path changes while cluster samples stay stable.",
    health: 73,
    rf: { state: "advisory", label: "ADVISORY", copy: "Optical-path fade sample", rsrp: -105, sinr: 3, vswr: 1.20, optical: -13.1, downlink: 21.0, gain: 65, temperature: 40 },
    compute: { state: "nominal", label: "NOMINAL", copy: "Compute remains isolated", cpu: 29, memory: 53, pending: 3, p95: 19, oldest: 7 },
    correlation: { label: "RF-LOCAL", copy: "Stable compute comparison" },
    queue: { running: 4, pending: 3, done: 131, failed: 1 },
    alert: ["Synthetic optical path is below fixture baseline", "demo-fiber-a · display-only RF advisory"],
    serviceOverrides: {},
    path: [
      { id: "demo-donor-01", name: "Donor", status: "advisory", value: "−105 dBm", detail: "Generated weak donor receive sample" },
      { id: "demo-headend-01", name: "Head-end", status: "nominal", value: "+65 dB", detail: "Gain sample remains unchanged" },
      { id: "demo-fiber-a", name: "Fiber A", status: "advisory", value: "−13.1 dBm", detail: "Generated optical fade sample" },
      { id: "demo-remote-a", name: "Remote A", status: "advisory", value: "+21.0 dBm", detail: "Lower demo composite downlink monitor point" },
      { id: "demo-zone-1", name: "Zone 1", status: "advisory", value: "3 dB", detail: "Generated signal-quality sample" }
    ],
    remotes: [
      { id: "DEMO-RU-A1", state: "advisory", optical: -13.1, temperature: 40, vswr: 1.20, band: "Demo low-band" },
      { id: "DEMO-RU-A2", state: "advisory", optical: -12.8, temperature: 41, vswr: 1.22, band: "Demo mid-band" },
      { id: "DEMO-RU-B1", state: "nominal", optical: -7.1, temperature: 41, vswr: 1.19, band: "Demo mixed-band" },
      { id: "DEMO-RU-B2", state: "nominal", optical: -6.9, temperature: 39, vswr: 1.17, band: "Demo mid-band" }
    ],
    findings: [
      { id: "DEMO-FIND-201", state: "warning", title: "Optical receive sample changed", detail: "Fiber A and its downstream remote share the generated fade." },
      { id: "DEMO-FIND-202", state: "info", title: "Antenna match stays stable", detail: "VSWR remains near baseline, arguing against a mismatch in this fiction." }
    ],
    trend: [-6.7, -7.8, -9.4, -11.2, -12.5, -13.1],
    isolation: "Lower optical receive, composite downlink, RSRP, and SINR appear together while VSWR, gain, temperature, and compute stay stable. This fictional pattern is RF-local, not proof of a real fault.",
    jobs: [
      { title: "Compare optical fixture samples", id: "DEMO-JOB-2048", state: "running", note: "76% · visual scenario" },
      { title: "Render RF isolation note", id: "DEMO-JOB-2049", state: "running", note: "31% · browser memory" },
      { title: "Stage synthetic path bundle", id: "DEMO-JOB-2050", state: "pending", note: "three items pending" },
      { title: "Retain intentional retry", id: "DEMO-JOB-2041", state: "failed", note: "controlled demo state" }
    ],
    events: [
      { severity: "info", domain: "RF", type: "SCENARIO_SELECTED", source: "demo-headend-01", message: "Optical-path fade fixture selected locally." },
      { severity: "warning", domain: "RF", type: "OPTICAL_SAMPLE", source: "demo-fiber-a", message: "Generated receive sample moved to −13.1 dBm." },
      { severity: "warning", domain: "RF", type: "SIGNAL_STUDY", source: "demo-zone-1", message: "Synthetic SINR sample moved to three dB." },
      { severity: "info", domain: "COMPUTE", type: "ISOLATION_SAMPLE", source: "demo-node-a", message: "Compute fixtures remain near baseline." }
    ]
  },
  {
    id: "C-03",
    label: "Compute queue pressure",
    heading: "Compute fixture is pressured; RF remains nominal",
    summary: "Queue depth and latency rise while RF/DAS samples stay stable.",
    health: 78,
    rf: { state: "nominal", label: "NOMINAL", copy: "RF path remains isolated", rsrp: -80, sinr: 22, vswr: 1.19, optical: -6.5, downlink: 29.8, gain: 65, temperature: 41 },
    compute: { state: "advisory", label: "ADVISORY", copy: "Generated queue pressure", cpu: 89, memory: 84, pending: 42, p95: 340, oldest: 156 },
    correlation: { label: "COMPUTE-LOCAL", copy: "Stable RF comparison" },
    queue: { running: 8, pending: 42, done: 142, failed: 2 },
    alert: ["Synthetic compute queue is above fixture baseline", "demo-worker-01 · display-only compute advisory"],
    serviceOverrides: {
      "demo-worker-01": { status: "warning", cpu: 89, memory: 842 },
      "demo-worker-03": { status: "warning", cpu: 87, memory: 806 },
      "demo-jobs-02": { status: "warning", cpu: 74, memory: 711 }
    },
    path: [
      { id: "demo-donor-01", name: "Donor", status: "nominal", value: "−80 dBm", detail: "Generated over-the-air receive sample" },
      { id: "demo-headend-01", name: "Head-end", status: "nominal", value: "+65 dB", detail: "Fixed display-only gain sample" },
      { id: "demo-fiber-a", name: "Fiber A", status: "nominal", value: "−6.5 dBm", detail: "Generated optical receive sample" },
      { id: "demo-remote-a", name: "Remote A", status: "nominal", value: "+29.8 dBm", detail: "Demo composite downlink monitor point" },
      { id: "demo-zone-1", name: "Zone 1", status: "nominal", value: "22 dB", detail: "Generated signal-quality sample" }
    ],
    remotes: [
      { id: "DEMO-RU-A1", state: "nominal", optical: -6.5, temperature: 41, vswr: 1.19, band: "Demo low-band" },
      { id: "DEMO-RU-A2", state: "nominal", optical: -6.9, temperature: 42, vswr: 1.18, band: "Demo mid-band" },
      { id: "DEMO-RU-B1", state: "nominal", optical: -7.0, temperature: 41, vswr: 1.20, band: "Demo mixed-band" },
      { id: "DEMO-RU-B2", state: "nominal", optical: -6.7, temperature: 40, vswr: 1.17, band: "Demo mid-band" }
    ],
    findings: [
      { id: "DEMO-FIND-301", state: "warning", title: "Compute queue pressure is isolated", detail: "RF samples remain near baseline while synthetic queue latency rises." },
      { id: "DEMO-FIND-302", state: "info", title: "RF path comparison is stable", detail: "No matching RF-side change is rendered in this scenario." }
    ],
    trend: [-6.7, -6.6, -6.8, -6.5, -6.6, -6.5],
    isolation: "CPU, memory, pending jobs, and queue latency rise together while the RF path remains steady. This fictional pattern is compute-local, not evidence about a real system.",
    jobs: [
      { title: "Reflow synthetic queue board", id: "DEMO-JOB-3048", state: "running", note: "86% · visual scenario" },
      { title: "Stage fictional event batch", id: "DEMO-JOB-3049", state: "running", note: "61% · browser memory" },
      { title: "Compare queue thresholds", id: "DEMO-JOB-3050", state: "pending", note: "42 sample items" },
      { title: "Render intentional retry", id: "DEMO-JOB-3041", state: "failed", note: "controlled demo state" }
    ],
    events: [
      { severity: "info", domain: "COMPUTE", type: "SCENARIO_SELECTED", source: "demo-node-a", message: "Compute-pressure fixture selected locally." },
      { severity: "warning", domain: "COMPUTE", type: "QUEUE_DEPTH", source: "demo-node-c", message: "Pending sample increased to forty-two." },
      { severity: "warning", domain: "COMPUTE", type: "LATENCY_SAMPLE", source: "demo-worker-01", message: "Generated queue p95 moved to 340 ms." },
      { severity: "info", domain: "RF", type: "ISOLATION_SAMPLE", source: "demo-headend-01", message: "RF fixtures remain near baseline." }
    ]
  }
];

const state = {
  fixtureIndex: 0,
  workspace: "rf",
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

function bounded(value, minimum, maximum) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return minimum;
  return Math.max(minimum, Math.min(maximum, numeric));
}

function recordActivity(title, detail) {
  state.activitySequence += 1;
  state.activity.unshift({ sequence: state.activitySequence, title, detail });
  state.activity = state.activity.slice(0, 5);
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
  const matches = currentServices().filter((service) => {
    const textMatch = service.name.includes(search) || service.host.includes(search) || service.role.toLowerCase().includes(search);
    return textMatch && (status === "all" || service.status === status);
  });
  grid.replaceChildren();
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
  const jobs = fixture.jobs.filter((job) => state.jobState === "all" || job.state === state.jobState);
  list.replaceChildren();
  jobs.forEach((job) => {
    const row = element("button", "job-row");
    row.type = "button";
    row.dataset.jobId = job.id;
    row.setAttribute("aria-label", `Inspect ${job.title}, ${job.state}`);
    const copy = element("span", "job-copy");
    copy.append(element("strong", "", job.title), element("span", "", `${job.id} · ${job.note}`));
    row.append(copy, element("span", `state-badge ${job.state}`, job.state));
    list.append(row);
  });
  if (!jobs.length) list.append(element("p", "empty-state", `No ${state.jobState} jobs in scenario ${fixture.id}.`));
}

function renderEvents() {
  const severity = document.getElementById("event-filter").value;
  const list = document.getElementById("event-list");
  const matches = currentFixture().events
    .map((event, index) => ({ ...event, fixtureTime: `T+00:${String(index * 7 + 3).padStart(2, "0")}` }))
    .filter((event) => severity === "all" || event.severity === severity);
  list.replaceChildren();
  matches.forEach((event) => {
    const row = element("article", "event-row");
    const copy = element("div");
    copy.append(element("strong", "", `${event.domain} · ${event.type}`), element("p", "", `${event.fixtureTime} · ${event.source} · ${event.message}`));
    row.append(element("span", `severity-badge ${event.severity}`, event.severity), copy);
    list.append(row);
  });
  if (!matches.length) list.append(element("p", "empty-state", `No ${severity} events in this scenario.`));
  setText("event-result-status", `${matches.length} synthetic event${matches.length === 1 ? "" : "s"} shown.`);
}

function renderVitals() {
  const fixture = currentFixture();
  const vitals = [
    ["CPU", fixture.compute.cpu, `${fixture.compute.cpu}%`],
    ["Memory", fixture.compute.memory, `${fixture.compute.memory}%`],
    ["Queue p95", bounded(fixture.compute.p95 / 4, 0, 100), `${fixture.compute.p95} ms`],
    ["Pending", bounded(fixture.compute.pending * 2, 0, 100), String(fixture.compute.pending)]
  ];
  const list = document.getElementById("vital-list");
  list.replaceChildren();
  vitals.forEach(([name, value, label]) => {
    const row = element("div", "vital-row");
    const gauge = element("div", "mini-meter");
    const fill = element("span");
    const normalized = bounded(value, 0, 100);
    fill.style.setProperty("--value", `${normalized}%`);
    gauge.setAttribute("role", "meter");
    gauge.setAttribute("aria-label", `Synthetic ${name.toLowerCase()}`);
    gauge.setAttribute("aria-valuemin", "0");
    gauge.setAttribute("aria-valuemax", "100");
    gauge.setAttribute("aria-valuenow", String(normalized));
    gauge.setAttribute("aria-valuetext", label);
    gauge.append(fill);
    row.append(element("span", "", name), gauge, element("strong", "", label));
    list.append(row);
  });
}

function kpiCard(key, label, value, status, note) {
  const card = element("button", "rf-kpi-card");
  card.type = "button";
  card.dataset.rfKpi = key;
  card.setAttribute("aria-label", `Inspect ${label}, ${value}, ${status}`);
  card.append(element("span", "kpi-label", label), element("strong", "kpi-value", value), element("span", `text-state ${status}`, status), element("small", "", note));
  return card;
}

function renderRfKpis() {
  const rf = currentFixture().rf;
  const status = rf.state;
  const cards = [
    ["rsrp", "Donor RSRP", `${rf.rsrp} dBm`, status, "generated receive sample"],
    ["sinr", "Signal quality", `${rf.sinr} dB`, status, "generated SINR sample"],
    ["vswr", "Worst VSWR", `${rf.vswr.toFixed(2)}:1`, rf.vswr < 1.3 ? "nominal" : "advisory", "fixture antenna match"],
    ["optical", "Optical Rx", `${rf.optical.toFixed(1)} dBm`, status, "generated fiber sample"],
    ["downlink", "Composite DL", `+${rf.downlink.toFixed(1)} dBm`, status, "demo monitor point"],
    ["temperature", "Remote temp", `${rf.temperature} °C`, "nominal", "generated equipment sample"]
  ];
  document.getElementById("rf-kpi-grid").replaceChildren(...cards.map((entry) => kpiCard(...entry)));
}

function renderSignalPath() {
  const path = document.getElementById("signal-path");
  path.replaceChildren();
  currentFixture().path.forEach((node, index) => {
    if (index) {
      const arrow = element("span", "path-arrow", "→");
      arrow.setAttribute("aria-hidden", "true");
      path.append(arrow);
    }
    const button = element("button", `path-node ${node.status}`);
    button.type = "button";
    button.dataset.pathId = node.id;
    button.setAttribute("aria-label", `Inspect ${node.name}, ${node.status}, ${node.value}`);
    button.append(element("span", "path-status", node.status), element("strong", "", node.name), element("small", "", node.value));
    path.append(button);
  });
  setText("path-summary", currentFixture().isolation);
}

function renderRemotes() {
  const selected = document.getElementById("remote-filter").value;
  const remotes = currentFixture().remotes.filter((remote) => selected === "all" || remote.state === selected);
  const grid = document.getElementById("remote-grid");
  grid.replaceChildren();
  remotes.forEach((remote) => {
    const button = element("button", "remote-card");
    button.type = "button";
    button.dataset.remoteId = remote.id;
    button.setAttribute("aria-label", `Inspect ${remote.id}, ${remote.state}`);
    const heading = element("span", "remote-heading");
    heading.append(element("strong", "", remote.id), element("span", `text-state ${remote.state}`, remote.state));
    const details = element("span", "remote-details");
    details.append(element("span", "", `Optical ${remote.optical.toFixed(1)} dBm`), element("span", "", `${remote.temperature} °C`), element("span", "", `VSWR ${remote.vswr.toFixed(2)}:1`), element("span", "", remote.band));
    button.append(heading, details, element("span", "inspect-cue", "Inspect"));
    grid.append(button);
  });
  setText("remote-result-status", `${remotes.length} synthetic remote${remotes.length === 1 ? "" : "s"} shown.`);
}

function renderFindings() {
  const list = document.getElementById("finding-list");
  list.replaceChildren();
  currentFixture().findings.forEach((finding) => {
    const button = element("button", "finding-card");
    button.type = "button";
    button.dataset.findingId = finding.id;
    button.setAttribute("aria-label", `Inspect ${finding.title}`);
    button.append(element("span", `severity-badge ${finding.state}`, finding.state), element("strong", "", finding.title), element("p", "", finding.detail), element("span", "inspect-cue", "Inspect"));
    list.append(button);
  });
}

function renderTrend() {
  const values = currentFixture().trend;
  const body = document.getElementById("trend-body");
  body.replaceChildren();
  values.forEach((value, index) => {
    const row = element("tr");
    const sample = element("th", "", `T${index + 1}`);
    sample.scope = "row";
    row.append(sample, element("td", "", `${value.toFixed(1)} dBm`));
    body.append(row);
  });
  const first = values[0];
  const last = values[values.length - 1];
  setText("trend-summary", `Fixed sequence: ${first.toFixed(1)} to ${last.toFixed(1)} dBm · ${currentFixture().rf.state} fixture.`);
}

function renderRfWorkspace() {
  const fixture = currentFixture();
  setText("rf-domain-state", fixture.rf.label);
  setText("rf-domain-copy", fixture.rf.copy);
  setText("compute-domain-state", fixture.compute.label);
  setText("compute-domain-copy", fixture.compute.copy);
  setText("correlation-state", fixture.correlation.label);
  setText("correlation-copy", fixture.correlation.copy);
  setText("advisory-count", fixture.findings.filter((finding) => finding.state === "warning").length);
  ["rf-domain-state", "compute-domain-state"].forEach((id) => {
    const node = document.getElementById(id);
    node.className = id === "rf-domain-state" ? fixture.rf.state : fixture.compute.state;
  });
  renderRfKpis();
  renderSignalPath();
  renderRemotes();
  renderFindings();
  renderTrend();
}

function updateFixture({ announce = false } = {}) {
  const fixture = currentFixture();
  document.getElementById("scenario-select").value = fixture.id;
  document.querySelectorAll(".scenario-stamp").forEach((node) => { node.textContent = `${fixture.id} · ${fixture.label}`; });
  setText("cover-heading", fixture.heading);
  setText("cover-summary", fixture.summary);
  setText("health-score", fixture.health);
  setText("cover-rf-state", fixture.rf.label);
  setText("cover-compute-state", fixture.compute.label);
  setText("cover-rsrp", `${fixture.rf.rsrp} dBm`);
  setText("cover-vswr", `${fixture.rf.vswr.toFixed(2)}:1`);
  setText("cover-cpu", `${fixture.compute.cpu}%`);
  setText("cover-p95", `${fixture.compute.p95} ms`);
  document.getElementById("cover-rf-state").className = `domain-state ${fixture.rf.state}`;
  document.getElementById("cover-compute-state").className = `domain-state ${fixture.compute.state}`;
  document.getElementById("health-ring").setAttribute("aria-label", `Demo health score ${fixture.health} percent`);
  setText("queue-running", fixture.queue.running);
  setText("queue-pending", fixture.queue.pending);
  setText("queue-done", fixture.queue.done);
  setText("queue-failed", fixture.queue.failed);
  setText("cover-alert-title", fixture.alert[0]);
  setText("cover-alert-copy", fixture.alert[1]);
  renderServices();
  renderJobs();
  renderEvents();
  renderVitals();
  renderRfWorkspace();
  if (announce) recordActivity("Scenario changed", `${fixture.id} · ${fixture.label}; RF and compute fixtures refreshed together.`);
  scheduleLayoutScan();
}

function addMessage(text, role) {
  const transcript = document.getElementById("transcript");
  transcript.append(element("div", `message ${role}`, text));
  while (transcript.childElementCount > 30) transcript.firstElementChild.remove();
  transcript.scrollTop = transcript.scrollHeight;
}

function simulateSiren(query) {
  const clean = query.trim();
  if (!clean) return;
  const fixture = currentFixture();
  addMessage(clean, "user");
  const normalized = clean.toLowerCase();
  let response = `Scenario ${fixture.id} is ${fixture.label.toLowerCase()}. RF is ${fixture.rf.label.toLowerCase()} and compute is ${fixture.compute.label.toLowerCase()}.`;
  if (normalized.includes("rf") || normalized.includes("isolation")) response = fixture.isolation;
  if (normalized.includes("warning")) response = `${fixture.alert[0]}. ${fixture.alert[1]}.`;
  if (normalized.includes("privacy")) response = "This preview contains no live identifiers, credentials, network or background connections, persistent storage, microphone access, permissions, or controller functions.";
  if (normalized.includes("layout")) response = "Device QA checks this visible workspace for overflow, clipped controls, small targets, scale, and sticky overlap. It stores and sends nothing.";
  addMessage(`SIMULATED RESPONSE — ${response}`, "assistant");
  document.getElementById("siren-input").value = "";
  recordActivity("Siren simulated", `Answered a local query against scenario ${fixture.id}.`);
}

function updateViewportNote() {
  const layout = document.getElementById("app-shell").dataset.layout;
  const view = layout === "auto" ? "Auto layout" : `${layout === "inner" ? "Unfolded" : "Cover"} forced`;
  const workspace = state.workspace === "rf" ? "RF / DAS" : "Operations";
  setText("viewport-note", `${view} · ${workspace}`);
}

function setLayout(layout, { announce = true } = {}) {
  document.getElementById("app-shell").dataset.layout = layout;
  document.querySelectorAll("[data-layout-choice]").forEach((peer) => {
    const active = peer.dataset.layoutChoice === layout;
    peer.classList.toggle("is-active", active);
    peer.setAttribute("aria-pressed", String(active));
  });
  updateViewportNote();
  if (announce) recordActivity("Layout changed", document.getElementById("viewport-note").textContent);
  scheduleLayoutScan();
}

function activateWorkspace(button, { focus = false, announce = true } = {}) {
  state.workspace = button.dataset.workspaceChoice;
  document.getElementById("app-shell").dataset.workspace = state.workspace;
  document.querySelectorAll("[data-workspace-choice]").forEach((peer) => {
    const active = peer === button;
    peer.classList.toggle("is-active", active);
    peer.setAttribute("aria-pressed", String(active));
    document.getElementById(peer.dataset.workspaceChoice === "rf" ? "rf-workspace" : "ops-workspace").hidden = !active;
  });
  updateViewportNote();
  if (focus) button.focus();
  if (announce) recordActivity("Workspace changed", `${button.textContent} workspace opened.`);
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
  wrapper.append(element("dt", "", term), element("dd", "", String(description)));
  return wrapper;
}

function showInspector({ kicker, title, summary, fields }, trigger) {
  const dialog = document.getElementById("inspector-dialog");
  setText("inspector-kicker", kicker);
  setText("inspector-title", title);
  setText("inspector-summary", summary);
  document.getElementById("inspector-grid").replaceChildren(...fields.map(([term, description]) => inspectorField(term, description)));
  state.lastInspectorTrigger = trigger;
  if (!dialog.open) {
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
  }
  document.getElementById("close-inspector").focus();
}

function inspectService(name, trigger) {
  const service = currentServices().find((item) => item.name === name);
  if (!service) return;
  showInspector({ kicker: "SERVICE FIXTURE", title: service.name, summary: service.role, fields: [["State", service.status], ["Fixture host", service.host], ["CPU sample", `${service.cpu}%`], ["Memory sample", `${service.memory} MB`], ["Scenario", currentFixture().label], ["Capability", "Display only"]] }, trigger);
  recordActivity("Service inspected", `${service.name} opened in the read-only inspector.`);
}

function inspectJob(id, trigger) {
  const job = currentFixture().jobs.find((item) => item.id === id);
  if (!job) return;
  showInspector({ kicker: "JOB FIXTURE", title: job.title, summary: "A fictional lifecycle artifact with no scheduler or execution path.", fields: [["Fixture ID", job.id], ["State", job.state], ["Detail", job.note], ["Scenario", currentFixture().label], ["Queue source", "Browser memory"], ["Capability", "Display only"]] }, trigger);
  recordActivity("Job inspected", `${job.id} opened in the read-only inspector.`);
}

function inspectRfKpi(key, trigger) {
  const rf = currentFixture().rf;
  const details = {
    rsrp: ["Donor RSRP", `${rf.rsrp} dBm`, "Generated receive sample; not a survey or acceptance value."],
    sinr: ["Signal quality", `${rf.sinr} dB`, "Generated SINR sample for visual comparison."],
    vswr: ["Worst VSWR", `${rf.vswr.toFixed(2)}:1`, "Fictional antenna-match sample; not an alarm limit."],
    optical: ["Optical Rx", `${rf.optical.toFixed(1)} dBm`, "Generated fiber-path receive sample."],
    downlink: ["Composite downlink", `+${rf.downlink.toFixed(1)} dBm`, "Demo monitor point; not test-equipment data."],
    temperature: ["Remote temperature", `${rf.temperature} °C`, "Generated equipment temperature sample."]
  };
  const detail = details[key];
  if (!detail) return;
  showInspector({ kicker: "RF MEASUREMENT FIXTURE", title: detail[0], summary: detail[2], fields: [["Display value", detail[1]], ["RF state", rf.label], ["Scenario", currentFixture().label], ["Provenance", "Browser-memory fixture"], ["Limits", "Illustrative only"], ["Capability", "Display only"]] }, trigger);
  recordActivity("RF sample inspected", `${detail[0]} opened in the read-only inspector.`);
}

function inspectPath(id, trigger) {
  const node = currentFixture().path.find((item) => item.id === id);
  if (!node) return;
  showInspector({ kicker: "SIGNAL-PATH FIXTURE", title: node.name, summary: node.detail, fields: [["Fixture ID", node.id], ["State", node.status], ["Display value", node.value], ["Scenario", currentFixture().label], ["Provenance", "Browser-memory fixture"], ["Capability", "Display only"]] }, trigger);
  recordActivity("Path node inspected", `${node.name} opened in the read-only inspector.`);
}

function inspectRemote(id, trigger) {
  const remote = currentFixture().remotes.find((item) => item.id === id);
  if (!remote) return;
  showInspector({ kicker: "REMOTE FIXTURE", title: remote.id, summary: "Fictional radio-unit sample with no hardware or network target.", fields: [["State", remote.state], ["Optical Rx", `${remote.optical.toFixed(1)} dBm`], ["Temperature", `${remote.temperature} °C`], ["VSWR", `${remote.vswr.toFixed(2)}:1`], ["Band label", remote.band], ["Capability", "Display only"]] }, trigger);
  recordActivity("Remote inspected", `${remote.id} opened in the read-only inspector.`);
}

function inspectFinding(id, trigger) {
  const finding = currentFixture().findings.find((item) => item.id === id);
  if (!finding) return;
  showInspector({ kicker: "SYNTHETIC FINDING", title: finding.title, summary: finding.detail, fields: [["Fixture ID", finding.id], ["State", finding.state], ["Scenario", currentFixture().label], ["Correlation", currentFixture().correlation.label], ["Disposition", "Explanation only"], ["Capability", "Display only"]] }, trigger);
  recordActivity("Finding inspected", `${finding.id} opened in the read-only inspector.`);
}

function effectiveView() {
  const shell = document.getElementById("app-shell");
  if (shell.dataset.layout === "cover") return "Cover (forced)";
  if (shell.dataset.layout === "inner") return `Unfolded · ${state.workspace}`;
  return shell.clientWidth >= 720 ? `Unfolded · ${state.workspace}` : "Cover (auto)";
}

function visible(node) {
  return Boolean(node && node.getClientRects().length);
}

function runLayoutScan({ announce = true } = {}) {
  const root = document.documentElement;
  const visual = window.visualViewport;
  const checks = [
    ["Truth banner", ".safety-banner"], ["Preview toolbar", ".preview-toolbar"], ["Cover canvas", ".cover-view"],
    ["Workspace controls", ".workspace-control"], ["Situation strip", ".situation-strip"], ["RF scorecard", ".rf-kpi-grid"],
    ["Signal path", ".signal-path"], ["Remote matrix", ".remote-grid"], ["Finding list", ".finding-list"],
    ["Service matrix", ".service-grid"], ["Job tabs", ".tab-list"], ["Siren query", ".query-row"], ["Device stats", ".device-stats"]
  ];
  const issues = [];
  let checked = 1;
  if (root.scrollWidth > root.clientWidth + 1) issues.push("Page root overflow");
  checks.forEach(([label, selector]) => {
    const node = document.querySelector(selector);
    if (!visible(node)) return;
    checked += 1;
    if (node.scrollWidth > node.clientWidth + 1) issues.push(`${label} overflow`);
  });
  const viewportWidth = visual ? visual.width : root.clientWidth;
  const viewportHeight = visual ? visual.height : root.clientHeight;
  const controls = [...document.querySelectorAll("button, input, select, a")].filter(visible);
  let smallTargets = 0;
  let clippedControls = 0;
  controls.forEach((control) => {
    const rect = control.getBoundingClientRect();
    const onScreen = rect.bottom > 0 && rect.top < viewportHeight && rect.right > 0 && rect.left < viewportWidth;
    if (rect.width < 44 || rect.height < 44) smallTargets += 1;
    if (onScreen && (rect.left < -1 || rect.right > viewportWidth + 1)) clippedControls += 1;
  });
  if (smallTargets) issues.push(`${smallTargets} visible target${smallTargets === 1 ? "" : "s"} below 44 px`);
  if (clippedControls) issues.push(`${clippedControls} clipped control${clippedControls === 1 ? "" : "s"}`);
  const banner = document.querySelector(".safety-banner").getBoundingClientRect();
  const topbar = document.querySelector(".topbar").getBoundingClientRect();
  if (topbar.bottom > 0 && topbar.top < banner.bottom - 1) issues.push("Sticky banner overlap");
  const passed = issues.length === 0;
  setText("layout-viewport", `${root.clientWidth} × ${root.clientHeight} CSS px`);
  setText("visual-viewport", visual ? `${Math.round(visual.width)} × ${Math.round(visual.height)} CSS px` : "Not exposed");
  setText("scale-dpr", `${visual ? visual.scale.toFixed(2) : "1.00"}× / ${window.devicePixelRatio.toFixed(2)}`);
  setText("effective-view", effectiveView());
  setText("page-fit", passed ? `PASS · ${checked} rails` : `REVIEW · ${issues.length} issue${issues.length === 1 ? "" : "s"}`);
  const badge = document.getElementById("fit-badge");
  badge.className = `fit-badge ${passed ? "pass" : "review"}`;
  badge.textContent = passed ? "FIT PASS" : "REVIEW";
  const results = document.getElementById("scan-results");
  results.replaceChildren();
  if (passed) results.append(element("p", "scan-pass", `PASS — ${checked} visible rails fit; visible controls meet the 44 px target check.`));
  else {
    results.append(element("p", "scan-review", "Review this viewport:"));
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

function wireAutomaticTabs(selector, activate) {
  document.querySelectorAll(selector).forEach((button) => {
    button.addEventListener("click", () => activate(button));
    button.addEventListener("keydown", (event) => {
      const tabs = [...document.querySelectorAll(selector)];
      const current = tabs.indexOf(event.currentTarget);
      let next = null;
      if (event.key === "ArrowRight") next = (current + 1) % tabs.length;
      if (event.key === "ArrowLeft") next = (current - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next !== null) {
        event.preventDefault();
        activate(tabs[next], { focus: true });
      }
    });
  });
}

document.querySelectorAll("[data-layout-choice]").forEach((button) => button.addEventListener("click", () => setLayout(button.dataset.layoutChoice)));
wireAutomaticTabs("[data-workspace-choice]", activateWorkspace);
wireAutomaticTabs("[data-job-state]", activateJobTab);

document.getElementById("scenario-select").addEventListener("change", (event) => {
  const nextIndex = fixtures.findIndex((fixture) => fixture.id === event.target.value);
  if (nextIndex >= 0) {
    state.fixtureIndex = nextIndex;
    updateFixture({ announce: true });
  }
});
document.getElementById("rotate-fixture").addEventListener("click", () => {
  state.fixtureIndex = (state.fixtureIndex + 1) % fixtures.length;
  updateFixture({ announce: true });
});

document.getElementById("open-workspace").addEventListener("click", () => {
  setLayout("inner");
  activateWorkspace(document.getElementById(state.workspace === "rf" ? "workspace-tab-rf" : "workspace-tab-ops"));
  document.getElementById(state.workspace === "rf" ? "rf-scorecard" : "services-panel").scrollIntoView({ behavior: "auto", block: "start" });
});

document.getElementById("service-search").addEventListener("input", renderServices);
document.getElementById("status-filter").addEventListener("change", (event) => { renderServices(); recordActivity("Service status filtered", `${event.target.options[event.target.selectedIndex].text} selected.`); });
document.getElementById("event-filter").addEventListener("change", (event) => { renderEvents(); recordActivity("Event severity filtered", `${event.target.options[event.target.selectedIndex].text} selected.`); });
document.getElementById("remote-filter").addEventListener("change", (event) => { renderRemotes(); recordActivity("Remote state filtered", `${event.target.options[event.target.selectedIndex].text} selected.`); });

document.getElementById("service-grid").addEventListener("click", (event) => { const card = event.target.closest("[data-service-name]"); if (card) inspectService(card.dataset.serviceName, card); });
document.getElementById("job-list").addEventListener("click", (event) => { const row = event.target.closest("[data-job-id]"); if (row) inspectJob(row.dataset.jobId, row); });
document.getElementById("rf-kpi-grid").addEventListener("click", (event) => { const card = event.target.closest("[data-rf-kpi]"); if (card) inspectRfKpi(card.dataset.rfKpi, card); });
document.getElementById("signal-path").addEventListener("click", (event) => { const card = event.target.closest("[data-path-id]"); if (card) inspectPath(card.dataset.pathId, card); });
document.getElementById("remote-grid").addEventListener("click", (event) => { const card = event.target.closest("[data-remote-id]"); if (card) inspectRemote(card.dataset.remoteId, card); });
document.getElementById("finding-list").addEventListener("click", (event) => { const card = event.target.closest("[data-finding-id]"); if (card) inspectFinding(card.dataset.findingId, card); });

document.getElementById("siren-send").addEventListener("click", () => simulateSiren(document.getElementById("siren-input").value));
document.getElementById("siren-input").addEventListener("keydown", (event) => { if (event.key === "Enter") simulateSiren(event.currentTarget.value); });
document.querySelectorAll("[data-query]").forEach((button) => button.addEventListener("click", () => simulateSiren(button.dataset.query)));

const dialog = document.getElementById("inspector-dialog");
document.getElementById("close-inspector").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
dialog.addEventListener("close", () => {
  if (state.lastInspectorTrigger && document.contains(state.lastInspectorTrigger)) state.lastInspectorTrigger.focus();
  else document.getElementById(state.workspace === "rf" ? "workspace-tab-rf" : "workspace-tab-ops").focus();
});

document.getElementById("run-scan").addEventListener("click", () => runLayoutScan());
document.getElementById("cover-scan").addEventListener("click", () => runLayoutScan());
window.addEventListener("resize", scheduleLayoutScan, { passive: true });
if (window.visualViewport) window.visualViewport.addEventListener("resize", scheduleLayoutScan, { passive: true });

recordActivity("Preview ready", "Synthetic canary V3 loaded; all state is browser-memory only.");
addMessage("Siren text simulator ready. RF and compute values are fictional and remain in this tab.", "assistant");
activateJobTab(document.getElementById("job-tab-all"), { announce: false });
activateWorkspace(document.getElementById("workspace-tab-rf"), { announce: false });
updateFixture();
scheduleLayoutScan();
