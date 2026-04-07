"""
Sample email dataset for the Email Auto-Triage system.

Each email is a dict with keys: subject, body, sender, priority, category
priority: one of ("High","Medium","Low")
category: one of ("Work","Personal","Spam")
"""

SAMPLE_EMAILS = [
    {
        "subject": "Urgent: Project deadline moved",
        "body": "We need the final report by EOD. Please update the slides.",
        "sender": "manager@company.com",
        "priority": "High",
        "category": "Work",
    },
    {
        "subject": "Dinner tonight?",
        "body": "Hey, are you free for dinner tonight at 7?",
        "sender": "friend@example.com",
        "priority": "Medium",
        "category": "Personal",
    },
    {
        "subject": "Congratulations, you won a prize!",
        "body": "Click this link to claim your free gift.",
        "sender": "promo@spammy.com",
        "priority": "Low",
        "category": "Spam",
    },
    {
        "subject": "Meeting request: project kickoff",
        "body": "Let's schedule a kickoff meeting next Monday.",
        "sender": "colleague@company.com",
        "priority": "High",
        "category": "Work",
    },
    {
        "subject": "Weekly newsletter",
        "body": "This week's updates and articles.",
        "sender": "newsletter@service.com",
        "priority": "Low",
        "category": "Spam",
    },
    {
        "subject": "Mom's birthday next week",
        "body": "Reminder: buy a gift for Mom's birthday.",
        "sender": "family@example.com",
        "priority": "Medium",
        "category": "Personal",
    },
    {
        "subject": "Invoice overdue",
        "body": "Your invoice is overdue; please make payment ASAP.",
        "sender": "billing@vendor.com",
        "priority": "High",
        "category": "Work",
    },
    {
        "subject": "Limited time sale",
        "body": "Huge discounts on electronics this weekend.",
        "sender": "deals@shop.com",
        "priority": "Low",
        "category": "Spam",
    },
    {
        "subject": "Catch up call?",
        "body": "Long time no see — want to catch up this week?",
        "sender": "oldfriend@example.com",
        "priority": "Medium",
        "category": "Personal",
    },
    {
        "subject": "ASAP: server down",
        "body": "The production server is down — need immediate help.",
        "sender": "ops@company.com",
        "priority": "High",
        "category": "Work",
    },
]
