# PhishBrief

AI-assisted phishing triage tool. Paste a suspicious email, get a structured security verdict.

## What it does

PhishBrief analyses email content using Claude AI and returns a structured triage report covering:

- **Verdict & risk score** — likelihood of phishing on a 0–100 scale with confidence rating
- **Key indicators** — specific suspicious elements identified in the email
- **Technical signals** — SPF/DKIM/DMARC assessment, domain analysis, link evaluation
- **Social engineering tactics** — urgency, authority impersonation, fear tactics, and more
- **Recommended actions** — ordered analyst steps to take
- **Escalation note** — whether and why to escalate
- **False positive cautions** — honest assessment of legitimate explanations

## Why it exists

Phishing analysis is time-consuming and inconsistent. Non-specialist staff often can't identify what makes an email suspicious, and even analysts spend significant time writing up findings manually. PhishBrief converts messy email evidence into a clean, structured brief in seconds.

## Demo

![PhishBrief input page](static/screenshots/input.png)
![PhishBrief result page](static/screenshots/result.png)

## Tech stack

- **Python / Flask** — web framework
- **Anthropic Claude API** — AI analysis engine (claude-haiku-4-5)
- **Jinja2** — templating
- **HTML / CSS** — dark, clean UI

## Getting started

**1. Clone the repo**
```bash
git clone https://github.com/SWBDevHub/Phishbrief.git
cd Phishbrief
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the root:
```
ANTHROPIC_API_KEY=your_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com)

**4. Run**
```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Project structure

```
phishbrief/
├── app.py                  # Flask routes
├── services/
│   └── ai_triage.py        # Claude API integration, structured JSON output
├── templates/
│   ├── index.html          # Input page
│   └── result.html         # Triage result page
├── static/
│   └── style.css           # Dark UI styling
└── requirements.txt
```

## Skills demonstrated

- AI workflow design — structured prompt engineering with enforced JSON output schema
- Cybersecurity domain knowledge — phishing indicators, email authentication, social engineering
- API integration — Anthropic Claude API
- Full-stack Python — Flask, Jinja2, REST routing
- Risk communication — translating technical findings into actionable analyst output

## Limitations & future work

This is a v0.1 prototype built for portfolio and learning purposes.

Planned additions:
- `.eml` file upload support
- PDF report export
- VirusTotal / URLScan API integration for live link analysis
- Batch triage mode

## Disclaimer

PhishBrief provides AI-assisted triage only. Findings should always be verified by a qualified security professional before action is taken. Not a substitute for professional security review.
