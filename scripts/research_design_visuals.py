#!/usr/bin/env python3
"""Publishable planning figures; all numbers are assumptions, not atlas estimates."""
import json
from math import ceil, sqrt
from pathlib import Path
from statistics import NormalDist

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as MplPath

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(parents=True, exist_ok=True)
views = [
    "Evidence coverage", "Sector × disposition", "Outcome stages", "Habeas routes",
    "Technology × sector", "Topic heatmap", "Topic overlap", "Historical timeline",
    "Coding sensitivity", "Restoration evidence", "Causal assumptions",
    "Legal barriers", "Event-state trajectories", "Review funnel", "Time to relief",
    "Court-year comparisons", "Citation network", "Coder agreement", "Cluster stability",
    "Capacity × delay", "Handoff latency", "Error confusion matrix", "Recurrence control chart",
    "Intervention effects", "Correction propagation",
]
readiness = [{"rank": i+1, "view": v,
              "readiness": "Now" if i < 11 else "Enrich" if i < 19 else "Prospective"}
             for i, v in enumerate(views)]
scenarios = []
for delta in [.05, .10, .15]:
    p0, p1 = .2, .2 + delta
    pbar = (p0 + p1) / 2
    n = ceil((NormalDist().inv_cdf(.975) * sqrt(2*pbar*(1-pbar))
              + NormalDist().inv_cdf(.8) * sqrt(p0*(1-p0)+p1*(1-p1)))**2 / delta**2)
    offices = ceil(n * 1.95 / 20)
    scenarios.append({"effect_pp": round(delta*100), "per_arm_evaluable": n,
                      "independent_enrollment": 2*ceil(n/.85),
                      "clustered_enrollment": 2*offices*24})
gates = ["Explore existing atlas", "Define independent population",
         "Specify hypotheses and primary outcome", "Freeze protocol and holdout",
         "Collect to a fixed stopping rule", "Estimate effects and uncertainty",
         "Replicate and test transportability"]
data = {"status": "Research design, not empirical results or completed preregistration",
        "power_assumptions": {"baseline": .2, "alpha_two_sided": .05, "power": .8,
                              "attrition": .15, "observed_per_office": 20, "icc": .05,
                              "design_effect": 1.95, "enrolled_per_office": 24},
        "scenarios": scenarios, "visualization_readiness": readiness,
        "testing_gates": gates,
        "sources": ["https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf",
                    "https://doi.org/10.1073/pnas.1708274114",
                    "https://miguelhernan.org/whatifbook"]}
(OUT / "research-design-data.json").write_text(json.dumps(data, indent=2)+"\n")

BLACK, GOLD, TEAL, GREY = "#171717", "#B68A2D", "#007A7A", "#D8D8D2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "axes.labelsize": 13, "xtick.labelsize": 12,
                     "ytick.labelsize": 12, "svg.fonttype": "none"})
fig, axs = plt.subplots(2, 2, figsize=(22, 21))
fig.subplots_adjust(left=.16, right=.96, top=.87, bottom=.09, wspace=.40, hspace=.30)
fig.text(.06, .966, "FROM PATTERNS TO TESTABLE EVIDENCE", size=27, weight="bold")
fig.text(.06, .941, "Proposed research design • Planning assumptions, not empirical effect estimates", size=16)
fig.text(.06, .916, "Baseline 20% • Two-sided α=.05 • Power 80% • Attrition 15% • Cluster illustration: 20 observed/office, ICC .05", size=12)

ax=axs[0,0]
for j, (field, color, label) in enumerate([("independent_enrollment", GOLD, "Independent"),
                                          ("clustered_enrollment", TEAL, "Office-clustered illustration")]):
    ys=[i + (j-.5)*.32 for i in range(3)]
    vals=[s[field] for s in scenarios]
    bars=ax.barh(ys, vals, height=.30, color=color, label=label)
    ax.bar_label(bars, labels=[f"{v:,}" for v in vals], padding=5, fontsize=13)
ax.set_yticks(range(3), [f"+{s['effect_pp']} percentage points" for s in scenarios])
ax.invert_yaxis(); ax.set_xlabel("Total enrollment (people)"); ax.set_ylabel("Assumed effect")
ax.set_xlim(0,max(s["clustered_enrollment"] for s in scenarios)*1.2)
ax.set_title("A  Three sample-size scenarios", loc="left", pad=24, size=19, weight="bold")
ax.legend(loc="lower right", frameon=False, fontsize=12)
ax.spines[["top", "right"]].set_visible(False)

ax=axs[0,1]
ax.set_xlim(0,1); ax.set_ylim(-.4,6.8); ax.axis("off")
ax.set_title("B  Hypothesis-testing gates", loc="left", pad=24, size=19, weight="bold")
for i, label in enumerate(gates):
    y=6-i
    ax.scatter([.035], [y], s=120, color=GOLD if i==0 else TEAL)
    ax.text(.10,y,label,va="center",fontsize=14)
    if i < len(gates)-1:
        ax.annotate("", xy=(.035,y-.78), xytext=(.035,y-.20),
                    arrowprops={"arrowstyle":"->", "color":"#888888", "lw":1.4})
ax.text(.10,-.35,"Already viewed data remain discovery data.",fontsize=12)

ax=axs[1,0]
ax.set_title("C  Visualization readiness: ranked 1–25", loc="left", pad=25, size=19, weight="bold")
for row in readiness:
    x={"Now":0,"Enrich":1,"Prospective":2}[row["readiness"]]
    ax.scatter(x, row["rank"], s=85, color=[BLACK,GOLD,TEAL][x], marker=["o","s","D"][x])
ax.set_yticks(range(1,26),[f"{r['rank']:02d}  {r['view']}" for r in readiness])
ax.set_xticks([0,1,2],["Now", "Enrich public\nrecords", "Prospective\nmeasurement"])
ax.set_xlim(-.5,2.5); ax.set_ylim(25.8,.2)
ax.tick_params(length=0,pad=8)
ax.spines[:].set_visible(False)

ax=axs[1,1]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
ax.set_title("D  Causal structure to test", loc="left", pad=25, size=19, weight="bold")
nodes={"context":(.5,.90,"Baseline context\nload · law · resources"),
       "intervention":(.22,.63,"Intervention\nreceived"),
       "challenge":(.65,.63,"Usable\nchallenge"),
       "correction":(.65,.36,"Operative\ncorrection"),
       "selection":(.34,.09,"Historical\nselection")}
def arrow(a,b):
    x,y,_=nodes[a]; xx,yy,_=nodes[b]
    vx,vy=xx-x,yy-y; length=sqrt(vx*vx+vy*vy)
    boundary=max(abs(vx)/.172,abs(vy)/.078)
    ax.annotate("",xy=(xx-vx/boundary,yy-vy/boundary),
                xytext=(x+vx/boundary,y+vy/boundary),
                arrowprops={"arrowstyle":"->","color":"#777777","lw":1.5})
for edge in [("context","intervention"),
             ("intervention","challenge"),("challenge","correction"),
             ("correction","selection"),("context","selection")]: arrow(*edge)
ax.add_patch(FancyArrowPatch(path=MplPath([(.67,.90),(.99,.86),(.99,.45),(.83,.37)],
                                        [MplPath.MOVETO,MplPath.CURVE4,MplPath.CURVE4,MplPath.CURVE4]),
                            arrowstyle="->",mutation_scale=12,color="#777777",lw=1.5))
for x,y,label in nodes.values():
    box=FancyBboxPatch((x-.15,y-.055),.30,.11,boxstyle="round,pad=.015",facecolor="#EDF5F3",edgecolor="none")
    ax.add_patch(box); ax.text(x,y,label,ha="center",va="center",size=13)
ax.text(.04,.99,"Assumed arrows; no causal effect estimated",size=12)
fig.text(.06,.045,"Prospective identification needs: defined population, valid assignment/comparison, consistent outcomes, follow-up, and an interference plan.",size=12)
fig.text(.06,.025,"Power calculations do not repair selection bias. Causal arrows are assumptions. Future confirmatory tests require an independent evaluation dataset.",size=12)
fig.savefig(OUT/"research-design.png",dpi=170,facecolor="white")
fig.savefig(OUT/"research-design.svg",facecolor="white")
plt.close(fig)
print(OUT / "research-design.png")
