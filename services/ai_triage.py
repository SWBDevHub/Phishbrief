# =============================================
# PhishBrief — AI-assisted phishing triage
# services/ai_triage.py
# Core analysis engine powered by Claude API
# =============================================

import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def triage_email(email_content, sender_domain="", org_type=""):
    """
    Analyse email content for phishing indicators.
    Returns structured JSON triage result.
    """

    # Build optional context block
    context_lines = []
    if sender_domain:
        context_lines.append(f"Reported sender domain: {sender_domain}")
    if org_type:
        context_lines.append(f"Target organisation type: {org_type}")
    context_block = "\n".join(context_lines) if context_lines else "No additional context provided."

    prompt = f"""You are a senior cybersecurity analyst specialising in phishing detection and email threat analysis.

Analyse the email content below and return a structured triage result.

Additional context:
{context_block}

Email content:
{email_content}

You MUST reply with ONLY a valid JSON object. No prose, no markdown, no explanation.
Return exactly this structure:

{{
  "verdict": "likely_phishing or suspicious or unclear or likely_benign",
  "risk_score": integer from 0 to 100,
  "confidence": "low or medium or high",
  "summary": "2-3 sentence plain English verdict explaining your reasoning",
  "key_indicators": [
    "specific finding 1",
    "specific finding 2"
  ],
  "technical_signals": [
    "e.g. SPF/DKIM/DMARC status, header anomalies, domain age signals, link analysis"
  ],
  "social_engineering_tactics": [
    "e.g. urgency, authority impersonation, fear, scarcity"
  ],
  "recommended_actions": [
    "ordered list of concrete analyst steps"
  ],
  "escalation_note": "one sentence — should this be escalated, and why or why not",
  "false_positive_cautions": [
    "any reasons this could be legitimate — be honest about uncertainty"
  ]
}}

Scoring guide:
0-20: Almost certainly benign
21-40: Low suspicion, minor anomalies
41-60: Suspicious, warrants review
61-80: Likely phishing, strong indicators present
81-100: High confidence phishing or confirmed malicious

Be specific. Reference actual content from the email. Do not give generic answers."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content[0].text

    try:
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        return json.loads(clean.strip())
    except json.JSONDecodeError:
        return {
            "verdict": "unclear",
            "risk_score": 0,
            "confidence": "low",
            "summary": "Analysis failed — could not parse AI response.",
            "key_indicators": [],
            "technical_signals": [],
            "social_engineering_tactics": [],
            "recommended_actions": ["Retry the analysis or review the email manually."],
            "escalation_note": "Manual review required.",
            "false_positive_cautions": [],
            "raw_response": raw
        }
