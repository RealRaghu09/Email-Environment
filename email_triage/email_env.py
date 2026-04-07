"""
EmailTriageEnv: a simple environment that simulates email classification.

This environment is intentionally lightweight and compatible with OpenAI-style
environments (i.e., has `reset` and `step`). It accepts a list of emails where
each email includes ground-truth `priority` and `category` labels.

State: the combined subject + body string
Actions: integer index corresponding to (priority, category) pairs
Reward: +1 for correct classification, -1 for incorrect
"""
from typing import List, Tuple, Dict, Any

PRIORITIES = ["High", "Medium", "Low"]
CATEGORIES = ["Work", "Personal", "Spam"]

# All possible actions: list of (priority, category) tuples
ACTIONS: List[Tuple[str, str]] = [(p, c) for p in PRIORITIES for c in CATEGORIES]


class EmailTriageEnv:
    """Simple environment for email triage.

    The environment is episodic with one step per email. It does not depend on
    any external OpenEnv package APIs, but the method signatures are familiar
    (`reset`, `step`) so it is easy to adapt to frameworks.
    """

    def __init__(self, emails: List[Dict[str, Any]]):
        self.emails = emails
        self.current_index = 0

    def reset(self, index: int = 0) -> str:
        """Reset environment to a specific email index and return state (text).

        Args:
            index: index into the provided email list. Defaults to 0.

        Returns:
            state string (subject + "\n" + body)
        """
        if index < 0 or index >= len(self.emails):
            raise IndexError("index out of range for email dataset")
        self.current_index = index
        email = self.emails[self.current_index]
        state = f"{email.get('subject','')}\n{email.get('body','')}"
        return state

    def step(self, action) -> Tuple[str, int, bool, Dict[str, Any]]:
        """Apply action and return (state, reward, done, info).

        Action may be either an integer index into ACTIONS or a tuple
        `(priority, category)`.
        """
        # normalize action
        if isinstance(action, int):
            if action < 0 or action >= len(ACTIONS):
                raise IndexError("action index out of range")
            pred_priority, pred_category = ACTIONS[action]
        elif isinstance(action, tuple) and len(action) == 2:
            pred_priority, pred_category = action
        else:
            raise ValueError("action must be int index or (priority, category) tuple")

        email = self.emails[self.current_index]
        true_priority = email.get("priority")
        true_category = email.get("category")

        correct = (pred_priority == true_priority) and (pred_category == true_category)
        reward = 1 if correct else -1

        # single-step episode
        done = True
        info = {
            "predicted": {"priority": pred_priority, "category": pred_category},
            "true": {"priority": true_priority, "category": true_category},
            "correct": correct,
        }

        # next state could be empty because episode ends; we return the same text
        state = f"{email.get('subject','')}\n{email.get('body','')}"
        return state, reward, done, info

    def action_space(self) -> List[Tuple[str, str]]:
        """Return the list of possible actions."""
        return ACTIONS
