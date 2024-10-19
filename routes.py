from flask import redirect, render_template, request, session, abort
from app import app
import users
import restaurants
import reviews


@app.route("/")
def index():
    restaurants_lst = restaurants.get_top5()

    return render_template("index.html", restaurants = restaurants_lst)


@app.route("/review", methods = ["GET", "POST"])
def review():

    if request.method == "GET":
        return render_template("review.html", restaurant_name = session.get("restaurant_name"))

    if request.method == "POST":
        if users.user_permission() :
            restaurant_id = session.get("restaurant_id")
            user_id = session.get("user_id")
            restaurant_name = session.get("restaurant_name")

            reviewText = request.form["reviewText"]
            stars = request.form["stars"]

            reviews.add_review(restaurant_id, user_id, reviewText, stars)

            return redirect ("/")
        return render_template("error.hmtl", messages = ["Ei oikeutta"])


@app.route("/restaurant/<name>")
def restaurant_page(name):

    restaurant = restaurants.get_restaurant(name)
    session["restaurant_id"] = restaurant.id
    session["restaurant_name"] = restaurant.name
    categories= restaurants.get_rest_categories(name)
    coordinates = restaurant.coordinates.split(",")
    lat = coordinates[0]
    lon = coordinates[1]
    all_reviews = reviews.get_reviews(restaurant.id)
    star_avg = reviews.get_avg(restaurant.id)

    return render_template("restaurant.html",
                            restaurant = restaurant,
                            categories = categories,
                            lat = lat, lon = lon,
                            all_reviews = all_reviews,
                            star_avg = star_avg)


@app.route("/newcategory", methods = ["GET", "POST"])
def newcategory():
        if request.method == "GET":
            categories = restaurants.get_categories()

            return render_template("newcategory.html", categories = categories)

        if request.method == "POST":
            category = request.form["category"]
            if users.user_permission():

                if restaurants.add_category(category) is False:
                    return render_template("error.html", messages = ["Kategoria on jo olemassa."])

                return redirect("/newcategory")
            return render_template("error.html", messages = ["Ei oikeutta."])


@app.route("/newrestaurant", methods = ["GET", "POST"])
def newrestaurant():
    if request.method == "GET":

        results = restaurants.get_categories()
        categories = []
        for row in results:
             result= {}
             result["id"] = row.id
             result["text"] = row.group_name
             categories.append(result)

        return render_template("newrestaurant.html", options = categories)

    if request.method == "POST":
        if request.is_json:
            data = request.json
            if "center" in data:
                center = data["center"]
                session["address"] = center

        address = session.get("address")
        name = request.form["name"]
        description= request.form["description"]
        categories = request.form.getlist("categories")

        if not restaurants.form_ok(address, name, description, categories):
            messages = ["Ravintolan nimen tulee olla 1-50 merkkiä pitkä.",
                        "Kuvauksen tulee olla 5-500 merkkiä pitkä.",
                        "Ravintolalle pitää valita yksi tai useampi kategoria.",
                        "Ravintolan osoite tulee etsiä kartasta."]
            if address:
                del session["address"]

            return render_template("error.html", messages=messages, go_to='/newrestaurant', go_to_text="Palaa lomakkeelle")

        if users.user_permission():
            if restaurants.add_restaurant(name, description, categories, address):
                del session["address"]
                return redirect("/")
            del session["address"]
            return render_template("error.html", messages = ["Ravintola on jo olemassa."])


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

        return render_template("error.html", messages = ["Virheellinen käyttäjänimi tai salasana."])


@app.route("/logout")
def logout():
    del session["name"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        messages = [
            "Käyttäjätunnuksen tulee olla 4-20 merkkiä.",
            "Salasanan tulee olla 8-20 merkkiä.",
        ]
        name = request.form["name"]
        if len(name) < 4 or len(name) > 20:
            return render_template(
                "error.html", messages=messages)

        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", messages=["Salasanat eroavat."])

        if len(password) < 8 or len(password)> 20:
            return render_template("error.html", messages=messages)

        if users.register(name, password):
            return redirect("/")

        return render_template("error.html", messages = ["Käyttäjänimi on jo varattu."])
