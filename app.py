from io import BytesIO
from xml.sax.saxutils import escape
import re

from flask import Flask, render_template, request, send_file
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    resume = get_resume_data()
    ats = calculate_ats_score(resume)

    return render_template("preview.html", resume=resume, ats=ats)


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    resume = get_resume_data()

    pdf_file = BytesIO()

    document = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Title"],
        fontSize=24,
        textColor=HexColor("#1e3a8a"),
        spaceAfter=8,
        alignment=1,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        alignment=1,
        spaceAfter=8,
    )

    role_style = ParagraphStyle(
        "Role",
        parent=styles["Normal"],
        alignment=1,
        textColor=HexColor("#2563eb"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=HexColor("#1e3a8a"),
        spaceBefore=12,
        spaceAfter=6,
    )

    content_style = ParagraphStyle(
        "Content",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=16,
    )

    content = [
        Paragraph(escape(resume["name"]), name_style),
        Paragraph(
            escape(f'{resume["email"]} | {resume["phone"]}'),
            contact_style,
        ),
        Paragraph(escape(resume["target_role"]), role_style),
    ]

    add_section(content, "Skills", resume["skills"], heading_style, content_style)
    add_section(content, "Education", resume["education"], heading_style, content_style)
    add_section(content, "Projects", resume["projects"], heading_style, content_style)
    add_section(content, "Experience", resume["experience"], heading_style, content_style)

    document.build(content)
    pdf_file.seek(0)

    safe_name = resume["name"].replace(" ", "_") or "resume"

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=f"{safe_name}_resume.pdf",
        mimetype="application/pdf",
    )


def get_resume_data():
    return {
        "name": request.form.get("name", ""),
        "email": request.form.get("email", ""),
        "phone": request.form.get("phone", ""),
        "target_role": request.form.get("target_role", ""),
        "job_description": request.form.get("job_description", ""),
        "skills": request.form.get("skills", ""),
        "education": request.form.get("education", ""),
        "projects": request.form.get("projects", ""),
        "experience": request.form.get("experience", ""),
    }


def calculate_ats_score(resume):
    stop_words = {
        "and", "the", "with", "for", "that", "this", "will", "are",
        "you", "your", "from", "our", "their", "have", "has", "must",
        "job", "role", "work", "team", "using", "looking", "strong",
        "skills", "experience", "knowledge", "candidate",
    }

    job_words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.]*",
        resume["job_description"].lower(),
    )

    keywords = sorted(
        {word for word in job_words if word not in stop_words and len(word) > 2}
    )

    resume_text = " ".join(
        [
            resume["target_role"],
            resume["skills"],
            resume["education"],
            resume["projects"],
            resume["experience"],
        ]
    ).lower()

    matched_keywords = [
        keyword for keyword in keywords if keyword in resume_text
    ]

    missing_keywords = [
        keyword for keyword in keywords if keyword not in resume_text
    ]

    score = 0

    if keywords:
        score = round((len(matched_keywords) / len(keywords)) * 100)

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


def add_section(content, heading, text, heading_style, content_style):
    if text:
        clean_text = escape(text).replace("\n", "<br/>")

        content.append(Spacer(1, 4))
        content.append(Paragraph(heading, heading_style))
        content.append(Paragraph(clean_text, content_style))


if __name__ == "__main__":
    app.run(debug=True)