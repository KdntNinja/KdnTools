from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@hostname/db_name"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_password = generate_password_hash(request.form["password"], method="sha256")
        new_user = User(username=request.form["username"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        new_post = Post(title=request.form["title"], content=request.form["content"],
                        user_id=1)  # replace 1 with actual logged in user id
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_post.html")


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_post.html", post=post)


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
