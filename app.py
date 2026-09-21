from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    resume = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "target_role": request.form.get("target_role"),
        "skills": request.form.get("skills"),
        "education": request.form.get("education"),
        "projects": request.form.get("projects"),
        "experience": request.form.get("experience"),
    }

    return render_template("preview.html", resume=resume)


if __name__ == "__main__":
    app.run(debug=True)