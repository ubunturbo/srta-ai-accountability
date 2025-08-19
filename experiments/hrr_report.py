#!/usr/bin/env python3
import json, argparse, pandas as pd, matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-jsonl", default="results_hrr.jsonl")
    ap.add_argument("--input-summary", default="results_hrr_summary.json")
    ap.add_argument("--model", default="(fill: model)")
    ap.add_argument("--dataset", default="(fill: dataset)")
    ap.add_argument("--notes", default="")
    a=ap.parse_args()

    # itemwise
    rows=[]
    with open(a.input_jsonl, encoding="utf-8") as f:
        for line in f:
            if line.strip(): rows.append(json.loads(line))
    import pandas as pd
    df=pd.DataFrame(rows)
    df.to_csv("hrr_by_item.csv", index=False)

    # summary
    summ=json.load(open(a.input_summary,encoding="utf-8"))
    table=[]
    for T,s in sorted(summ.items(), key=lambda kv: float(kv[0])):
        table.append({"temperature":float(T),"per_trial_rate":s["per_trial_rate"],
                      "mean_hrr_itemwise":s["mean_hrr_itemwise"],"wilson_lo":s["wilson_ci_95"][0],
                      "wilson_hi":s["wilson_ci_95"][1],"n_items":s["n_items"],
                      "total_trials":s["total_trials"],"total_hallucinations":s["total_hallucinations"]})
    pdf=pd.DataFrame(table)
    pdf.to_csv("hrr_summary.csv", index=False)

    # plot
    plt.figure()
    plt.plot(pdf["temperature"].values, pdf["per_trial_rate"].values, marker="o")
    plt.title("Hallucination Reproduction Rate vs Temperature")
    plt.xlabel("Temperature"); plt.ylabel("Per-trial HRR")
    plt.savefig("hrr_vs_temperature.png", bbox_inches="tight")

    # md report
    lines=[]
    lines+=["# Hallucination Reproduction Rate (HRR) Report","",
            f"- **Model**: {a.model}","- **Dataset**: {a.dataset}",f"- **Generated**: {pd.Timestamp.now()}"]
    if a.notes: lines.append(f"- **Notes**: {a.notes}")
    lines+=["","## Aggregate Results",
            "Temperature | Per-trial HRR | 95% CI (Wilson) | Items | Trials | Hallucinations",
            ":--:|:--:|:--:|--:|--:|--:"]
    for r in table:
        lines.append(f"{r['temperature']:.2f} | {r['per_trial_rate']*100:.1f}% | "
                     f"{r['wilson_lo']*100:.1f}–{r['wilson_hi']*100:.1f}% | "
                     f"{r['n_items']} | {r['total_trials']} | {r['total_hallucinations']}")
    lines+=["", "![HRR vs Temperature](hrr_vs_temperature.png)", "",
            "## Method (Short)",
            "- N回生成し、ベンチマークの誤りスパン（normalized substring）出現率をHRRとして計測。",
            "- item-wise平均とper-trial率を併記し、Wilson 95%CIを付与。", ""]
    open("HRR_Report.md","w",encoding="utf-8").write("\n".join(lines))
if __name__=="__main__": main()
