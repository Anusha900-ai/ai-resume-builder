f
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
        "skills": request.form.get("skills", ""),
        "education": request.form.get("education", ""),
        "projects": request.form.get("projects", ""),
        "experience": request.form.get("experience", ""),
    }


def add_section(content, heading, text, heading_style, content_style):
    if text:
        clean_text = escape(text).replace("\n", "<br/>")

        content.append(Spacer(1, 4))
        content.append(Paragraph(heading, heading_style))
        content.append(Paragraph(clean_text, content_style))


if __name__ == "__main__":
    app.run(debug=True)