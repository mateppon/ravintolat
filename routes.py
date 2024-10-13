from flask import redirect, render_template, request, session
from app import app
import users
import restaurants


@app.route("/")
def index():
    restaurants_lst = restaurants.get_top5()

    return render_template("index.html", restaurants = restaurants_lst)


@app.route("/newcategory", methods = ["GET", "POST"])
def newcategory():
        if request.method == "GET":
            categories = restaurants.get_categories()

            return render_template("newcategory.html", categories = categories)

        if request.method == "POST":
            category = request.form["category"]

            if restaurants.add_category(category) is False:
                return render_template("error.html", message = "Kategoria on jo olemassa.")

            return redirect("/newcategory")


@app.route("/newrestaurant", methods = ["GET", "POST"])
def newrestaurant():
    if request.method == "GET":

        categories = [
        {'id': 1, 'text': 'Ei kategoriaa'},
        {'id': 2, 'text': 'Italialainen'},
        {'id': 3, 'text': 'Aasialainen'}
        ]

        return render_template("newrestaurant.html", options = categories)

    if request.method == "POST":

        if request.is_json:
            data = request.json
            if 'center' in data:
                center = data['center']
                session["address"] = center

        address = session.get("address")
        name = request.form["name"]
        description= request.form["description"]
        categories = request.form.getlist("categories")
        restaurants.add_restaurant(name, description, categories, address)

        return redirect("/newrestaurant")


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
