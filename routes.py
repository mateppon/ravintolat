from flask import redirect, render_template, request, session, jsonify
import json
from app import app
import users
import restaurants

@app.route("/")
def index():
    userlist = users.all_users()
    return render_template("index.html", count=len(userlist), users=userlist)

@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        if users.credentials_exists(name, password):
            session["name"] = name
            return redirect("/")

        return render_template("error.html", message = "Virheellinen käyttäjänimi tai salasana.")

@app.route("/logout")
def logout():
    del session["name"]
    return redirect("/")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 4 or len(name) > 20:
            return render_template(
                "error.html", message = "Käyttäjätunnuksen tulee olla 4-20 merkkiä.")

        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message = "Salasanat eroavat.")

        if len(password) < 8 or len(password)> 20:
            return render_template("error.html", message = "Salasanan tulee olla 8-20 merkkiä.")

        if users.register(name, password):
            return redirect("/")

        return render_template("error.html", message = "Käyttäjänimi on jo varattu.")
