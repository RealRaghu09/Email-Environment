"""
Training loop and simple runner for the Email Auto-Triage system.

This script runs a baseline agent over the sample dataset, prints per-email
classification, tracks total reward, and prints accuracy. Results are also
saved to `results.csv` in the `email_triage` folder.
"""
import csv
import os
from typing import List

try:
    # preferred: run as a package from project root: `python -m email_triage.train`
    from email_triage.dataset import SAMPLE_EMAILS
    from email_triage.email_env import EmailTriageEnv, ACTIONS
    from email_triage.agent import RandomAgent, RuleAgent
except Exception:
    # fallback: allow running `python email_triage\train.py` from project root
    from dataset import SAMPLE_EMAILS
    from email_env import EmailTriageEnv, ACTIONS
    from agent import RandomAgent, RuleAgent


def run_episode(env: EmailTriageEnv, agent, index: int):
    state = env.reset(index)
    email = env.emails[index]
    action = agent.choose_action(email)
    _, reward, done, info = env.step(action)
    return reward, info


def main(save_csv: bool = True):
    env = EmailTriageEnv(SAMPLE_EMAILS)

    # choose an agent: RuleAgent is a better baseline than pure random
    agent = RuleAgent()

    total_reward = 0
    results = []

    for i in range(len(SAMPLE_EMAILS)):
        reward, info = run_episode(env, agent, i)
        total_reward += reward
        email = env.emails[i]
        pred = info["predicted"]
        true = info["true"]
        correct = info["correct"]

        print(f"Email {i+1}/{len(SAMPLE_EMAILS)}")
        print(f"  From: {email['sender']}")
        print(f"  Subject: {email['subject']}")
        print(f"  Predicted: {pred['priority']}, {pred['category']}")
        print(f"  True:      {true['priority']}, {true['category']}")
        print(f"  Correct: {correct}\n")

        results.append(
            {
                "subject": email["subject"],
                "sender": email["sender"],
                "pred_priority": pred["priority"],
                "pred_category": pred["category"],
                "true_priority": true["priority"],
                "true_category": true["category"],
                "correct": correct,
            }
        )

    accuracy = sum(1 for r in results if r["correct"]) / len(results)
    print(f"Total reward: {total_reward}")
    print(f"Accuracy: {accuracy*100:.1f}% ({sum(1 for r in results if r['correct'])}/{len(results)})")

    if save_csv:
        out_path = os.path.join(os.path.dirname(__file__), "results.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "subject",
                    "sender",
                    "pred_priority",
                    "pred_category",
                    "true_priority",
                    "true_category",
                    "correct",
                ],
            )
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved results to {out_path}")


if __name__ == "__main__":
    main()
