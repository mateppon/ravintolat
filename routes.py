from flask import redirect, render_template, request, session, abort
from app import app
import users
import restaurants
import reviews


@app.route("/")
def index():
    restaurants_lst = restaurants.get_top5()
    return render_template("index.html",
                           restaurants=restaurants_lst)


@app.route("/delete_review", methods= ["POST"])
def delete_review():
    if not users.is_admin():
        return redirect("/")

    if not request.form["csrf_token"]:
        return render_template("error.html", messages=[
            "Kirjadu sisään ylläpitäjänä"], go_to="/register", go_to_text="Kirjaudu")

    if users.user_permission(request.form["csrf_token"]):
        review_id = request.form["review_id"]
        reviews.delete_review(review_id)
        return redirect("/")
    return abort(403)


@app.route("/allrestaurants")
def allrestaurants():
    if not users.is_admin():
        return redirect("/")
    restaurant_lst = restaurants.get_restaurants()
    return render_template("allrestaurants.html", restaurants=restaurant_lst)


@app.route("/delete_restaurants", methods= ["POST"])
def delete_restaurants():
    if not users.is_admin():
        return redirect("/")

    if not request.form["csrf_token"]:
        return render_template("error.html", messages=[
            "Kirjadu sisään ylläpitäjänä"], go_to="/register", go_to_text="Kirjaudu")

    if users.user_permission(request.form["csrf_token"]):
        restaurant = request.form["name"]
        restaurants.delete_restaurant(restaurant)
        if session.get("restaurant_name"):
            del session["restaurant_name"]
        if session.get("restaurant_id"):
            del session["restaurant_id"]
        return redirect("/")
    return abort(403)


@app.route("/adminpage")
def adminpage():
    if not users.is_admin():
        return redirect("/")
    return render_template("adminpage.html")


@app.route("/delete_category", methods= ["POST"])
def delete_category():
    if not users.is_admin():
        return redirect("/")

    if not request.form["csrf_token"]:
        return render_template("error.html", messages=[
            "Kirjadu sisään ylläpitäjänä"], go_to="/register", go_to_text="Kirjaudu")

    if users.user_permission(request.form["csrf_token"]):
        category = request.form["group_name"]
        restaurants.delete_category(category)
        return redirect("/newcategory")
    return abort(403)


@app.route("/results", methods = ["POST"])
def results():
    word = request.form["description"]
    if len(word) < 1 or len(word) > 10:
        render_template("error.html", messages=[
            "Etsittävän sanan tulee olla 1-20 merkkiä pitkä."])
    restaurants_lst = restaurants.search_word(word)

    return render_template("results.html", restaurants=restaurants_lst, word= word)


@app.route("/review", methods = ["GET", "POST"])
def review():

    if request.method == "GET":
        return render_template("review.html", restaurant_name = session.get("restaurant_name"))

    if request.method == "POST":
        if not request.form["csrf_token"]:
            return render_template("error.html", messages=[
                "Vain kirjautuneet käyttäjät voivat jättää arvion"],
                  go_to="/", go_to_text="Palaa etusivulle")
        if users.user_permission(request.form["csrf_token"]):
            restaurant_id = session.get("restaurant_id")
            user_id = session.get("user_id")
            review_text = request.form["reviewText"]
            stars = request.form["stars"]

            if reviews.review_ok(review_text, stars):
                reviews.add_review(restaurant_id, user_id, review_text, stars)
                return redirect ("/")
            return render_template("error.html", messages=
                                   ["Arvion pituus pitää olla 2-1000 merkkiä",
                                     "Arviossa täytyy olla arvosana"],
                                       go_to="/review", go_to_text="Palaa lomakkeelle")
        return abort(403)


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
        if not users.is_admin():
            return redirect("/")

       # categories = restaurants.get_categories()
        categories = restaurants.count_groups()
        return render_template("newcategory.html", categories = categories)

    if request.method == "POST":
        if not users.is_admin():
            return redirect("/")
        category = request.form["category"]
        if not request.form["csrf_token"]:
            return abort(403)
        if users.user_permission(request.form["csrf_token"]):
            if len(category) < 4 or len(category) > 20:
                return render_template("error.html", messages=
                                           ["Kategorian nimen pitää olla 4-20 merkkiä pitkä"],
                                             go_to="/newcategory", go_to_text="Palaa")

            if not restaurants.add_category(category):
                return render_template("error.html", messages=
                                           ["Kategoria on jo olemassa."],
                                             go_to="/newcategory",
                                             go_to_text="Palaa")

            return redirect("/newcategory")
        return abort(403)


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

            return render_template("error.html", messages=messages, go_to='/newrestaurant',
                                    go_to_text="Palaa lomakkeelle")

        if not request.form["csrf_token"]:
            return redirect("/register")
        if users.user_permission(request.form["csrf_token"]):
            if restaurants.add_restaurant(name, description, categories, address):
                del session["address"]
                return redirect("/")
            del session["address"]
            return render_template("error.html", messages=[
                                    "Ravintola on jo olemassa."],
                                      go_to="/newrestaurant",
                                      go_to_text="Palaa lomakkeelle")
        del session["address"]
        return abort(403)


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

        return render_template("error.html", messages=
                               ["Virheellinen käyttäjänimi tai salasana."],
                                 go_to="/", go_to_text="Palaa etusivulle")


@app.route("/logout")
def logout():
    del session["name"]
    if not session.get("csrf_token"):
        return redirect("/")
    del session["csrf_token"]
    del session["user_role"]
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
