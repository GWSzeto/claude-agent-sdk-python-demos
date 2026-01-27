"""Mock email data for Email Agent demo.

This module provides stubbed email data and helper functions to simulate
an email inbox without requiring actual IMAP integration.
"""

from datetime import datetime, timedelta
from typing import Any


def _days_ago(days: int) -> str:
    """Generate ISO timestamp for N days ago."""
    return (datetime.now() - timedelta(days=days)).isoformat() + "Z"


def _hours_ago(hours: int) -> str:
    """Generate ISO timestamp for N hours ago."""
    return (datetime.now() - timedelta(hours=hours)).isoformat() + "Z"


# =============================================================================
# Mock Email Database
# =============================================================================

MOCK_EMAILS: list[dict[str, Any]] = [
    # CEO/Leadership Updates (4 emails)
    {
        "id": "msg-001",
        "from": "sarah.chen@company.com",
        "to": "all-hands@company.com",
        "subject": "Weekly Update - Q4 Goals and Progress",
        "body": """Team,

I wanted to share our Q4 progress and upcoming priorities:

1. Product Launch: We're on track for the November release. Engineering has completed 85% of the features.

2. Customer Growth: We've added 50 new enterprise customers this quarter, exceeding our target by 20%.

3. Team Updates: Please welcome our new VP of Engineering, Michael Torres, starting next Monday.

4. All-Hands Meeting: Reminder that our quarterly all-hands is this Friday at 2pm PT.

Keep up the great work!
Sarah Chen, CEO""",
        "date": _days_ago(2),
        "labels": ["important", "internal", "ceo-update"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-002",
        "from": "sarah.chen@company.com",
        "to": "all-hands@company.com",
        "subject": "Weekly Update - New Partnership Announcement",
        "body": """Team,

Exciting news! We've signed a strategic partnership with TechGiant Corp.

Key highlights:
- Joint product integration launching Q1 next year
- Access to their 10M+ user base
- Co-marketing opportunities

This is a significant milestone for our company. More details in Friday's all-hands.

Sarah""",
        "date": _days_ago(9),
        "labels": ["important", "internal", "ceo-update"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-003",
        "from": "sarah.chen@company.com",
        "to": "all-hands@company.com",
        "subject": "Weekly Update - Q3 Results",
        "body": """Team,

Q3 was our best quarter yet:
- Revenue up 45% YoY
- Customer satisfaction score: 4.8/5
- Employee NPS: 72 (up from 65)

Thank you all for your hard work. Bonuses will be announced next week.

Sarah""",
        "date": _days_ago(16),
        "labels": ["important", "internal", "ceo-update"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": True
    },
    {
        "id": "msg-004",
        "from": "michael.torres@company.com",
        "to": "engineering@company.com",
        "subject": "Engineering Team - Sprint Planning Updates",
        "body": """Hi Engineering Team,

As I settle into my new role, I wanted to share some thoughts on our sprint process:

1. We'll be moving to 2-week sprints starting next month
2. Daily standups will be async via Slack
3. Friday afternoons are now protected time for tech debt

Looking forward to working with all of you!

Michael Torres
VP of Engineering""",
        "date": _days_ago(1),
        "labels": ["internal", "engineering"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },

    # Newsletters (5 emails - varying ages)
    {
        "id": "msg-005",
        "from": "newsletter@techcrunch.com",
        "to": "user@company.com",
        "subject": "TechCrunch Daily - AI Startup Raises $500M",
        "body": """Today's Top Stories:

1. AI Startup Raises $500M Series D
An AI company focused on enterprise automation has raised $500M at a $5B valuation...

2. Apple Announces New MacBook Pro
The new M4 chip promises 2x performance improvements...

3. Crypto Markets Rally
Bitcoin crosses $50,000 as institutional adoption increases...

Read more at techcrunch.com""",
        "date": _days_ago(1),
        "labels": ["newsletter"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-006",
        "from": "newsletter@techcrunch.com",
        "to": "user@company.com",
        "subject": "TechCrunch Daily - Tech Layoffs Continue",
        "body": """Today's Top Stories:

1. Major Tech Company Announces 10% Workforce Reduction
The company cited economic uncertainty and a focus on AI initiatives...

Read more at techcrunch.com""",
        "date": _days_ago(35),
        "labels": ["newsletter"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-007",
        "from": "daily@morningbrew.com",
        "to": "user@company.com",
        "subject": "Morning Brew - Markets Update",
        "body": """Good morning!

MARKETS
- S&P 500: +1.2%
- NASDAQ: +1.5%
- DOW: +0.8%

TOP STORY
The Fed signals potential rate cuts in early 2024...

TECH
New smartphone sales data shows surprising trends...

Have a great day!
Morning Brew Team""",
        "date": _days_ago(3),
        "labels": ["newsletter"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-008",
        "from": "daily@morningbrew.com",
        "to": "user@company.com",
        "subject": "Morning Brew - Weekend Edition",
        "body": """Happy Saturday!

This week's highlights...

Morning Brew Team""",
        "date": _days_ago(45),
        "labels": ["newsletter"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-009",
        "from": "digest@hackernews.com",
        "to": "user@company.com",
        "subject": "Hacker News Digest - Top Stories This Week",
        "body": """This Week's Top Stories:

1. Show HN: I built a CLI tool for managing dotfiles (892 points)
2. Why SQLite is so great for embedded systems (756 points)
3. The future of WebAssembly (634 points)

Happy hacking!""",
        "date": _days_ago(40),
        "labels": ["newsletter"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },

    # Customer Support Tickets (4 emails)
    {
        "id": "msg-010",
        "from": "john.doe@acmecorp.com",
        "to": "support@company.com",
        "subject": "URGENT: Production system down - need immediate help",
        "body": """Hi Support Team,

Our production environment is completely down. We're getting 500 errors on all API endpoints.

This is CRITICAL - we have a major client demo in 2 hours!

Error message: "Connection refused to database cluster"

Please help ASAP!

John Doe
CTO, ACME Corp
Enterprise Customer""",
        "date": _hours_ago(3),
        "labels": ["support", "urgent", "enterprise"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-011",
        "from": "jane.smith@bigtech.io",
        "to": "support@company.com",
        "subject": "Question about API rate limits",
        "body": """Hello,

We're planning to increase our usage next month and wanted to clarify the rate limits on our current plan.

Specifically:
1. What's the max requests/second?
2. Can we get a temporary increase for our product launch?

Thanks,
Jane Smith
BigTech.io""",
        "date": _days_ago(2),
        "labels": ["support"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-012",
        "from": "alex.wong@startup.co",
        "to": "support@company.com",
        "subject": "Critical: Data export not working",
        "body": """Hi,

The data export feature has been failing for the past hour. We need to export our data for a compliance audit due tomorrow.

Error: "Export timed out after 30 seconds"

This is blocking our compliance deadline!

Alex Wong
Startup.co""",
        "date": _hours_ago(6),
        "labels": ["support", "urgent"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": True
    },
    {
        "id": "msg-013",
        "from": "support@vendor.com",
        "to": "user@company.com",
        "subject": "Re: Your support ticket #12345",
        "body": """Hi,

Thank you for contacting us. We've resolved the issue with your account.

Please let us know if you have any other questions.

Best regards,
Vendor Support Team""",
        "date": _days_ago(5),
        "labels": ["support"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },

    # Invoice/Payment Emails (3 emails)
    {
        "id": "msg-014",
        "from": "billing@cloudprovider.com",
        "to": "finance@company.com",
        "subject": "Invoice #INV-2024-001 - Payment Due",
        "body": """Dear Customer,

Please find attached your invoice for cloud services.

Invoice Number: INV-2024-001
Amount Due: $12,450.00
Due Date: November 15, 2024
Status: OVERDUE (5 days)

Please remit payment at your earliest convenience.

Cloud Provider Billing Team""",
        "date": _days_ago(7),
        "labels": ["invoice", "finance"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": True
    },
    {
        "id": "msg-015",
        "from": "accounts@acmecorp.com",
        "to": "ar@company.com",
        "subject": "Payment Received - Thank You",
        "body": """Hi,

We've received your payment of $5,000 for Invoice #INV-2024-089.

Thank you for your prompt payment!

ACME Corp Accounts""",
        "date": _days_ago(3),
        "labels": ["invoice", "finance"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-016",
        "from": "billing@saasvendor.com",
        "to": "finance@company.com",
        "subject": "Upcoming renewal - Annual subscription",
        "body": """Dear Customer,

Your annual subscription will renew on December 1, 2024.

Plan: Enterprise
Amount: $24,000/year
Auto-renewal: Enabled

To make changes, please log into your account or contact us.

SaaS Vendor Team""",
        "date": _days_ago(10),
        "labels": ["invoice", "finance"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },

    # Bug Reports (3 emails)
    {
        "id": "msg-017",
        "from": "developer@clientcompany.com",
        "to": "bugs@company.com",
        "subject": "Bug Report: API returns incorrect timestamps",
        "body": """Hi,

We've noticed that the API is returning timestamps in local time instead of UTC.

Steps to reproduce:
1. Call GET /api/v1/events
2. Check the 'created_at' field
3. Compare with expected UTC time

Expected: UTC timestamp
Actual: Local timezone (PST)

This is causing issues with our data processing pipeline.

Priority: P1 - High
Affected Feature: Events API

Thanks,
Developer at Client Company""",
        "date": _days_ago(1),
        "labels": ["bug-report", "api"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-018",
        "from": "qa@partner.com",
        "to": "bugs@company.com",
        "subject": "Bug: Dashboard charts not loading on Safari",
        "body": """Hello,

The analytics dashboard charts fail to load on Safari 17.

Browser: Safari 17.0
OS: macOS Sonoma
Error in console: "WebGL context lost"

This works fine on Chrome and Firefox.

Priority: P2 - Medium
Affected Feature: Analytics Dashboard

QA Team
Partner Inc.""",
        "date": _days_ago(4),
        "labels": ["bug-report", "frontend"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": True
    },
    {
        "id": "msg-019",
        "from": "user@enterprise.com",
        "to": "bugs@company.com",
        "subject": "Critical Bug: Data loss on form submission",
        "body": """URGENT BUG REPORT

We experienced data loss when submitting a large form.

Steps to reproduce:
1. Create a form with 50+ fields
2. Fill all fields
3. Submit
4. Only 20 fields are saved

This is a critical production issue affecting our workflow.

Priority: P0 - Critical
Affected Feature: Form Builder

Enterprise Customer""",
        "date": _hours_ago(12),
        "labels": ["bug-report", "urgent", "data-loss"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },

    # Internal Communications (3 emails)
    {
        "id": "msg-020",
        "from": "hr@company.com",
        "to": "all-hands@company.com",
        "subject": "Reminder: Benefits enrollment ends Friday",
        "body": """Hi everyone,

This is a reminder that open enrollment for 2024 benefits ends this Friday.

Please log into the HR portal to:
- Review your current selections
- Make any changes for next year
- Add dependents if needed

Questions? Contact hr@company.com

HR Team""",
        "date": _days_ago(2),
        "labels": ["internal", "hr"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-021",
        "from": "facilities@company.com",
        "to": "all-hands@company.com",
        "subject": "Office closure - Thanksgiving week",
        "body": """Hi all,

The office will be closed November 23-24 for Thanksgiving.

Remote work is available for those who need it.

Happy holidays!
Facilities Team""",
        "date": _days_ago(8),
        "labels": ["internal"],
        "is_read": True,
        "folder": "inbox",
        "has_attachment": False
    },
    {
        "id": "msg-022",
        "from": "team-lead@company.com",
        "to": "engineering@company.com",
        "subject": "Team lunch - Friday 12pm",
        "body": """Hey team,

Let's do a team lunch this Friday at noon. I'm thinking the new Thai place on Market Street.

Reply if you can make it!

- Team Lead""",
        "date": _days_ago(1),
        "labels": ["internal", "social"],
        "is_read": False,
        "folder": "inbox",
        "has_attachment": False
    },
]


# =============================================================================
# Helper Functions
# =============================================================================

def search_emails(query: str, limit: int = 30) -> list[dict[str, Any]]:
    """Search emails using Gmail-style query syntax.

    Supported operators:
    - from:email - Filter by sender
    - to:email - Filter by recipient
    - subject:keyword - Filter by subject
    - is:unread / is:read - Filter by read status
    - label:name - Filter by label
    - has:attachment - Has attachments
    - newer_than:Nd - Within last N days
    - older_than:Nd - Older than N days
    - Plain text - Search in subject and body

    Args:
        query: Gmail-style search query
        limit: Maximum results to return

    Returns:
        List of matching emails
    """
    results = MOCK_EMAILS.copy()

    # Parse query into parts
    parts = query.lower().split()

    for part in parts:
        if part.startswith("from:"):
            sender = part[5:]
            results = [e for e in results if sender in e["from"].lower()]

        elif part.startswith("to:"):
            recipient = part[3:]
            results = [e for e in results if recipient in e["to"].lower()]

        elif part.startswith("subject:"):
            keyword = part[8:]
            results = [e for e in results if keyword in e["subject"].lower()]

        elif part == "is:unread":
            results = [e for e in results if not e["is_read"]]

        elif part == "is:read":
            results = [e for e in results if e["is_read"]]

        elif part.startswith("label:"):
            label = part[6:]
            results = [e for e in results if label in e["labels"]]

        elif part == "has:attachment":
            results = [e for e in results if e.get("has_attachment", False)]

        elif part.startswith("newer_than:"):
            days_str = part[11:].rstrip("d")
            try:
                days = int(days_str)
                cutoff = datetime.now() - timedelta(days=days)
                results = [e for e in results
                          if datetime.fromisoformat(e["date"].rstrip("Z")) > cutoff]
            except ValueError:
                pass

        elif part.startswith("older_than:"):
            days_str = part[11:].rstrip("d")
            try:
                days = int(days_str)
                cutoff = datetime.now() - timedelta(days=days)
                results = [e for e in results
                          if datetime.fromisoformat(e["date"].rstrip("Z")) < cutoff]
            except ValueError:
                pass

        else:
            # Plain text search in subject and body
            results = [e for e in results
                      if part in e["subject"].lower() or part in e["body"].lower()]

    # Sort by date (newest first) and limit
    results.sort(key=lambda e: e["date"], reverse=True)
    return results[:limit]


def get_emails_by_ids(ids: list[str]) -> list[dict[str, Any]]:
    """Get emails by their message IDs.

    Args:
        ids: List of message IDs to retrieve

    Returns:
        List of matching emails
    """
    return [e for e in MOCK_EMAILS if e["id"] in ids]


def get_inbox_stats() -> dict[str, Any]:
    """Get statistics about the inbox.

    Returns:
        Dictionary with inbox statistics
    """
    emails = MOCK_EMAILS

    # Count by folder
    by_folder: dict[str, int] = {}
    for email in emails:
        folder = email.get("folder", "inbox")
        by_folder[folder] = by_folder.get(folder, 0) + 1

    # Count by label
    by_label: dict[str, int] = {}
    for email in emails:
        for label in email.get("labels", []):
            by_label[label] = by_label.get(label, 0) + 1

    # Count by sender domain
    by_sender_domain: dict[str, int] = {}
    for email in emails:
        domain = email["from"].split("@")[-1]
        by_sender_domain[domain] = by_sender_domain.get(domain, 0) + 1

    return {
        "total_emails": len(emails),
        "unread_count": sum(1 for e in emails if not e["is_read"]),
        "read_count": sum(1 for e in emails if e["is_read"]),
        "with_attachments": sum(1 for e in emails if e.get("has_attachment", False)),
        "by_folder": by_folder,
        "by_label": dict(sorted(by_label.items(), key=lambda x: x[1], reverse=True)),
        "by_sender_domain": dict(sorted(by_sender_domain.items(), key=lambda x: x[1], reverse=True)[:10])
    }


def archive_email(email_id: str) -> bool:
    """Archive an email by ID.

    Args:
        email_id: The email ID to archive

    Returns:
        True if successful, False if email not found
    """
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            email["folder"] = "archive"
            return True
    return False


def add_label(email_id: str, label: str) -> bool:
    """Add a label to an email.

    Args:
        email_id: The email ID
        label: Label to add

    Returns:
        True if successful, False if email not found
    """
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            if label not in email["labels"]:
                email["labels"].append(label)
            return True
    return False


def remove_label(email_id: str, label: str) -> bool:
    """Remove a label from an email.

    Args:
        email_id: The email ID
        label: Label to remove

    Returns:
        True if successful, False if email not found
    """
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            if label in email["labels"]:
                email["labels"].remove(label)
            return True
    return False


def mark_as_read(email_id: str) -> bool:
    """Mark an email as read.

    Args:
        email_id: The email ID

    Returns:
        True if successful, False if email not found
    """
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            email["is_read"] = True
            return True
    return False
