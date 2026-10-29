"""Figures for documents 09-17."""
import math
from svg import Diagram, CRIMSON, GRAY, MUTED, LINE, SOFT, PANEL, WHITE, MIDNIGHT, SKY, AUTUMN, VINE, text_width, wrap
from figures import fig


# =====================================================================  09 DEPLOYMENT
@fig("deploy-pipeline", "<b>Every site follows the same seven steps.</b> A site does not go live until its parallel run meets the gate thresholds; if it falls short, the team remediates and extends the parallel run rather than switching on early.", wide=True)
def deploy_pipeline():
    d = Diagram(760, 236, "Seven-step site rollout: readiness assessment, ICT and access setup, training, eight-week parallel run, go or no-go, live use, support and refreshers; a no-go loops back to remediation and an extended parallel run.")
    st = [("Readiness", "people, power, network"), ("ICT & access", "devices, accounts"), ("Training", "ToT + all users"),
          ("Parallel run", "8 weeks, both paths"), ("Go / no-go", "thresholds met?"), ("Live use", "RADAR in routine use"), ("Support", "helpdesk, refreshers")]
    w, g = 96, 14
    bs = []
    for i, (t, s) in enumerate(st):
        style = "accent" if t == "Parallel run" else ("solid" if t == "Go / no-go" else ("dark" if t == "Live use" else "plain"))
        bs.append(d.box(i * (w + g), 40, w, 76, t, s, style=style, ts=12, ss=10))
    for a, b in zip(bs, bs[1:]):
        d.arrow([a.r(), b.l()], "go" if a is bs[4] else None, lpos=(a.x + a.w + 7, a.y - 10))
    d.arrow([bs[4].b(), (bs[4].cx, 170), (bs[3].cx, 170), bs[3].b()], "no-go → remediate, extend", style="dashacc", lpos=(bs[3].cx + 55, 186))
    d.text(0, 16, "WEEKS −6 TO −1", 10, 700, "start", MUTED, ls="0.06em")
    d.text(bs[3].x, 16, "WEEKS 1–8", 10, 700, "start", CRIMSON, ls="0.06em")
    d.text(bs[5].x, 16, "WEEK 9 ONWARDS", 10, 700, "start", MUTED, ls="0.06em")
    d.text(0, 220, "Site order (proposal): national EOC first (Gate 1), then five priority county EOCs (Gate 2).", 10.5, 600, "start", MUTED)
    return d


@fig("deploy-parallel", "<b>How the parallel run produces the concordance dataset.</b> Each event is decided the usual way and, separately, by RADAR + DMT-PHE. An independent expert panel classifies the same event from the same facts without seeing either answer. Comparing both paths to the panel shows accuracy, speed and where they disagree — without risking a live decision on an unvalidated tool.", wide=True)
def deploy_parallel():
    d = Diagram(760, 300, "One event feeds three paths: usual EOC process with paper DMT-PHE, RADAR plus AI recommendation, and a blinded expert panel reference; outputs are compared for concordance, timeliness and discrepancies, reviewed weekly.")
    ev = d.box(0, 110, 130, 64, "Event", "same facts, same time", style="dark", ts=13, ss=10)
    p1 = d.box(200, 20, 200, 64, "Usual process", "EOC team + paper DMT-PHE · level, time", ts=12, ss=10)
    p2 = d.box(200, 110, 200, 64, "RADAR + AI agent", "recommendation, citations, time", style="accent", ts=12, ss=10)
    p3 = d.box(200, 200, 200, 64, "Expert panel (blinded)", "reference classification", style="plain", ts=12, ss=10)
    for p in (p1, p2, p3):
        d.arrow([ev.r(), (165, ev.cy), (165, p.cy), p.l()])
    cmp_ = d.box(470, 80, 130, 124, "Compare", "agreement · speed · completeness", style="solid", ts=13, ss=10)
    for p in (p1, p2, p3):
        d.arrow([p.r(), (440, p.cy), (440, cmp_.cy), cmp_.l()])
    outs = [("Concordance", "AI vs panel, usual vs panel"), ("Timeliness", "detection → classification"), ("Discrepancy log", "reviewed weekly")]
    for i, (t, s) in enumerate(outs):
        b = d.box(640, 40 + i * 74, 120, 60, t, s, ts=11.5, ss=9.5)
        d.arrow([cmp_.r(), (620, cmp_.cy), (620, b.cy), b.l()])
    return d


# =====================================================================  10 GOVERNANCE
@fig("gov-approvals", "<b>Approvals that must be in place before live data flows (recommended sequencing).</b> Ethics, agreements, the DPIA and registration run in parallel from month 1. The DPIA must reach the Data Protection Commissioner at least 60 days before high-risk processing starts, so it sits on the critical path to the MVP. Ethics approvals and data-sharing agreements are Gate 1 conditions; the DPIA and registration are legal prerequisites for processing.", wide=True)
def gov_approvals():
    d = Diagram(760, 300, "Gantt-style chart from November 2026 to June 2027 with bars for KEMRI SERU amendment, WSU IRB extension, data-sharing agreements per source, DPIA with 60-day notice, ODPC registration and DHA alignment, converging on first live data flows and MVP acceptance by 30 June 2027.")
    months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    x0, x1 = 210, 750
    mw = (x1 - x0) / len(months)
    for i, m in enumerate(months):
        x = x0 + i * mw
        d.text(x + mw / 2, 12, m, 10.5, 600, "middle", MUTED)
        d.line(x, 22, x, 262, SOFT, 1, layer="back")
    d.text(x0, 30, "2026", 9.5, 700, "start", MUTED)
    d.text(x0 + 2 * mw + 3, 30, "2027", 9.5, 700, "start", MUTED)
    rows = [("KEMRI SERU amendment", "", 0, 3.5, GRAY), ("WSU IRB extension", "", 0, 2.5, GRAY),
            ("DSAs / MOUs per source", "", 0, 4, CRIMSON), ("DPIA submitted to ODPC", "", 0, 2, CRIMSON),
            ("60-day notice window", "", 2, 4, None), ("ODPC registration check", "", 0.5, 2, GRAY),
            ("DHA standards & hosting", "", 1, 8, MIDNIGHT)]
    for i, (t, s, a, b, c) in enumerate(rows):
        y = 44 + i * 30
        d.text(0, y + 7, t, 11, 700 if c else 500, "start", "currentColor" if c else MUTED)
        if s:
            d.text(x0 - 8, y + 7, s, 9.5, 500, "end", MUTED)
        if c:
            d.rect(x0 + a * mw + 2, y, (b - a) * mw - 4, 14, c, c, 1, 4)
        else:
            d.rect(x0 + a * mw + 2, y, (b - a) * mw - 4, 14, WHITE, CRIMSON, 1.2, 4, dash="4 3")
    xl = x0 + 4 * mw
    d.line(xl, 22, xl, 262, CRIMSON, 2, layer="front")
    d.text(xl + 6, 272, "first live data flows (target)", 10.5, 700, "start", CRIMSON)
    xm = x0 + 8 * mw - 2
    d.line(xm, 22, xm, 262, GRAY, 2, dash="5 3", layer="front")
    d.text(xm - 4, 288, "MVP accepted by 30 Jun 2027", 10.5, 700, "end", GRAY)
    return d


# =====================================================================  11 SECURITY
@fig("sec-zones", "<b>Network zones and the only paths between them.</b> Users and partner systems reach RADAR only through the edge. The data zone accepts connections only from the application zone; the AI zone has no internet egress at all; outbound calls leave through an allow-listed proxy. Encrypted backups go to a Government-authorised recovery site.", wide=True)
def sec_zones():
    d = Diagram(760, 380, "Five zones: external users and partner systems; edge zone with WAF, reverse proxy and gateway; application zone with web app, APIs, agent and analytics; data zone with PostgreSQL and FHIR, object store and audit log; AI zone with LLM server and vector store without internet egress; plus management zone and recovery site.")
    z_ext = d.zone(0, 0, 150, 300, "Outside", fill="#F8F8F8")
    z_edge = d.zone(166, 0, 150, 300, "Edge", fill="#F8F8F8")
    z_app = d.zone(332, 0, 210, 300, "Application", fill="#F8F8F8")
    z_data = d.zone(558, 0, 202, 186, "Data", fill="#F8F8F8", lcolor=CRIMSON)
    z_ai = d.zone(558, 196, 202, 104, "AI · no egress", fill="#F8F8F8", lcolor=CRIMSON)
    u = d.box(10, 30, 130, 56, "EOC users", "browser · MFA", ts=11.5, ss=10)
    ps = d.box(10, 110, 130, 56, "Partner systems", "KHIS2 · KABS · LIMS", ts=11.5, ss=10)
    gh = d.box(10, 190, 130, 56, "GHEC-AI · SMS", "outbound only", style="dashed", ts=11.5, ss=10)
    waf = d.box(176, 30, 130, 56, "WAF + proxy", "TLS 1.3 · rate limits", ts=11.5, ss=10)
    gw = d.box(176, 110, 130, 56, "OpenHIM gateway", "mutual TLS · client auth", ts=11.5, ss=10)
    eg = d.box(176, 190, 130, 56, "Egress proxy", "allow-list only", ts=11.5, ss=10)
    app = d.box(342, 30, 190, 56, "Web app + API", "RBAC from Keycloak", ts=11.5, ss=10)
    wk = d.box(342, 110, 190, 56, "Workers", "connectors · analytics", ts=11.5, ss=10)
    ag = d.box(342, 190, 190, 56, "Agent service", "MCP tools · approvals", style="solid", ts=11.5, ss=10)
    db = d.box(568, 30, 182, 44, "PostgreSQL · FHIR", "encrypted at rest", style="accent", ts=11.5, ss=10)
    ob = d.box(568, 82, 182, 44, "Object store", "raw landing", ts=11.5, ss=10)
    au = d.box(568, 134, 182, 44, "Audit log", "append-only", ts=11.5, ss=10)
    llm = d.box(568, 222, 182, 34, "LLM server (GPU)", None, ts=11.5)
    vs = d.box(568, 262, 182, 30, "Vector store", None, ts=11)
    d.arrow([u.r(), waf.l()])
    d.arrow([ps.r(), gw.l()])
    d.arrow([waf.r(), app.l()])
    d.arrow([gw.r(), wk.l()])
    d.arrow([eg.l(), gh.r()])
    d.arrow([ag.l(), eg.r()])
    d.arrow([app.r(), (550, app.cy), (550, db.cy), db.l()])
    d.arrow([wk.r(), (550, wk.cy), (550, ob.cy), ob.l()], None)
    d.arrow([ag.r(), (548, ag.cy), (548, llm.cy), llm.l()])
    mg = d.box(0, 316, 470, 54, "Management zone", "bastion with MFA · monitoring & alerting · patching · backup jobs", style="soft", ts=12, ss=10)
    dr = d.box(560, 316, 200, 54, "Recovery site", "encrypted, Government-authorised", style="dashed", ts=12, ss=10)
    d.arrow([(659, 300), dr.t()], "backups", lpos=(700, 308))
    return d


# =====================================================================  12 RESPONSIBLE AI
@fig("ai-lifecycle", "<b>The assurance loop every model version goes through.</b> A new prompt, model, retrieval index or threshold set is a new version. No version reaches users without passing offline evaluation and simulation; live monitoring feeds the next cycle.", wide=True)
def ai_lifecycle():
    d = Diagram(760, 340, "Six steps arranged in a loop: define intended use and hazards, build test sets, offline evaluation, simulation and parallel run, monitored live use, retrain or recalibrate, with a release gate in the centre.")
    steps = [("1 · Define", "intended use, hazards, metrics"), ("2 · Test sets", "SIMEX cases, past events, red-team"),
             ("3 · Offline eval", "concordance, citations, FN rate"), ("4 · Simulate", "tabletop + parallel run"),
             ("5 · Monitor live", "overrides, drift, incidents"), ("6 · Recalibrate", "versioned, re-evaluated")]
    cx, cy, rx, ry = 380, 168, 290, 120
    pos = []
    for i in range(6):
        ang = -math.pi / 2 + i * 2 * math.pi / 6
        pos.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    boxes = []
    for i, ((t, s), (x, y)) in enumerate(zip(steps, pos)):
        st = "accent" if i in (2, 3) else ("dark" if i == 4 else "plain")
        boxes.append(d.box(x - 85, y - 30, 170, 60, t, s, style=st, ts=12, ss=10))
    order = list(range(6))
    for i in order:
        a, b = boxes[i], boxes[(i + 1) % 6]
        ax, ay = a.cx, a.cy
        bx_, by = b.cx, b.cy
        # shorten to box edges along straight line
        def edge(bb, tx, ty):
            dx, dy = tx - bb.cx, ty - bb.cy
            sx = (bb.w / 2) / abs(dx) if dx else 1e9
            sy = (bb.h / 2) / abs(dy) if dy else 1e9
            s_ = min(sx, sy)
            return (bb.cx + dx * s_, bb.cy + dy * s_)
        p1 = edge(a, bx_, by)
        p2 = edge(b, ax, ay)
        d.arrow([p1, p2], style="dashed" if i == 5 else "solid")
    g = d.box(cx - 95, cy - 34, 190, 68, "Release gate", "no version ships without passing steps 3 and 4", style="solid", ts=12.5, ss=10)
    return d


# =====================================================================  13 ROADMAP
@fig("roadmap-gantt", "<b>Three years, three gates.</b> Bars follow the stage-gate paper (the funding schedule). The MVP is a hard internal deadline inside Gate 1; the eight-week parallel run and the pre-deployment baseline must both finish before the Gate 1 report. Placement of the parallel run and baseline within their windows is a recommendation.", wide=True)
def roadmap_gantt():
    d = Diagram(760, 350, "Gantt chart from November 2026 to October 2029 with Phase 0 MVP, baseline measurement, Phase 1 platform and national parallel run, Phase 2 county deployment, Phase 3 evaluation and transition, endline evaluation; milestones MVP acceptance 30 June 2027 and gates 1 to 3 with payments 2 and 3.")
    x0, x1 = 196, 752
    N = 36
    mw = (x1 - x0) / N
    X = lambda m: x0 + m * mw  # m = months since 1 Nov 2026
    years = [(0, "2026"), (2, "2027"), (14, "2028"), (26, "2029")]
    for m, y in years:
        d.line(X(m), 18, X(m), 300, LINE if m else SOFT, 1, layer="back")
        d.text(X(m) + 4, 12, y, 10.5, 700, "start", MUTED)
    for m in range(0, N + 1, 3):
        d.line(X(m), 24, X(m), 300, SOFT, 1, layer="back")
    rows = [
        ("Phase 0 · MVP", "4 components", 0, 6, CRIMSON),
        ("Baseline measurement", "pre-deployment", 1, 6, GRAY),
        ("Phase 1 · platform + national EOC", "connectors, guides, TPP", 6, 11, CRIMSON),
        ("8-week parallel run", "national EOC", 8.5, 10.5, MIDNIGHT),
        ("Phase 2 · 5 county EOCs", "hardening, training", 11, 23, CRIMSON),
        ("Phase 3 · evaluate + transition", "handover to KNPHI", 23, 36, CRIMSON),
        ("Endline evaluation", "mixed methods", 29, 34, GRAY),
    ]
    for i, (t, s, a, b, c) in enumerate(rows):
        y = 34 + i * 32
        d.text(0, y + 2, t, 11, 700, "start")
        d.text(0, y + 16, s, 9.5, 500, "start", MUTED)
        d.rect(X(a) + 1, y, (b - a) * mw - 2, 16, c, c, 1, 4)
    # milestones
    ms = [(8, "MVP accepted", "30 Jun 2027", CRIMSON), (11, "Gate 1", "PR 1 · Payment 2", GRAY), (23, "Gate 2", "PR 2 · Payment 3", GRAY), (36, "Gate 3", "final report", GRAY)]
    for m, t, s, c in ms:
        x = X(m)
        d.line(x, 26, x, 270, c, 1.6, dash="4 3", layer="front")
        d.poly([(x, 270), (x + 7, 279), (x, 288), (x - 7, 279)], c, c)
        anchor = "end" if m == 36 else ("end" if m == 8 else "start")
        dx = -10 if anchor == "end" else 10
        d.text(x + dx, 296 if m != 8 else 314, t, 11, 700, anchor, c)
        d.text(x + dx, 310 if m != 8 else 328, s, 9.5, 500, anchor, MUTED)
    return d


@fig("gate-decision", "<b>How a gate decision is made.</b> The consortium assembles the evidence pack; the review checks every milestone and threshold. A partly met gate is a hold, not a pass. For the MVP specifically, if it is not accepted by 30 June 2027 the foundation is notified within 30 days with a remediation plan — without waiting for the progress report.")
def gate_decision():
    d = Diagram(760, 236, "Flow: evidence pack, gate review, decision whether all milestones and thresholds are met; yes leads to proceed and payment release; no leads to hold and remediation plan within 30 days, then re-review.")
    e = d.box(0, 70, 150, 70, "Evidence pack", "MEL data · test reports · approvals", ts=12.5, ss=10)
    r = d.box(190, 70, 150, 70, "Gate review", "WSU · KNPHI · foundation", style="dark", ts=12.5, ss=10)
    q = d.box(380, 70, 150, 70, "All milestones + thresholds met?", None, style="accent", ts=12)
    y = d.box(580, 10, 180, 70, "Proceed", "payment released · next phase", style="solid", ts=12.5, ss=10)
    n = d.box(580, 130, 180, 70, "Hold", "remediation plan ≤ 30 days", style="dashed", ts=12.5, ss=10)
    d.arrow([e.r(), r.l()])
    d.arrow([r.r(), q.l()])
    d.arrow([(q.x + q.w, q.cy - 14), (556, q.cy - 14), (556, y.cy), y.l()], "yes", style="accent", lpos=(556, 70))
    d.arrow([(q.x + q.w, q.cy + 14), (556, q.cy + 14), (556, n.cy), n.l()], "no", lpos=(556, 148))
    d.arrow([n.b(), (n.cx, 222), (r.cx, 222), r.b()], "re-review after fixes", style="dashed", lpos=(450, 222))
    return d


@fig("thresholds", "<b>The bar rises at each gate.</b> Gate thresholds from the stage-gate paper, next to the March 2026 preliminary evaluation (11 surveillance professionals, 33 simulated interactions). The preliminary scores already clear the Gate 3 bar — the challenge is holding them under real workload, at every site, on real data.", wide=True)
def thresholds():
    d = Diagram(760, 250, "Three small charts: AI-expert concordance thresholds 0.85, 0.88, 0.90 against preliminary 0.924; System Usability Scale thresholds 75, 78, 80 against preliminary 85.2; documentation completeness thresholds 80, 85, 90 percent.")
    panels = [("AI-expert concordance", [None, 0.85, 0.88, 0.90], 0.924, (0.80, 0.95), "{:.2f}"),
              ("System Usability Scale", [None, 75, 78, 80], 85.2, (70, 90), "{:.0f}"),
              ("Documentation completeness", [None, 80, 85, 90], None, (75, 95), "{:.0f}%")]
    pw, gap = 236, 26
    cats = ["Prelim.", "Gate 1", "Gate 2", "Gate 3"]
    for i, (title, vals, pre, (lo, hi), fmt) in enumerate(panels):
        x = i * (pw + gap)
        d.text(x, 12, title, 12, 700, "start")
        top, bot = 44, 200
        Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
        d.line(x, bot, x + pw, bot, LINE, 1, layer="back")
        cx = [x + 22 + j * ((pw - 50) / 3) for j in range(4)]
        for j, c in enumerate(cats):
            d.text(cx[j], bot + 14, c, 10, 600, "middle", MUTED)
        pts = [(cx[j], Y(v)) for j, v in enumerate(vals) if v is not None]
        p = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        d.raw(f'<polyline points="{p}" fill="none" stroke="{CRIMSON}" stroke-width="2"/>', layer="mid")
        for (a, b), v in zip(pts, [v for v in vals if v is not None]):
            d.circle(a, b, 5, CRIMSON, WHITE, 2)
            d.text(a, b - 14, fmt.format(v), 10.5, 700, "middle", "currentColor", halo=True)
        if pre is not None:
            d.circle(cx[0], Y(pre), 5, WHITE, GRAY, 2)
            d.text(cx[0], Y(pre) - 14, ("{:.3f}" if pre < 1 else "{:.1f}").format(pre), 10.5, 700, "middle", GRAY, halo=True)
        else:
            d.text(cx[0], bot - 20, "n/a", 10, 600, "middle", MUTED)
    d.circle(8, 236, 5, CRIMSON, WHITE, 2)
    d.text(18, 236, "gate threshold (minimum)", 10.5, 600, "start", MUTED)
    d.circle(200, 236, 5, WHITE, GRAY, 2)
    d.text(210, 236, "preliminary result, March 2026 (simulation)", 10.5, 600, "start", MUTED)
    return d


# =====================================================================  14 MEL
@fig("mel-chain", "<b>From raw evidence to decisions.</b> Most numbers come from data RADAR already writes (MER timestamps, audit and override logs), so measurement adds little burden. Each metric answers a learning question, and the answers feed the gate, retraining and scale-up decisions.", wide=True)
def mel_chain():
    d = Diagram(760, 330, "Four columns: data sources, metrics, learning questions and decisions, connected left to right.")
    cols = [
        ("Data sources", ["MER timestamps", "Audit & override log", "Expert-panel reviews", "SUS & user surveys", "Interviews, observation", "Data-quality reports"], "plain"),
        ("Metrics", ["Detection → classification", "7-1-7 compliance", "AI-expert concordance", "False-negative rate", "Documentation completeness", "Dataset integration %"], "accent"),
        ("Learning questions", ["LQ1 Faster?", "LQ2 More accurate & usable?", "LQ3 Multi-stream adds value?", "LQ4 GHEC-AI hand-off works?"], "plain"),
        ("Decisions", ["Gate go / no-go", "Retrain / recalibrate", "Scale-up & policy"], "solid"),
    ]
    cw, gx = 172, 24
    for i, (h, items, st) in enumerate(cols):
        x = i * (cw + gx)
        d.text(x, 10, h.upper(), 10.5, 700, "start", CRIMSON if i == 1 else MUTED, ls="0.08em")
        n = len(items)
        step = 300 / 6
        off = (6 - n) * step / 2
        for j, it in enumerate(items):
            d.box(x, 26 + off + j * step, cw, step - 10, it, style=st if st != "plain" else "line", ts=11, tw=600)
        if i < 3:
            d.arrow([(x + cw + 3, 176), (x + cw + gx - 3, 176)])
    return d


# =====================================================================  15 PARTNERS
@fig("partners-org", "<b>Who is who.</b> KNPHI (with DHA) owns the system and the decisions; WSU holds the grant and leads integration; each partner owns a distinct workstream. Three standing bodies (right) keep decisions moving between quarterly reviews.", wide=True)
def partners_org():
    d = Diagram(760, 400, "Organisation diagram: Gates Foundation funds WSU Global Health Kenya as prime; government stewardship by KNPHI and DHA; consortium workstreams University of Michigan CGHE, CGP, KEMRI, KIPRE, enterprise software partner and Sobek GHEC-AI; governance bodies steering committee, technical working group and data governance group.")
    f = d.box(0, 0, 200, 48, "Gates Foundation", "funder · INV-110654", style="plain", ts=12.5, ss=10)
    w = d.box(250, 0, 260, 48, "WSU Global Health – Kenya", "prime · grant holder · PI", style="solid", ts=12.5, ss=10)
    d.arrow([f.r(), w.l()], "grant")
    d.zone(0, 72, 560, 96, "Government stewardship", fill="#F8F8F8", lcolor=GRAY)
    k = d.box(14, 96, 260, 60, "KNPHI", "owner · primary user · PHEOC · DMT-PHE steward", style="dark", ts=12.5, ss=10)
    h = d.box(286, 96, 260, 60, "Digital Health Agency (DHA)", "standards · hosting · certification", style="dark", ts=12.5, ss=10)
    d.arrow([w.b(), (w.cx, 84)], None, style="muted")
    d.zone(0, 186, 560, 206, "Consortium workstreams", fill="#F8F8F8", lcolor=GRAY)
    parts = [("WSU", "MER, fusion layer, connectors, APIs/MCP, TPP, evaluation lead"), ("UM / CGHE", "AI-enabled DMT-PHE, guardrails, containers"),
             ("CGP", "national/county rollout, training, helpdesk"), ("KEMRI", "ethics, baseline/endline, data quality"),
             ("KIPRE", "One Health linkages, stakeholders"), ("Enterprise partner (TBD)", "UI/UX, load & security testing, hardening"),
             ]
    for i, (t, s) in enumerate(parts):
        r, c = divmod(i, 3)
        d.box(14 + c * 180, 210 + r * 88, 168, 74, t, s, ts=12, ss=9.8)
    sb = d.box(600, 190, 160, 60, "Sobek · GHEC-AI", "response hand-off interface", style="dashed", ts=12, ss=10)
    gov = [("Steering committee", "quarterly · gates"), ("Technical WG", "fortnightly · design"), ("Data governance", "monthly · access, DSAs")]
    for i, (t, s) in enumerate(gov):
        d.box(600, 0 + i * 58, 160, 50, t, s, style="accent", ts=11.5, ss=9.5) if False else None
    d.zone(588, 0, 172, 176, "Governance bodies", fill="#F8F8F8", lcolor=CRIMSON)
    for i, (t, s) in enumerate(gov):
        d.box(598, 26 + i * 50, 152, 44, t, s, style="accent", ts=10.5, ss=9.5)
    d.box(600, 270, 160, 60, "Consultants", "KNPHI data governance · MEL", style="plain", ts=12, ss=10)
    return d


# =====================================================================  16 BUDGET
@fig("budget-bars", "<b>Where the US$1.5M goes (as stated in the proposal).</b> Subawards to consortium partners are over half the budget; WSU personnel and indirect costs are the next largest lines. Hover a bar for its share. The stated line items sum to more than the total — see the reconciliation note below.", wide=True)
def budget_bars():
    data = [("Subawards (cumulative)", 800000), ("Personnel & benefits", 308941), ("Indirect costs (12%)", 164032),
            ("Consultants", 157838), ("Other direct costs (P1–P3)", 74025), ("Enterprise server (Dell R770)", 36095), ("Travel", 31797)]
    d = Diagram(760, 300, "Horizontal bar chart of budget lines: subawards 800,000; personnel 308,941; indirect 164,032; consultants 157,838; other direct 74,025; server 36,095; travel 31,797 US dollars.")
    x0, x1 = 230, 680
    mx = 800000
    for i, (t, v) in enumerate(data):
        y = 10 + i * 40
        d.text(0, y + 12, t, 11.5, 600, "start")
        w = (x1 - x0) * v / mx
        # bar with rounded data-end only
        r = 4
        path = (f'<path d="M{x0},{y + 2} H{x0 + w - r} Q{x0 + w},{y + 2} {x0 + w},{y + 2 + r} V{y + 22 - r} '
                f'Q{x0 + w},{y + 22} {x0 + w - r},{y + 22} H{x0} Z" fill="{CRIMSON}"><title>{t}: US${v:,} ({v / 1500000:.0%} of US$1.5M)</title></path>')
        d.raw(path)
        d.text(x0 + w + 8, y + 12, f"${v:,}", 11, 700, "start")
    d.line(x0, 4, x0, 290, GRAY, 1, layer="front")
    return d


# =====================================================================  17 RISK
RISKS = [
    ("R1", "Data-sharing agreements slow", 3, 3), ("R2", "Source data poor / no API", 3, 2), ("R3", "Low adoption, extra workload", 2, 3),
    ("R4", "Unsafe AI recommendation", 1, 3), ("R5", "Security incident / breach", 1, 3), ("R6", "GPU / ICT procurement delay", 2, 3),
    ("R7", "Recruitment delays", 2, 2), ("R8", "Power & connectivity at counties", 3, 2), ("R9", "EOC staff turnover", 3, 2),
    ("R10", "No recurrent budget after grant", 2, 3), ("R11", "DHA certification / regulation", 2, 2), ("R12", "Late enterprise partner", 2, 2),
    ("R13", "Major outbreak diverts staff", 2, 2), ("R14", "Model drift on real data", 2, 2), ("R15", "Scope creep", 2, 2),
]


@fig("risk-heatmap", "<b>Risk map.</b> Likelihood (across) against impact (up), before mitigation. Risks in the top-right cells get a named owner and are reviewed at every steering committee and gate; details and mitigations are in the register below.", wide=True)
def risk_heatmap():
    d = Diagram(760, 330, "Three by three grid of likelihood against impact with risk IDs R1 to R15 placed in cells; R1 is high likelihood and high impact.")
    x0, y0, cw, ch = 90, 10, 190, 92
    shade = {2: "#F4F4F4", 3: "#E6E6E6", 4: "#D6D6D6", 5: "#C4C4C4", 6: "#B0B0B0"}
    for li in range(1, 4):
        for im in range(1, 4):
            x = x0 + (li - 1) * cw
            y = y0 + (3 - im) * ch
            sc = li + im
            d.rect(x, y, cw - 4, ch - 4, shade[sc] if sc < 6 else "#B8B8B8", WHITE, 1, 4, layer="back")
            items = [r for r in RISKS if r[2] == li and r[3] == im]
            for k, (rid, name, *_ ) in enumerate(items):
                col, row = divmod(k, 4)
                px = x + 12 + col * 92
                py = y + 16 + row * 20
                hot = li + im >= 5
                pill = d.pill(px, py, rid, fill=CRIMSON if hot else WHITE, color=WHITE if hot else GRAY, size=10, anchor="start", padx=7, h=18)
                if not hot:
                    d.rect(pill.x, pill.y, pill.w, pill.h, "none", LINE, 1, 9)
    for i, lab in enumerate(["Low", "Medium", "High"]):
        d.text(x0 + i * cw + cw / 2 - 2, y0 + 3 * ch + 8, lab, 11, 600, "middle", MUTED)
        d.text(x0 - 10, y0 + (2 - i) * ch + ch / 2 - 2, lab, 11, 600, "end", MUTED)
    d.text(x0 + 1.5 * cw, y0 + 3 * ch + 28, "LIKELIHOOD →", 10.5, 700, "middle", MUTED, ls="0.08em")
    d.vtext(14, y0 + 1.5 * ch, "IMPACT →", 10.5, 700, MUTED, ls="0.08em")
    return d
