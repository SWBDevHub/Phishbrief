# =============================================
# PhishBrief — AI-assisted phishing triage
# app.py
# =============================================

from flask import Flask, render_template, request
from services.ai_triage import triage_email

import os
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyse", methods=["POST"])
def analyse():
    email_content = request.form.get("email_content", "").strip()
    sender_domain = request.form.get("sender_domain", "").strip()
    org_type = request.form.get("org_type", "").strip()

    if not email_content:
        return render_template("index.html", error="Please paste some email content to analyse.")

    result = triage_email(email_content, sender_domain, org_type)

    return render_template(
        "result.html",
        result=result,
        email_content=email_content,
        sender_domain=sender_domain,
        org_type=org_type
    )


if __name__ == "__main__":
    app.run(debug=True)
