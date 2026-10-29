"""All RADAR documentation diagrams. Each function returns a Diagram; FIGS maps name -> (fn, caption)."""
from svg import Diagram, CRIMSON, GRAY, MUTED, LINE, SOFT, PANEL, WHITE, MIDNIGHT, SKY, AUTUMN, VINE, GOLD, text_width

FIGS = {}


def fig(name, caption, wide=False):
    def deco(fn):
        FIGS[name] = (fn, caption, wide)
        return fn
    return deco


TRACK = {"orient": GRAY, "build": CRIMSON, "run": MIDNIGHT, "govern": SKY, "deliver": AUTUMN}


def lane_label(d, y, h, label, color):
    d.rect(10, y + 12, 4, h - 24, color, color, 1, 2)
    d.text(22, y + h / 2, label, 11, 700, "start", MUTED, ls="0.08em")


# =====================================================================  00 HUB
@fig("docmap", "<b>The document set at a glance.</b> Read top to bottom: the problem and landscape shape the data contract (MER); the build documents turn it into a working system; operations put it into EOCs; trust-and-safety documents constrain everything above; delivery documents turn the evidence into gate decisions. Click any box to open that document.")
def docmap():
    d = Diagram(760, 600, "Map of the 19 RADAR documents grouped into Orientation, Build, Run, Govern and Deliver lanes, with arrows showing how each feeds the next.")
    # lanes
    lanes = [(8, 88, "ORIENT", TRACK["orient"]), (104, 116, "BUILD", TRACK["build"]), (228, 88, "RUN", TRACK["run"]),
             (324, 88, "GOVERN", TRACK["govern"]), (420, 172, "DELIVER", TRACK["deliver"])]
    for y, h, lab, col in lanes:
        d.zone(0, y, 760, h, None, fill="#F8F8F8")
        lane_label(d, y, h, lab, col)
    # orient
    b01 = d.box(110, 28, 190, 48, "01 Project Overview", style="plain", ts=12.5, href="01-project-overview.html")
    b02 = d.box(330, 28, 230, 48, "02 Surveillance Landscape", style="plain", ts=12.5, href="02-surveillance-landscape.html")
    d.box(590, 28, 160, 48, "18 Glossary & References", style="dashed", ts=11.5, href="18-glossary-references.html")
    d.arrow([b01.r(), b02.l()], None)
    # build
    xs = [110, 241, 372, 503, 634]
    names = [("03 Minimum Event Record", "03-minimum-event-record.html"), ("04 System Architecture", "04-system-architecture.html"),
             ("05 Interoperability", "05-interoperability.html"), ("06 Intelligence Layer", "06-intelligence-layer.html"),
             ("07 DMT-PHE & AI Agent", "07-dmt-phe-ai-agent.html")]
    bb = []
    for x, (n, h) in zip(xs, names):
        bb.append(d.box(x, 140, 116, 56, n, style="accent" if n.startswith("03") else "plain", ts=11.5, href=h))
    for a, b in zip(bb, bb[1:]):
        d.arrow([a.r(), b.l()])
    d.arrow([b02.b(), (b02.cx, 112), (bb[0].cx, 112), bb[0].t()], "sources shape the record", lpos=(300, 112))
    # run
    b08 = d.box(500, 246, 250, 50, "08 Signal-to-Response Workflow", ts=12, href="08-signal-to-response.html")
    b09 = d.box(220, 246, 230, 50, "09 Deployment & Adoption", ts=12, href="09-deployment-adoption.html")
    d.arrow([bb[4].b(), (bb[4].cx, 246)], "recommendations", lpos=(bb[4].cx, 222), lanchor="middle")
    d.arrow([b08.l(), b09.r()], "taught at")
    # govern
    g = [d.box(110, 344, 200, 48, "10 Data Governance", ts=12, href="10-data-governance.html"),
         d.box(330, 344, 200, 48, "11 Security & Infrastructure", ts=12, href="11-security-infrastructure.html"),
         d.box(550, 344, 200, 48, "12 Responsible AI", ts=12, href="12-responsible-ai.html")]
    for gb in g:
        d.arrow([gb.t(), (gb.cx, 312)], style="dashed")
    d.text(118, 312, "constrain build & run ↑", 10.5, 600, "start", MUTED, halo=True)
    # deliver
    fx = [(110, "14 MEL Framework", "14-mel-framework.html"), (270, "15 Partners & Governance", "15-partners-governance.html"),
          (430, "16 Budget & Resources", "16-budget-resources.html"), (590, "17 Risk Register", "17-risk-register.html")]
    feeders = [d.box(x, 438, 150, 44, t, ts=11.5, href=h) for x, t, h in fx]
    for f in feeders:
        d.line(f.cx, f.y + f.h, f.cx, 504, GRAY, 1.4)
    d.line(feeders[0].cx, 504, feeders[-1].cx, 504, GRAY, 1.4)
    b13 = d.box(270, 528, 260, 50, "13 Roadmap & Stage Gates", sub="go / no-go and payment", style="solid", ts=12.5, ss=11, href="13-roadmap-stage-gates.html")
    d.arrow([(400, 504), b13.t()])
    d.text(560, 553, "evidence · people · money · risk", 10.5, 600, "start", MUTED)
    return d


# =====================================================================  01 OVERVIEW
@fig("before-after", "<b>Today vs. with RADAR.</b> Today each system holds its own piece of one outbreak under its own ID, so the EOC must rebuild the story by hand. With RADAR each system publishes a few standard fields to a shared Minimum Event Record, so the same event has one identity and one timeline that DMT-PHE can act on.")
def before_after():
    d = Diagram(760, 340, "Side-by-side comparison: today five systems hold separate IDs for the same outbreak with no link; with RADAR they all link to one Minimum Event Record that feeds DMT-PHE.")
    d.zone(0, 0, 370, 340, "Today", fill="#F8F8F8")
    d.zone(390, 0, 370, 340, "With RADAR", fill="#F8F8F8", lcolor=CRIMSON)
    srcs = [("Community signal", "m-Dharura #S-118"), ("Animal report", "KABS case #22"), ("Case counts", "KHIS2 weekly form"),
            ("Lab result", "LIMS ref #83"), ("Response decision", "EOC spreadsheet row")]
    for i, (t, s) in enumerate(srcs):
        y = 34 + i * 58
        d.box(16, y, 150, 46, t, s, ts=11.5, ss=10.5, align="left")
        d.arrow([(166, y + 23), (214, y + 23)], style="muted", head="none")
        d.text(222, y + 23, "?", 15, 700, "middle", CRIMSON)
        d.box(390 + 16, y, 150, 46, t, s, ts=11.5, ss=10.5, align="left")
    d.box(240, 120, 116, 96, "Manual reconstruction", "phone calls, re-typing, memory", style="dashed", ts=11.5, ss=10.5)
    d.text(185, 318, "No shared event ID · timestamps scattered", 11, 600, "middle", MUTED)
    mer = d.box(600, 92, 150, 120, "MER", "RVF-ISI-2026-001 · one ID, one timeline", style="accent", ts=14, ss=10.5)
    for i in range(5):
        y = 34 + i * 58 + 23
        d.arrow([(556, y), (578, y), (578, mer.cy), (600, mer.cy)] if False else [(556, y), (585, y), (585, min(max(y, 100), 204)), (600, min(max(y, 100), 204))], style="accent", head="end" if 100 <= y <= 204 or True else "none")
    dmt = d.box(600, 246, 150, 50, "DMT-PHE", "classify · escalate", style="solid", ts=12, ss=10.5)
    d.arrow([mer.b(), dmt.t()], style="accent")
    d.text(575, 318, "publish a few fields · subscribe to the rest", 11, 600, "middle", CRIMSON)
    return d


@fig("loop", "<b>The detection-to-action loop RADAR shortens.</b> Each hand-over in the loop is where time is lost today. RADAR automates the first three steps, keeps a human in charge of the decision, and records every timestamp so the loop can be measured against 7-1-7.")
def loop():
    d = Diagram(760, 250, "Six-step loop: ingest signals, link to an event, score risk, classify and escalate with human confirmation, mobilise response, learn from outcomes back to ingest.")
    steps = [("Ingest", "multi-stream feeds"), ("Link", "one event record"), ("Score", "anomaly + risk"),
             ("Decide", "DMT-PHE + human"), ("Mobilise", "GHEC-AI, EOC"), ("Learn", "overrides, outcomes")]
    w, gap, y = 106, 20, 60
    boxes = []
    for i, (t, s) in enumerate(steps):
        x = 10 + i * (w + gap)
        st = "solid" if t == "Decide" else ("accent" if t in ("Ingest", "Link", "Score") else "plain")
        boxes.append(d.box(x, y, w, 64, t, s, style=st, ts=13, ss=10.5))
    for a, b in zip(boxes, boxes[1:]):
        d.arrow([a.r(), b.l()])
    d.arrow([boxes[-1].b(), (boxes[-1].cx, 170), (boxes[0].cx, 170), boxes[0].b()], "feedback improves thresholds and models", style="dashed", lpos=(380, 170))
    d.line(10, 30, 368, 30, CRIMSON, 2)
    d.text(189, 18, "AUTOMATED BY RADAR", 10.5, 700, "middle", CRIMSON, ls="0.08em")
    d.line(388, 30, 494, 30, GRAY, 2)
    d.text(441, 18, "HUMAN DECIDES", 10.5, 700, "middle", GRAY, ls="0.08em")
    d.text(380, 222, "Every arrow writes a timestamp to the MER → detection, notification and response times become measurable.", 11, 500, "middle", MUTED)
    return d


@fig("logic-model", "<b>Logic model.</b> What the grant buys (inputs), what the team does, what it produces, the change it must demonstrate by the end of the grant, and the long-term impact. The outcomes column is exactly what the stage gates and MEL framework measure.")
def logic_model():
    d = Diagram(760, 320, "Logic model with five columns: inputs, activities, outputs, outcomes and impact, connected left to right.")
    cols = [
        ("Inputs", ["US$1.5M over 3 years", "Consortium team", "KNPHI data & EOCs", "DMT-PHE prototype"]),
        ("Activities", ["Define MER", "Build connectors", "Build analytics & agent", "Train & deploy", "Evaluate"]),
        ("Outputs", ["MER standard", "RADAR platform", "Digital DMT-PHE", "Trained EOC staff", "User guides"]),
        ("Outcomes", ["Faster detection", "Shorter detect → escalate", "Better 7-1-7", "Accurate AI classification"]),
        ("Impact", ["Earlier containment", "Disease-agnostic platform", "Regional reference"]),
    ]
    w, gap = 140, 15
    for i, (h, items) in enumerate(cols):
        x = i * (w + gap)
        st = "solid" if h == "Outcomes" else "dark" if h == "Impact" else "plain"
        d.box(x, 10, w, 34, h, style=st if st != "plain" else "soft", ts=12.5)
        for j, it in enumerate(items):
            d.box(x, 56 + j * 50, w, 40, it, style="accent" if h == "Outcomes" else "plain", ts=10.8, tw=600)
        if i < 4:
            d.arrow([(x + w + 1, 27), (x + w + gap - 1, 27)])
    return d


# =====================================================================  02 LANDSCAPE
@fig("landscape", "<b>Where outbreak signals live today.</b> Each sector runs its own systems, owners and reporting rhythm. RADAR replaces none of them: connectors (or LATTICE, where it is operational) bring a small, standard slice of each into the Minimum Event Record, and each source system stays authoritative for its own data. Phase tags show the recommended connection order — to be confirmed with KNPHI.", wide=True)
def landscape():
    d = Diagram(760, 446, "Grid of six sectors - human health, animal and wildlife, laboratory, environment and climate, open-source and media, outbreak management - each listing its systems and planned connection phase, all feeding connectors and then the Minimum Event Record.")
    sectors = [
        ("Human health", GRAY, [("IDSR / KHIS2", "weekly aggregates (DHIS2)", "MVP"), ("m-Dharura", "community & facility EBS", "MVP"), ("eCHIS", "community health promoters", "P2")]),
        ("Animal & wildlife", AUTUMN, [("KABS", "livestock & wildlife syndromes", "MVP"), ("EarthRanger", "wildlife health events", "P2")]),
        ("Laboratory", MIDNIGHT, [("LIMS / NPHL", "confirmations", "P1")]),
        ("Environment & climate", VINE, [("KMD", "rainfall, forecasts", "P1"), ("NDMA", "drought, vegetation", "P1")]),
        ("Open-source & media", SKY, [("WHO EIOS 2.0", "media, radio, web", "P2")]),
        ("Outbreak management", CRIMSON, [("EOC logs / DMT-PHE", "decisions, activations", "MVP"), ("ADaM / SHIELD", "line lists, contacts", "P1")]),
    ]
    cw, gx = 244, 14
    rowh = [26 + 3 * 42, 26 + 2 * 42]
    for i, (name, col, items) in enumerate(sectors):
        r, c = divmod(i, 3)
        x = c * (cw + gx)
        y = 0 if r == 0 else rowh[0] + 12
        h = rowh[r]
        d.rect(x, y, cw, h, "#F8F8F8", "#F8F8F8", 1, 6, layer="back")
        d.rect(x, y, 4, h, col, col, 1, 2)
        d.text(x + 14, y + 15, name.upper(), 10, 700, "start", MUTED, ls="0.08em")
        for j, (sysn, sub, ph) in enumerate(items):
            yy = y + 30 + j * 42
            d.rect(x + 10, yy, cw - 20, 36, WHITE, SOFT, 1, 5)
            d.text(x + 20, yy + 12, sysn, 11.5, 700, "start")
            d.text(x + 20, yy + 26, sub, 10, 400, "start", MUTED)
            lab = {"MVP": "MVP", "P1": "Phase 1", "P2": "Phase 2"}[ph]
            pw = text_width(lab, 9.5, True) + 14
            if ph == "MVP":
                d.pill(x + cw - 18 - pw / 2, yy + 18, lab, size=9.5, h=18, padx=7)
            else:
                d.rect(x + cw - 18 - pw, yy + 9, pw, 18, WHITE, LINE, 1, 9)
                d.text(x + cw - 18 - pw / 2, yy + 18.5, lab, 9.5, 700, "middle", GRAY)
    gy = rowh[0] + 12 + rowh[1]
    d.arrow([(380, gy + 4), (380, gy + 34)], "a small, standard slice of each", lpos=(380, gy + 18))
    conn = d.box(0, gy + 36, 760, 40, "Connectors", None, ts=12.5)
    d.text(470, gy + 56, "API pull · scheduled file · FHIR · LATTICE", 10.5, 400, "start", MUTED)
    mer = d.box(250, gy + 108, 260, 54, "Minimum Event Record", "one event ID · shared timestamps", style="accent", ts=12.5, ss=10.5)
    d.arrow([(380, gy + 76), mer.t()], "standard fields", style="accent", lpos=(380, gy + 92))
    d.text(530, gy + 128, "Source systems stay authoritative;", 10.5, 600, "start", MUTED)
    d.text(530, gy + 143, "RADAR stores pointers, not copies.", 10.5, 600, "start", MUTED)
    return d


# =====================================================================  03 MER
@fig("mer-linking", "<b>How four unrelated records become one event.</b> The RVF example from the project deck: each system sees part of the picture under its own ID. The linker matches them on place, time window, hazard/syndrome and species, and the MER stores the event identity plus pointers back to each source record — not copies of the data.")
def mer_linking():
    d = Diagram(760, 330, "Four source records (KMD A-104, ENV-331, KABS-22, EBS-7 with lab ref 83) pass through a linker that matches on place, time, syndrome and species, producing one MER event RVF-ISI-2026-001 with linked record pointers.")
    srcs = [("KMD · ID A-104", "Heavy rainfall + flooding forecast", GRAY),
            ("Vector signal · ENV-331", "Mosquito breeding increases", VINE),
            ("KABS · case #22", "Livestock abortions & deaths", AUTUMN),
            ("EBS-7 + Lab ref 83", "Human febrile illness, deaths", MIDNIGHT)]
    ys = []
    for i, (t, s, c) in enumerate(srcs):
        y = 14 + i * 78
        d.box(0, y, 200, 60, t, s, ts=11.5, ss=10.5, align="left", stripe=c)
        ys.append(y + 30)
    lk = d.box(246, 92, 130, 140, "Linker", "match on: place · time window · hazard / syndrome · species", style="plain", ts=12.5, ss=10.5)
    for y in ys:
        d.arrow([(200, y), (223, y), (223, lk.cy), (246, lk.cy)], head="none")
    d.arrow([(223, lk.cy), (246, lk.cy)])
    mer = d.box(420, 30, 340, 270, None, style="accent")
    d.text(438, 56, "MER  RVF-ISI-2026-001", 13, 700, "start", CRIMSON)
    rows = [("Hazard", "Suspected Rift Valley fever"), ("Place", "County → sub-county"), ("Species", "Cattle, goats, humans"),
            ("Status", "Verified → Level 2"), ("Confidence", "Probable"), ("Timestamps", "detected · notified · classified"),
            ("Linked records", "A-104 · ENV-331 · KABS-22"), ("", "EBS-7 · Lab-83")]
    for i, (k, v) in enumerate(rows):
        yy = 86 + i * 26
        d.text(438, yy, k, 11, 700, "start", GRAY)
        d.text(548, yy, v, 11, 400, "start")
        if i < len(rows) - 2:
            d.line(438, yy + 13, 744, yy + 13, SOFT, 1, layer="front")
    d.arrow([lk.r(), (420, lk.cy)], style="accent")
    d.text(590, 318, "pointers, not copies — data stays in source systems", 10.5, 600, "middle", MUTED)
    return d


@fig("mer-timeline", "<b>The event clock.</b> 7-1-7 needs three intervals: emergence → detection (≤ 7 days), detection → notification (≤ 1 day), notification → completion of seven early response actions (≤ 7 days). RADAR adds intermediate timestamps (verification, DMT-PHE classification, escalation) so the bottleneck can be located, not just the total.", wide=True)
def mer_timeline():
    d = Diagram(760, 270, "Timeline with milestones emergence, detection, notification, verified, classified, escalation decision, response authorised and early response complete; brackets show the 7-day, 1-day and 7-day targets and a 48-hour classification target.")
    ms = [(30, "Emergence", "first case / exposure"), (170, "Detection", "first recorded anywhere"), (260, "Notification", "reaches responsible authority"),
          (350, "Verified", "signal → event"), (440, "Classified", "DMT-PHE level set"), (520, "Escalated", "decision logged"),
          (600, "Authorised", "response hand-off"), (730, "Response done", "7 actions complete")]
    yline = 120
    d.line(20, yline, 745, yline, GRAY, 2, layer="front")
    for i, (x, t, s) in enumerate(ms):
        core = t in ("Emergence", "Detection", "Notification", "Response done")
        d.circle(x, yline, 7 if core else 5, CRIMSON if core else WHITE, CRIMSON if core else GRAY, 2)
        up = i % 2 == 0
        ty = 64 if up else 162
        d.line(x, yline + (-9 if up else 9), x, ty + (14 if up else -14), LINE, 1, layer="back")
        anchor = "start" if x < 60 else ("end" if x > 700 else "middle")
        d.text(x, ty, t, 11.5, 700, anchor, CRIMSON if core else None or "currentColor")
        d.text(x, ty + 15 if up else ty + 15, s, 10, 400, anchor, MUTED)
    # brackets
    def bracket(x1, x2, y, label, col=CRIMSON):
        d.line(x1, y, x2, y, col, 1.6, layer="front")
        d.line(x1, y - 5, x1, y + 5, col, 1.6, layer="front")
        d.line(x2, y - 5, x2, y + 5, col, 1.6, layer="front")
        d.text((x1 + x2) / 2, y + 14, label, 11, 700, "middle", col)
    bracket(30, 170, 214, "≤ 7 days detect")
    bracket(170, 260, 214, "≤ 1 day notify")
    bracket(260, 730, 214, "≤ 7 days early response")
    bracket(170, 440, 248, "≤ 48 h median signal → classification (Gate 2 target)", GRAY)
    d.text(20, 18, "7-1-7 MILESTONES (filled) · RADAR CHECKPOINTS (open)", 10.5, 700, "start", MUTED, ls="0.06em")
    return d


@fig("mer-states", "<b>MER lifecycle.</b> Every event moves through a small set of states. Only a verified event can be classified; every transition writes who, when and why to the audit trail. Discarded signals are kept (not deleted) because they are needed to measure false alarms.")
def mer_states():
    d = Diagram(760, 275, "State machine: Signal, Under verification, then either Discarded or Verified event, then Classified at level 1 to 3, Responding, Monitoring and Closed; escalation and de-escalation loops between levels.")
    s = {}
    y, h = 100, 52
    s["sig"] = d.box(0, y, 88, h, "Signal", "raw report", ts=12, ss=10)
    s["ver"] = d.box(114, y, 112, h, "Verifying", "triage ≤ 24 h", ts=12, ss=10)
    s["dis"] = d.box(114, 200, 112, 48, "Discarded", "kept for audit", style="dashed", ts=11.5, ss=10)
    s["evt"] = d.box(252, y, 104, h, "Verified event", None, ts=12)
    s["cls"] = d.box(382, y, 116, h, "Classified", "Level 1 · 2 · 3", style="accent", ts=12, ss=10)
    s["rsp"] = d.box(546, y, 104, h, "Responding", "7 actions", ts=12, ss=10)
    s["mon"] = d.box(546, 200, 104, 48, "Monitoring", "watch period", ts=11.5, ss=10)
    s["cls2"] = d.box(676, y, 84, h, "Closed", None, style="dark", ts=12, ss=10)
    d.arrow([s["sig"].r(), s["ver"].l()])
    d.arrow([s["ver"].b(), s["dis"].t()], "not an event", lpos=(170, 176))
    d.arrow([s["ver"].r(), s["evt"].l()])
    d.arrow([s["evt"].r(), s["cls"].l()])
    d.arrow([s["cls"].r(), s["rsp"].l()], "authorised", lpos=(522, 86))
    d.arrow([s["rsp"].b(), s["mon"].t()])
    d.arrow([s["mon"].r(), (718, s["mon"].cy), s["cls2"].b()], "criteria met", lpos=(684, 212))
    d.arrow([(s["cls"].cx - 22, y), (s["cls"].cx - 22, 58), (s["cls"].cx + 22, 58), (s["cls"].cx + 22, y)], "escalate / de-escalate", lpos=(440, 44))
    d.arrow([s["mon"].l(), (440, s["mon"].cy), (440, y + h)], "new cases", style="dashed", lpos=(490, 236))
    return d


@fig("mer-pubsub", "<b>Federated, not centralised.</b> The MER is a data standard and exchange profile. Each system publishes a handful of fields about an event and subscribes to what others have published; each remains the authoritative source for its own data and no institution has to work inside a new system.")
def mer_pubsub():
    d = Diagram(760, 300, "Hub and spoke: KHIS2, m-Dharura, KABS, LIMS, EOC log and GHEC-AI publish fields to and subscribe from a central MER exchange; full records stay in each source.")
    hub = d.box(290, 110, 180, 80, "MER exchange", "event IDs · status · timestamps · pointers", style="accent", ts=13, ss=10.5)
    spokes = [(20, 20, "KHIS2", "case counts"), (20, 120, "m-Dharura", "community signals"), (20, 220, "KABS", "animal syndromes"),
              (590, 20, "LIMS", "lab confirmation"), (590, 120, "EOC log / DMT-PHE", "decisions"), (590, 220, "GHEC-AI", "deployment status")]
    for x, y, t, s in spokes:
        b = d.box(x, y, 150, 56, t, s, ts=12, ss=10.5)
        if x < 300:
            d.arrow([b.r(-8), (230, b.cy - 8), (230, hub.cy - 8), (hub.x, hub.cy - 8)] if False else [b.r(-7), (hub.x - 40, b.cy - 7), (hub.x, hub.cy - 7 + (b.cy - 150) * 0.15)], style="accent")
            d.arrow([(hub.x, hub.cy + 7 + (b.cy - 150) * 0.15), (hub.x - 40, b.cy + 7), b.r(7)], style="muted")
        else:
            d.arrow([b.l(-7), (hub.x + hub.w + 40, b.cy - 7), (hub.x + hub.w, hub.cy - 7 + (b.cy - 150) * 0.15)], style="accent")
            d.arrow([(hub.x + hub.w, hub.cy + 7 + (b.cy - 150) * 0.15), (hub.x + hub.w + 40, b.cy + 7), b.l(7)], style="muted")
    d.line(300, 268, 330, 268, CRIMSON, 2, layer="front")
    d.text(336, 268, "publish fields", 10.5, 600, "start", MUTED)
    d.line(430, 268, 460, 268, LINE, 1.4, layer="front")
    d.text(466, 268, "subscribe to updates", 10.5, 600, "start", MUTED)
    return d
