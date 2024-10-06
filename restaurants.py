from flask import session
from sqlalchemy.sql import text
from db import db




def add_restaurant(name :str, description :str, categories : list, address : str):

    creator = session.get("user_id")
    print(creator)
    visible = True

    try:
        sql = text("INSERT INTO restaurants (creator_id, name, info, visible) VALUES (:creator, :name, :info, :visible)")
        db.session.execute(sql, {"creator_id":creator, "name":name, "info":description, "visible": visible})
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

    try:
        sql = text("INSERT INTO addresses (restaurant_id, coordinates) VALUES (:restaurant_id, :address)")
        db.session.execute(sql, {"restaurant_id":restaurant_id, "coordinates":address})
        db.session.commit()
    except:
            return False


    return True







