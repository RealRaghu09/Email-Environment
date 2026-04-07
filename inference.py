"""
Simple inference script for the Email Auto-Triage project.

Usage examples:
  - Run on bundled sample emails:
      python inference.py --use-sample

  - Run on a CSV file (columns: subject, body, sender, optional true_priority, true_category):
      python inference.py --input-csv my_emails.csv --agent rule --save-out out.csv

This script supports two agents: `rule` (keyword-based) and `random`.
"""
import argparse
import csv
import os
from typing import List, Dict, Tuple

try:
    # package-style imports
    from email_triage.dataset import SAMPLE_EMAILS
    from email_triage.agent import RuleAgent, RandomAgent
    from email_triage.email_env import ACTIONS
except Exception:
    # fallback when running as a script from project root
    from email_triage.dataset import SAMPLE_EMAILS  # type: ignore
    from email_triage.agent import RuleAgent, RandomAgent  # type: ignore
    from email_triage.email_env import ACTIONS  # type: ignore


def load_emails_from_csv(path: str) -> List[Dict]:
    emails = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails.append({
                "subject": row.get("subject", ""),
                "body": row.get("body", ""),
                "sender": row.get("sender", ""),
                # optional ground-truth fields
                "priority": row.get("true_priority") or row.get("priority"),
                "category": row.get("true_category") or row.get("category"),
            })
    return emails


def run_inference(emails: List[Dict], agent, save_out: str = None) -> List[Dict]:
    results = []
    for i, email in enumerate(emails):
        action_idx = agent.choose_action(email)
        pred_priority, pred_category = ACTIONS[action_idx]

        true_pr = email.get("priority")
        true_cat = email.get("category")
        correct = None
        if true_pr and true_cat:
            correct = (pred_priority == true_pr) and (pred_category == true_cat)

        out = {
            "index": i,
            "sender": email.get("sender", ""),
            "subject": email.get("subject", ""),
            "pred_priority": pred_priority,
            "pred_category": pred_category,
            "true_priority": true_pr,
            "true_category": true_cat,
            "correct": correct,
        }
        results.append(out)

        # print a short summary
        print(f"[{i+1}/{len(emails)}] {out['sender']} - {out['subject']}")
        print(f"  Predicted: {pred_priority}, {pred_category}")
        if true_pr and true_cat:
            print(f"  True:      {true_pr}, {true_cat} -> {'OK' if correct else 'WRONG'}")
        print()

    if save_out:
        fieldnames = [
            "index",
            "sender",
            "subject",
            "pred_priority",
            "pred_category",
            "true_priority",
            "true_category",
            "correct",
        ]
        with open(save_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved inference results to {save_out}")

    return results


def print_summary(results: List[Dict]):
    total = len(results)
    has_labels = sum(1 for r in results if r["true_priority"] and r["true_category"])
    correct = sum(1 for r in results if r.get("correct") is True)
    print("--- Summary ---")
    print(f"Total examples: {total}")
    if has_labels:
        print(f"Labeled examples: {has_labels}")
        print(f"Correct: {correct} ({(correct/has_labels*100):.1f}%)")
    else:
        print("No ground-truth labels found; accuracy not available.")


def main():
    parser = argparse.ArgumentParser(description="Run inference for Email Auto-Triage")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--use-sample", action="store_true", help="Run on bundled sample emails")
    group.add_argument("--input-csv", type=str, help="Path to input CSV with emails")
    parser.add_argument("--agent", choices=["rule", "random"], default="rule", help="Agent to use")
    parser.add_argument("--save-out", type=str, help="Path to save CSV results")

    args = parser.parse_args()

    if args.use_sample:
        emails = SAMPLE_EMAILS
    else:
        if not os.path.exists(args.input_csv):
            raise FileNotFoundError(f"Input CSV not found: {args.input_csv}")
        emails = load_emails_from_csv(args.input_csv)

    agent = RuleAgent() if args.agent == "rule" else RandomAgent()

    results = run_inference(emails, agent, save_out=args.save_out)
    print_summary(results)


if __name__ == "__main__":
    main()
