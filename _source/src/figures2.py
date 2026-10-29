"""Figures for documents 04-08."""
from svg import Diagram, CRIMSON, GRAY, MUTED, LINE, SOFT, PANEL, WHITE, MIDNIGHT, SKY, AUTUMN, VINE, text_width
from figures import fig


# =====================================================================  04 ARCHITECTURE
@fig("arch-layers", "<b>RADAR's five layers on top of existing systems.</b> Data moves up the stack; decisions, overrides and outcomes flow back down as feedback. Identity, audit and observability cut across every layer rather than being bolted onto one of them.", wide=True)
def arch_layers():
    d = Diagram(760, 486, "Layered stack: source systems, integration layer, bridge layer (MER), intelligence layer, decision-support layer and users and channels, with cross-cutting identity and access, audit and governance, and observability columns.")
    layers = [
        ("Users & channels", "dark", ["EOC dashboard", "DMT-PHE workspace", "SMS / email alerts", "Partner APIs"]),
        ("Decision support", "solid", ["Rules engine (trigger cards)", "AI agent (RAG + LLM)", "Human review", "Audit log"]),
        ("Intelligence", "accent", ["Record linkage", "Anomaly detection", "Fusion", "Forecasts", "Risk score"]),
        ("Bridge · MER", "accent", ["MER service", "FHIR R4 server", "Event bus"]),
        ("Integration", "plain", ["Connectors", "OpenHIM / LATTICE", "Terminology", "Quality checks"]),
        ("Source systems", "ghost", ["KHIS2", "m-Dharura", "KABS", "LIMS", "KMD · NDMA", "EIOS"]),
    ]
    flows = ["recommendations", "risk signals", "linked events", "standard fields", "pull / push"]
    lh, gap, y0 = 52, 26, 8
    for i, (name, st, items) in enumerate(layers):
        y = y0 + i * (lh + gap)
        lab = d.box(0, y, 130, lh, name, style=st if st != "ghost" else "dashed", ts=12)
        x = 142
        avail = 600 - x
        w = (avail - (len(items) - 1) * 8) / len(items)
        for it in items:
            d.box(x, y + 6, w, lh - 12, it, style="dashed" if st == "ghost" else "line", ts=10.5, tw=600, pad=6)
            x += w + 8
        if i < len(layers) - 1:
            yy = y + lh
            d.arrow([(40, yy + gap - 1), (40, yy + 1)], style="accent")
            d.text(52, yy + gap / 2, flows[i], 10, 600, "start", CRIMSON, halo=True)
            d.arrow([(92, yy + 1), (92, yy + gap - 1)], style="muted", sw=1.1)
    d.text(104, y0 + 6 * (lh + gap) - 12, "", 10)
    # cross-cutting
    ccs = ["Identity & access", "Audit & governance", "Observability"]
    for j, c in enumerate(ccs):
        x = 616 + j * 49
        d.rect(x, y0, 41, 5 * (lh + gap) + lh - 0, PANEL, PANEL, 1, 6)
        d.vtext(x + 20.5, y0 + (5 * (lh + gap) + lh) / 2, c.upper(), 10.5, 700, GRAY, ls="0.08em")
    d.line(0, 476, 30, 476, CRIMSON, 2, layer="front")
    d.text(36, 476, "data up", 10, 600, "start", MUTED)
    d.line(110, 476, 140, 476, LINE, 1.4, layer="front")
    d.text(146, 476, "feedback down", 10, 600, "start", MUTED)
    return d


@fig("arch-containers", "<b>Runtime components and the path one record takes.</b> A record enters through the gateway, is landed unchanged, validated, mapped and coded, linked to an event, and published. Analytics consume events from the bus; the decision service combines deterministic rules with the AI agent, and every human decision lands in the append-only audit log.", wide=True)
def arch_containers():
    d = Diagram(760, 440, "Component diagram in four rows: ingestion (gateway, connector workers, raw landing, validate and map), core (linker, MER service with FHIR, event bus, analytics, signal store), decision (rules engine, agent service, web app, audit log, outbound gateway) and AI support (knowledge base, LLM server, identity provider).")
    cw, gx = 136, 20
    X = [i * (cw + gx) for i in range(5)]
    R = [24, 136, 248, 360]
    h = 58
    zl = [(0, "Ingest"), (1, "Core"), (2, "Decide"), (3, "Support")]
    for r, lab in zl:
        d.text(0, R[r] - 12, lab.upper(), 10, 700, "start", MUTED, ls="0.08em")
    b = {}
    b["src"] = d.box(X[0], R[0], cw, h, "Source systems", "KHIS2 · KABS · m-Dharura …", style="dashed", ts=11.5, ss=10)
    b["gw"] = d.box(X[1], R[0], cw, h, "Gateway", "OpenHIM / LATTICE", ts=11.5, ss=10)
    b["wk"] = d.box(X[2], R[0], cw, h, "Connectors", "scheduled jobs · Dagster", ts=11.5, ss=10)
    b["raw"] = d.box(X[3], R[0], cw, h, "Raw landing", "immutable object store", ts=11.5, ss=10)
    b["val"] = d.box(X[4], R[0], cw, h, "Validate · map", "schema · FHIR · codes", ts=11.5, ss=10)
    b["lnk"] = d.box(X[4], R[1], cw, h, "Linker", "match to events (Splink)", ts=11.5, ss=10)
    b["mer"] = d.box(X[3], R[1], cw, h, "MER service", "HAPI FHIR R4 · PostgreSQL", style="accent", ts=11.5, ss=10)
    b["bus"] = d.box(X[2], R[1], cw, h, "Event bus", "NATS JetStream", ts=11.5, ss=10)
    b["ana"] = d.box(X[1], R[1], cw, h, "Analytics", "detection · fusion · forecasts", ts=11.5, ss=10)
    b["sig"] = d.box(X[0], R[1], cw, h, "Signal store", "risk scores + evidence", ts=11.5, ss=10)
    b["rul"] = d.box(X[0], R[2], cw, h, "Rules engine", "trigger-card thresholds", style="solid", ts=11.5, ss=10)
    b["agt"] = d.box(X[1], R[2], cw, h, "Agent service", "RAG · tools via MCP", style="solid", ts=11.5, ss=10)
    b["app"] = d.box(X[2], R[2], cw, h, "RADAR web app", "dashboard · DMT-PHE", style="dark", ts=11.5, ss=10)
    b["aud"] = d.box(X[3], R[2], cw, h, "Audit log", "append-only, signed", ts=11.5, ss=10)
    b["out"] = d.box(X[4], R[2], cw, h, "Outbound", "GHEC-AI · SMS · email", ts=11.5, ss=10)
    b["kb"] = d.box(X[0], R[3], cw, h, "Knowledge base", "guidelines · pgvector", ts=11.5, ss=10)
    b["llm"] = d.box(X[1], R[3], cw, h, "LLM server", "vLLM · on-prem GPU", ts=11.5, ss=10)
    b["idp"] = d.box(X[2], R[3], cw * 3 + gx * 2, h, "Identity provider (Keycloak)", "SSO · MFA · role-based access for every component above", style="soft", ts=11.5, ss=10)
    A = d.arrow
    A([b["src"].r(), b["gw"].l()])
    A([b["gw"].r(), b["wk"].l()])
    A([b["wk"].r(), b["raw"].l()])
    A([b["raw"].r(), b["val"].l()])
    A([b["val"].b(), b["lnk"].t()])
    A([b["lnk"].l(), b["mer"].r()])
    A([b["mer"].l(), b["bus"].r()], style="accent")
    A([b["bus"].l(), b["ana"].r()])
    A([b["ana"].l(), b["sig"].r()])
    A([b["sig"].b(), b["rul"].t()], "signal card", lpos=(X[0] + cw / 2, R[1] + h + 26))
    A([b["rul"].r(), b["agt"].l()])
    A([b["agt"].r(), b["app"].l()])
    A([b["app"].r(), b["aud"].l()], style="accent")
    A([b["aud"].r(), b["out"].l()])
    A([b["agt"].b(-20), (b["agt"].cx - 20, R[3])], None, head="end")
    A([(b["agt"].cx + 20, R[3]), b["agt"].b(20)], None, head="end", style="muted")
    A([(b["agt"].x + 14, R[2] + h), (b["agt"].x + 14, R[3] - 22), (b["kb"].cx, R[3] - 22), b["kb"].t()], "retrieve", lpos=(b["kb"].cx + 34, R[3] - 22))
    A([b["app"].t(), (b["app"].cx, R[1] + h + 22), (b["mer"].cx, R[1] + h + 22), b["mer"].b()], "status updates", style="muted", lpos=(X[3] - 10, R[1] + h + 22))
    return d


@fig("arch-envs", "<b>Three environments, one rule.</b> Code and models are promoted left to right through signed CI/CD builds; identifiable data never moves left. Development can use cloud hosting because it only ever sees synthetic or approved non-identifiable data.")
def arch_envs():
    d = Diagram(760, 236, "Development, staging and production environments with promotion arrows; production backs up to a recovery site; identifiable data stays in production.")
    e1 = d.box(0, 20, 210, 120, "Development", "approved cloud or WSU-hosted · synthetic & de-identified data · open to all developers", ts=13, ss=10.5)
    e2 = d.box(275, 20, 210, 120, "Staging / UAT", "KNPHI/DHA-approved infra · de-identified replay of real feeds · load & security tests", ts=13, ss=10.5)
    e3 = d.box(550, 20, 210, 120, "Production", "KNPHI/DHA infra · live identifiable data · least-privilege admin access", style="accent", ts=13, ss=10.5)
    d.arrow([e1.r(), e2.l()], "promote\nsigned build", lpos=(242, 60))
    d.arrow([e2.r(), e3.l()], "after\ngo/no-go", lpos=(517, 60))
    dr = d.box(550, 176, 210, 50, "Recovery site", "encrypted backups · Government-authorised", style="dashed", ts=12, ss=10)
    d.arrow([e3.b(), dr.t()], "encrypted backup", lpos=(655, 158))
    d.line(0, 186, 490, 186, CRIMSON, 2, dash="6 4", layer="front")
    d.poly([(0, 186), (10, 181), (10, 191)], CRIMSON, CRIMSON)
    d.text(245, 204, "Identifiable data never flows left of production", 11, 700, "middle", CRIMSON)
    return d


# =====================================================================  05 INTEROPERABILITY
@fig("interop-pipeline", "<b>One connector pipeline for every source.</b> Each step is small and testable. Raw data is always kept unchanged so any record can be re-processed when a mapping improves; records that fail validation are quarantined and the data steward is alerted — they are never silently dropped.")
def interop_pipeline():
    d = Diagram(760, 236, "Seven-step pipeline: extract, land raw, validate, map to MER and FHIR, code with terminology, link to event, publish; failed validation goes to quarantine with an alert and is replayed after a fix.")
    steps = [("Extract", "API · file · FHIR"), ("Land", "raw, unchanged"), ("Validate", "schema · ranges"), ("Map", "to MER / FHIR"),
             ("Code", "ICD-11 · KMHFL · admin units"), ("Link", "to an event"), ("Publish", "event bus")]
    w, g = 96, 14
    bs = []
    for i, (t, s) in enumerate(steps):
        bs.append(d.box(i * (w + g), 30, w, 66, t, s, style="accent" if t in ("Link", "Publish") else "plain", ts=12.5, ss=10))
    for a, b in zip(bs, bs[1:]):
        d.arrow([a.r(), b.l()])
    q = d.box(bs[2].x - 30, 160, w + 60, 56, "Quarantine", "alert data steward", style="dashed", ts=12, ss=10)
    d.arrow([bs[2].b(), (bs[2].cx, 160)], "fails", lpos=(bs[2].cx, 128))
    d.arrow([q.l(), (bs[1].cx, q.cy), bs[1].b()], "fix & replay", style="dashed", lpos=(bs[1].cx - 6, 190), lanchor="end")
    d.text(560, 188, "Every step logs counts in / out → data-quality dashboard", 10.5, 600, "middle", MUTED)
    d.text(0, 12, "SAME PATTERN FOR EVERY SOURCE", 10, 700, "start", MUTED, ls="0.08em")
    return d


@fig("interop-ladder", "<b>Integration maturity ladder.</b> Start each source at the lowest level that delivers value and climb when the partner is ready. The MVP only needs Level 1–2 for its priority sources; Level 4 (publish/subscribe of MER events) is the end state the MER standard enables.")
def interop_ladder():
    d = Diagram(760, 280, "Five ascending steps: level 0 manual upload, level 1 scheduled file, level 2 API pull, level 3 standards-based FHIR exchange, level 4 publish and subscribe of MER events, with MVP target bracket over levels 1 and 2.")
    lv = [("L0 · Manual", "EOC uploads a sheet", "e.g. historic line lists"), ("L1 · Scheduled file", "CSV / Excel via SFTP", "e.g. NDMA bulletins"),
          ("L2 · API pull", "source REST API", "e.g. KHIS2, KABS"), ("L3 · FHIR exchange", "Kenya Core profiles", "e.g. LIMS (Diagnostics IG)"),
          ("L4 · Pub / sub", "MER events both ways", "end state")]
    w, g = 140, 15
    for i, (t, s, e) in enumerate(lv):
        x = i * (w + g)
        top = 190 - i * 36
        st = "accent" if i in (1, 2) else ("solid" if i == 4 else "plain")
        d.box(x, top, w, 56, t, s, style=st, ts=12, ss=10)
        d.rect(x, top + 60, w, 276 - top - 60, PANEL, PANEL, 1, 4, layer="back")
        d.text(x + w / 2, top + 74, e, 10, 500, "middle", MUTED)
    d.line(155, 100, 435, 100, CRIMSON, 2, layer="front")
    d.line(155, 94, 155, 106, CRIMSON, 2, layer="front")
    d.line(435, 94, 435, 106, CRIMSON, 2, layer="front")
    d.text(295, 86, "MVP target for priority sources", 11, 700, "middle", CRIMSON)
    d.arrow([(10, 18), (750, 18)], "more automated · more standardised · less manual EOC effort", style="muted", lpos=(330, 18))
    return d


@fig("interop-fhir-mcp", "<b>FHIR and MCP do different jobs.</b> FHIR R4 (through the OpenHIM/LATTICE gateway) moves records between systems. MCP connects the AI agent to a small set of tools; read tools are open to the agent, while any tool that writes or sends something outside RADAR requires an explicit human approval first.", wide=True)
def interop_fhir_mcp():
    d = Diagram(760, 330, "Top lane: source systems exchange FHIR R4 resources through the gateway with the MER FHIR server and GHEC-AI. Bottom lane: the AI agent, as MCP client, calls four MCP tool servers: MER query, trigger-card lookup, guideline search and GHEC-AI hand-off which requires human approval.")
    d.zone(0, 0, 760, 120, "System ↔ system · FHIR R4", fill="#F8F8F8")
    d.zone(0, 140, 760, 190, "AI agent ↔ tools · MCP", fill="#F8F8F8", lcolor=CRIMSON)
    s = d.box(14, 34, 150, 66, "Source systems", "KHIS2 · LIMS · KABS", ts=12, ss=10)
    g = d.box(214, 34, 150, 66, "Gateway", "OpenHIM / LATTICE · auth · logs", ts=12, ss=10)
    f = d.box(414, 34, 150, 66, "MER FHIR server", "HAPI FHIR R4", style="accent", ts=12, ss=10)
    gh = d.box(614, 34, 132, 66, "GHEC-AI API", "partner system", ts=12, ss=10)
    d.arrow([s.r(), g.l()], "Bundle", head="both")
    d.arrow([g.r(), f.l()], "REST", head="both")
    d.arrow([f.r(), gh.l()], "hand-off", head="end")
    ag = d.box(14, 200, 150, 90, "AI agent", "MCP client · LLM on-prem", style="solid", ts=12.5, ss=10)
    tools = [("MER query", "read-only", "plain"), ("Trigger-card lookup", "read-only", "plain"), ("Guideline search", "read-only · cited", "plain"),
             ("GHEC-AI hand-off", "needs approval", "accent")]
    for i, (t, sub, st) in enumerate(tools):
        x = 236 + i * 130
        tb = d.box(x, 210, 124, 66, t, sub, style=st, ts=11.5, ss=10)
        if i == 0:
            d.arrow([(tb.cx, 214), (tb.cx, f.y + f.h + 30), (f.cx, f.y + f.h + 30), f.b()], "reads", style="muted", lpos=(400, f.y + f.h + 30))
    d.line(164, 245, 226, 245, GRAY, 1.4)
    d.line(226, 196, 226, 290, GRAY, 1.4)
    d.text(195, 234, "MCP", 10, 700, "middle", MUTED, halo=True)
    d.text(236, 304, "Write tools run only after a named officer approves the action.", 10.5, 600, "start", CRIMSON)
    return d


# =====================================================================  06 INTELLIGENCE
@fig("intel-pipeline", "<b>From harmonised feeds to a signal card.</b> Single-stream detectors find unusual counts; clustering finds unusual places; fusion asks whether several independent streams point at the same place and syndrome at the same time. Confirmed and discarded outcomes flow back to recalibrate thresholds and weights.", wide=True)
def intel_pipeline():
    d = Diagram(760, 300, "Six stages: harmonised streams, baselines, aberration detection, space-time clustering, cross-stream fusion with forecasts as an extra input, risk score and signal card to DMT-PHE; outcome labels feed back to baselines and fusion.")
    st = [("Harmonised streams", "per place · syndrome · day/week"), ("Baselines", "seasonal, trend-adjusted"), ("Aberration detection", "Farrington · EARS · CUSUM"),
          ("Space-time clusters", "scan statistics"), ("Fusion", "rules + graph across streams"), ("Signal card", "risk score + evidence → DMT-PHE")]
    w, g = 112, 17
    bs = []
    for i, (t, s) in enumerate(st):
        style = "accent" if t == "Fusion" else ("solid" if t == "Signal card" else "plain")
        bs.append(d.box(i * (w + g), 40, w, 84, t, s, style=style, ts=12, ss=10))
    for a, b in zip(bs, bs[1:]):
        d.arrow([a.r(), b.l()])
    fc = d.box(bs[4].x - 20, 170, w + 40, 56, "Forecasts", "climate-driven risk (e.g. RVF, cholera)", style="dashed", ts=11.5, ss=10)
    d.arrow([fc.t(), bs[4].b()], "prior risk", lpos=(bs[4].cx + 30, 148), lanchor="start")
    d.arrow([bs[5].b(), (bs[5].cx, 262), (bs[1].cx, 262), bs[1].b()], "confirmed / discarded labels recalibrate thresholds and weights", style="dashed", lpos=(300, 262))
    d.text(0, 18, "RUNS ON EVERY NEW BATCH · RESULTS STORED WITH THEIR EVIDENCE", 10, 700, "start", MUTED, ls="0.06em")
    return d


@fig("intel-rvf", "<b>Why fusion buys time: the Rift Valley fever chain (illustrative).</b> Climate and animal signals usually appear weeks before human cases. A single-stream human detector fires late; a fused score rises as each independent stream adds evidence. Actual lags must be estimated from Kenyan data (e.g., the 2006–07 and 2018 outbreaks) before thresholds are set.", wide=True)
def intel_rvf():
    d = Diagram(760, 318, "Timeline over twelve weeks with bars for rainfall anomaly, vegetation and vector conditions, livestock abortions, human febrile cases and lab confirmation; a stepped fused risk line rises from low to high as each stream appears, well before the human-only detector would alert.")
    x0, x1 = 170, 738
    wk = lambda w: x0 + (x1 - x0) * w / 12
    rows = [("Rainfall anomaly", "KMD", 0, 2.5, GRAY), ("Vegetation / vectors", "NDMA · entomology", 1.5, 6, VINE),
            ("Livestock abortions", "KABS", 4, 8.5, AUTUMN), ("Human febrile cases", "m-Dharura · KHIS2", 6.5, 10.5, MIDNIGHT),
            ("Lab confirmation", "LIMS", 8.5, 11, CRIMSON)]
    ytop = 146
    for i, (t, s, a, b, c) in enumerate(rows):
        y = ytop + i * 32
        d.text(0, y + 1, t, 11, 700, "start")
        d.text(0, y + 15, s, 9.5, 500, "start", MUTED)
        d.rect(wk(a), y + 1, wk(b) - wk(a), 13, c, c, 1, 4)
    for w in range(0, 13, 2):
        x = wk(w)
        d.line(x, 136, x, ytop + 5 * 32 - 6, SOFT, 1, layer="back")
        d.text(x, ytop + 5 * 32 + 4, f"wk {w}", 9.5, 500, "middle", MUTED)
    # fused score
    pts = [(wk(0), 110), (wk(1), 110), (wk(1), 92), (wk(3), 92), (wk(3), 72), (wk(5), 72), (wk(5), 48), (wk(12), 48)]
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d.raw(f'<polyline points="{p}" fill="none" stroke="{CRIMSON}" stroke-width="2.5" stroke-linejoin="round"/>')
    d.text(0, 48, "Fused risk", 11, 700, "start", CRIMSON)
    d.text(0, 64, "(RADAR)", 9.5, 500, "start", MUTED)
    for y, lab in [(110, "low"), (92, "watch"), (72, "alert"), (48, "high")]:
        d.text(x0 - 10, y, lab, 9.5, 600, "end", MUTED)
    d.line(wk(8), 30, wk(8), 120, GRAY, 1.4, dash="4 3", layer="front")
    d.text(wk(8) + 6, 28, "human-only alert", 10, 600, "start", GRAY)
    d.line(wk(5), 30, wk(5), 120, CRIMSON, 1.4, dash="4 3", layer="front")
    d.text(wk(5) - 6, 28, "fused alert", 10, 700, "end", CRIMSON)
    return d


# =====================================================================  07 DMT-PHE & AGENT
@fig("dmt-agent", "<b>LLM proposes, rules verify, a human decides.</b> The escalation level always comes from the deterministic trigger-card rules; the language model explains, gathers context and drafts actions with page-level citations. A validator blocks drafts that disagree with the rules or cite nothing, and no recommendation takes effect until a named officer confirms, modifies or overrides it.", wide=True)
def dmt_agent():
    d = Diagram(760, 346, "Flow: signal card into rules engine, retrieval of guidelines, LLM draft, validator; if checks pass the EOC officer confirms, modifies or overrides with a reason; the decision goes to the audit log and then to escalation or GHEC-AI hand-off; failed checks route to senior review.")
    w, g = 168, 29
    r1 = [("Signal card", "from RADAR: event, evidence, risk", "plain"), ("1 · Rules engine", "trigger-card thresholds → level", "solid"),
          ("2 · Retrieve", "guidelines KB · cited pages", "plain"), ("3 · LLM draft", "classification, actions, reasoning trace", "plain")]
    b1 = [d.box(i * (w + g), 30, w, 72, t, s, style=st, ts=12.5, ss=10.5) for i, (t, s, st) in enumerate(r1)]
    for a, b in zip(b1, b1[1:]):
        d.arrow([a.r(), b.l()])
    val = d.box(b1[3].x, 160, w, 72, "4 · Validator", "schema · citations exist · agrees with rules?", style="accent", ts=12.5, ss=10.5)
    d.arrow([b1[3].b(), val.t()])
    hum = d.box(b1[2].x, 160, w, 72, "5 · EOC officer", "confirm · modify · override (+ reason)", style="dark", ts=12.5, ss=10.5)
    d.arrow([val.l(), hum.r()], "pass", style="accent", lpos=(val.x - 14, val.y - 10))
    aud = d.box(b1[1].x, 160, w, 72, "6 · Audit log", "inputs, draft, decision, who, when", ts=12.5, ss=10.5)
    d.arrow([hum.l(), aud.r()])
    out = d.box(b1[0].x, 160, w, 72, "Escalation / hand-off", "notify level owner · GHEC-AI", style="solid", ts=12.5, ss=10.5)
    d.arrow([aud.l(), out.r()])
    sr = d.box(b1[2].x + 40, 272, w + 60, 52, "Senior review", "draft withheld · rules level shown alone", style="dashed", ts=12, ss=10)
    d.arrow([val.b(), (val.cx, sr.cy), sr.r()], "fail", style="dashacc", lpos=(val.cx + 18, 270), lanchor="start")
    d.arrow([(sr.x, sr.cy), (hum.x + 20, sr.cy), (hum.x + 20, hum.y + hum.h)], None, style="dashed")
    d.arrow([b1[1].b(), (b1[1].cx, 132), (val.cx - 50, 132), (val.cx - 50, val.y)], "level used as check", style="muted", lpos=(430, 132))
    return d


@fig("dmt-ihr", "<b>The notification logic DMT-PHE digitises (IHR 2005 Annex 2, Kenya adaptation).</b> Some diseases are always notifiable; others always go through the algorithm; any other event of concern is assessed against four questions. Kenya's version lists wild poliovirus, new influenza subtypes, SARS and COVID-19 as always notifiable, and adds inter-county spread to the third question. Simplified for orientation — the official instrument governs.", wide=True)
def dmt_ihr():
    d = Diagram(760, 356, "Event detected leads to three entry paths: always-notifiable diseases notify directly; any event of potential concern and listed diseases go through four questions on serious impact, unusual or unexpected, risk of inter-county or international spread, and risk of travel or trade restrictions; two yes answers lead to notification of KNPHI.")
    top = d.box(250, 0, 260, 40, "Event detected by surveillance", style="dark", ts=12.5)
    a = d.box(0, 76, 230, 92, "Always notify", "wild poliovirus · new influenza subtype · SARS · COVID-19", style="plain", ts=12, ss=10.5)
    b = d.box(265, 76, 230, 92, "Any event of potential concern", "unknown cause, unusual source, or not on IDSR list", ts=12, ss=10.5)
    c = d.box(530, 76, 230, 92, "Always use the algorithm", "cholera · yellow fever · VHFs; Kenya adds RVF, dengue, kala-azar, chikungunya, mpox", ts=12, ss=10.5)
    for x in (a, b, c):
        d.arrow([top.b(), (top.cx, 58), (x.cx, 58), x.t()])
    qs = ["Serious public-health impact?", "Unusual or unexpected?", "Significant risk of inter-county / international spread?", "Significant risk of travel or trade restrictions?"]
    qy = 196
    for i, q in enumerate(qs):
        d.box(265, qy + i * 34, 495, 28, f"Q{i + 1}  {q}", style="line", ts=11, align="left", pad=10)
    d.arrow([b.b(), (b.cx, qy)])
    d.arrow([c.b(), (c.cx, 182), (b.cx + 60, 182), (b.cx + 60, qy)])
    notif = d.box(0, 236, 230, 64, "Notify KNPHI", "→ WHO via IHR National Focal Point", style="solid", ts=12.5, ss=10)
    d.arrow([a.b(), notif.t()], "always", lpos=(a.cx, 202))
    d.arrow([(265, qy + 3 * 34 + 14), (245, qy + 3 * 34 + 14), (245, notif.cy), notif.r()], "2 of 4", style="accent", lpos=(251, qy + 3 * 34 - 4), lanchor="start")
    d.text(265, 344, "Rule of thumb: YES to any two → notify; otherwise reassess as information arrives.", 10.5, 600, "start", MUTED)
    return d


@fig("dmt-levels", "<b>Three escalation levels, illustrated with the Ebola/Marburg trigger card.</b> Each level names who leads, the trigger that moves an event up, and the time-bound actions. RADAR's job is to surface the evidence for each trigger as soon as it exists; the trigger card, not the model, sets the level.", wide=True)
def dmt_levels():
    d = Diagram(760, 332, "Three ascending steps: level 1 sub-county or county response for a single suspected case; level 2 county or national response for two or more epidemiologically linked cases or a cluster among health workers; level 3 national or regional surge for laboratory-confirmed cases, multi-county spread or cross-border risk. Timelines: 24 hours isolate and notify, 72 hours deploy county rapid response team, 7 days confirm and expand contact tracing.")
    steps = [("Level 1", "Sub-county / county", "Single suspected case or death with bleeding symptoms", "isolate, IPC, notify"),
             ("Level 2", "County / national", "≥ 2 epi-linked suspected cases, or cluster among health workers", "deploy county RRT, test at KEMRI/NPHL"),
             ("Level 3", "National / regional", "Lab-confirmed case(s), multi-county spread or cross-border risk", "national activation, IHR notification")]
    from svg import wrap
    w, g = 236, 26
    for i, (lv, who, trig, act) in enumerate(steps):
        x = i * (w + g)
        y = 104 - i * 44
        st = "solid" if i == 2 else ("accent" if i == 1 else "plain")
        d.box(x, y, w, 40, f"{lv} · {who}", style=st, ts=12)
        d.rect(x, y + 46, w, 296 - y - 46, PANEL, PANEL, 1, 6)
        yy = y + 64
        for k, v in [("Trigger", trig), ("Actions", act)]:
            d.text(x + 12, yy, k.upper(), 9.5, 700, "start", MUTED, ls="0.06em")
            ls_ = wrap(v, w - 24, 11)
            for j, line in enumerate(ls_):
                d.text(x + 12, yy + 16 + j * 15, line, 11, 500, "start")
            yy += 16 + 15 * len(ls_) + 10
    tl = [("≤ 24 h", "isolate · notify PHEOC"), ("≤ 72 h", "county RRT deployed"), ("≤ 7 days", "diagnosis confirmed")]
    for i, (t, s_) in enumerate(tl):
        x = i * (w + g)
        d.text(x, 318, t, 12, 700, "start", CRIMSON)
        d.text(x + text_width(t, 12, True) + 8, 318, s_, 10.5, 500, "start", MUTED)
    return d


# =====================================================================  08 WORKFLOW
@fig("workflow-lanes", "<b>Who does what, in order.</b> Columns are actors; time runs downward. RADAR (crimson) does the assembling and timestamping; people make every decision. Level 1 events can be authorised at county level (dashed path); Level 2–3 events pass through KNPHI PHEOC before the GHEC-AI hand-off.", wide=True)
def workflow_lanes():
    d = Diagram(760, 560, "Swimlane with six actor columns: community and facility, sub-county surveillance, RADAR, county EOC, KNPHI PHEOC and response. Steps: signal reported, MER opened, verification within 24 hours, link score and draft, county confirms level, national confirms level 2 or 3, GHEC-AI matches responders, actions logged and event closed.")
    cols = ["Community & facility", "Sub-county surveillance", "RADAR (system)", "County EOC", "KNPHI PHEOC", "Response · GHEC-AI"]
    cw = 126
    for i, c in enumerate(cols):
        x = i * cw
        fill = "#F8F8F8"
        d.rect(x + 2, 0, cw - 4, 560, fill, fill, 1, 6, layer="back")
        from svg import wrap
        for j, line in enumerate(wrap(c.upper(), cw - 16, 9.5, True)):
            d.text(x + cw / 2, 16 + j * 13, line, 9.5, 700, "middle", CRIMSON if "RADAR" in c else MUTED, layer="back", ls="0.05em")
    steps = [
        (0, "Signal reported", "m-Dharura · facility", "plain"),
        (2, "MER opened", "detection stamped", "accent"),
        (1, "Verify ≤ 24 h", "call · visit · discard", "plain"),
        (2, "Link and score", "DMT-PHE draft ready", "accent"),
        (3, "Confirm level", "confirm or override", "dark"),
        (4, "L2–3: national", "confirm · activate", "dark"),
        (5, "Match team", "GHEC-AI registry", "plain"),
        (5, "Early actions", "7 actions dated", "plain"),
        (2, "7-1-7 computed", "close on criteria", "accent"),
    ]
    y0, step, h = 48, 56, 42
    bx = []
    for i, (c, t, s_, st) in enumerate(steps):
        x = c * cw + 9
        bx.append(d.box(x, y0 + i * step, cw - 18, h, t, s_, style=st, ts=10.8, ss=9.5, pad=6))
        d.num(x, y0 + i * step, i + 1, r=9, fill=CRIMSON if st == "accent" else GRAY, size=10)
    for i in range(len(bx) - 1):
        if i == 4:
            continue
        a, b = bx[i], bx[i + 1]
        if abs(a.cx - b.cx) < 1:
            d.arrow([a.b(), b.t()])
        elif b.cx > a.cx:
            d.arrow([a.r(), (b.cx, a.cy), b.t()])
        else:
            d.arrow([a.l(), (b.cx, a.cy), b.t()])
    a, b = bx[4], bx[5]
    d.arrow([a.r(), (b.cx, a.cy), b.t()], "L2–3")
    d.arrow([(a.cx, a.y + h), (a.cx, bx[6].cy), bx[6].l()], "L1: county authorises", style="dashed", lpos=(a.cx + 6, bx[6].cy - 12), lanchor="start")
    return d


@fig("ghec-seq", "<b>The GHEC-AI hand-off, step by step.</b> Only after a named officer authorises escalation does RADAR send GHEC-AI the minimum necessary operational fields (event ID, hazard, location, level, capacities needed) — no patient identifiers. Deployment status flows back so the response timestamps land on the same MER event.", wide=True)
def ghec_seq():
    d = Diagram(760, 380, "Sequence diagram with lifelines EOC officer, DMT-PHE agent, MER, GHEC-AI and responders, showing approval, decision logging, minimum-necessary hand-off, matching, proposed team approval, mobilisation and status written back to the MER.")
    lifelines = ["EOC officer", "DMT-PHE agent", "MER", "GHEC-AI", "Responders"]
    X = [70, 226, 382, 538, 690]
    for x, n in zip(X, lifelines):
        st = "dark" if n == "EOC officer" else ("solid" if n == "DMT-PHE agent" else ("accent" if n == "MER" else "plain"))
        d.box(x - 60, 0, 120, 36, n, style=st, ts=11.5)
        d.line(x, 36, x, 370, LINE, 1, dash="3 4", layer="back")
    msgs = [(0, 1, "1 approve Level 2 + mobilisation"), (1, 2, "2 log decision · timestamp"), (1, 3, "3 hand-off: minimum necessary fields"),
            (3, 3, "4 match team to needs"), (3, 0, "5 proposed team"), (0, 3, "6 approve deployment"),
            (3, 4, "7 mobilise"), (3, 2, "8 status + response timestamps")]
    y = 64
    for a, b, t in msgs:
        if a == b:
            x = X[a]
            d.arrow([(x, y), (x + 40, y), (x + 40, y + 18), (x + 2, y + 18)], None)
            d.text(x + 46, y + 9, t, 10.5, 600, "start", MUTED)
            y += 40
            continue
        style = "accent" if t.startswith("3") else "solid"
        d.arrow([(X[a] + (2 if b > a else -2), y), (X[b] + (-2 if b > a else 2), y)], None, style=style)
        mid = (X[a] + X[b]) / 2
        d.text(mid, y - 9, t, 10.5, 600, "middle", CRIMSON if style == "accent" else MUTED, halo=True)
        y += 38
    return d
