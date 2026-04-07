"""
Baseline agents for the Email Auto-Triage system.

Contains:
- `RandomAgent`: picks a random action.
- `RuleAgent`: simple keyword-based rules (optional extension point).
"""
import random
from typing import Dict, Tuple, List

try:
    # when used as a package: `python -m email_triage.train`
    from .email_env import ACTIONS
except Exception:
    # when running the file directly or when package context isn't set
    from email_env import ACTIONS


class RandomAgent:
    """Agent that selects a random action uniformly."""

    def __init__(self, seed: int = None):
        self.random = random.Random(seed)

    def choose_action(self, email: Dict) -> int:
        return self.random.randrange(len(ACTIONS))


class RuleAgent:
    """Simple rule-based agent using keywords to map to priority/category.

    Rules are intentionally simple for a clear baseline and to be easy to
    extend into an ML model later.
    """

    def __init__(self):
        # keyword -> priority hints
        self.priority_keywords = {
            "urgent": "High",
            "asap": "High",
            "immediately": "High",
            "deadline": "High",
            "reminder": "Medium",
        }
        self.category_keywords = {
            "invoice": "Work",
            "project": "Work",
            "meeting": "Work",
            "birthday": "Personal",
            "dinner": "Personal",
            "sale": "Spam",
            "free": "Spam",
            "winner": "Spam",
        }

    def _predict_priority(self, text: str) -> str:
        txt = text.lower()
        for kw, p in self.priority_keywords.items():
            if kw in txt:
                return p
        return "Medium"

    def _predict_category(self, text: str) -> str:
        txt = text.lower()
        for kw, c in self.category_keywords.items():
            if kw in txt:
                return c
        # fallback: personal if from a non-company-like sender, else Work
        return "Personal"

    def choose_action(self, email: Dict) -> int:
        text = f"{email.get('subject','')} {email.get('body','')}"
        p = self._predict_priority(text)
        c = self._predict_category(text)
        # find matching action index
        for i, (pp, cc) in enumerate(ACTIONS):
            if pp == p and cc == c:
                return i
        # fallback to Medium/Personal index
        for i, (pp, cc) in enumerate(ACTIONS):
            if pp == "Medium" and cc == "Personal":
                return i
        return 0
