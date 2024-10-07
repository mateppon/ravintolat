from flask import session
from sqlalchemy.sql import text
from db import db




def add_restaurant(name :str, info :str, categories : list, address : str):

    creator_id = session.get("user_id")
    visible = True

    try:
        sql = text("INSERT INTO restaurants (creator_id, name, info, visible) VALUES (:creator_id, :name, :info, :visible)")
        db.session.execute(sql, {"creator_id":creator_id, "name":name, "info":info, "visible": visible})
        db.session.commit()
    except:
            return False

    try:

        sql = text("SELECT id FROM restaurants WHERE name=:name")
        result = db.session.execute(sql, {"name":name})
        restaurant = result.fetchone()
    except:
            return False

    restaurant_id = restaurant.id
    coordinates = (address["lat"],address["lng"])

    try:
        sql = text("INSERT INTO addresses (restaurant_id, coordinates) VALUES (:restaurant_id, :coordinates)")
        db.session.execute(sql, {"restaurant_id":restaurant_id, "coordinates":coordinates})
        db.session.commit()
    except:
            return False


    return True







