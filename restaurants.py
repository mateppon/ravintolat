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
    coordinates = f"{address['lat']},{address['lng']}"

    try:
        sql = text("INSERT INTO addresses (restaurant_id, coordinates) VALUES (:restaurant_id, :coordinates)")
        db.session.execute(sql, {"restaurant_id":restaurant_id, "coordinates":coordinates})
        db.session.commit()
    except:
        return False
    return True


def add_category(group_name : str):
    creator_id = session.get("user_id")
    try:
        sql = text("INSERT INTO groups (group_name, creator_id) VALUES (:group_name, :creator_id)")
        db.session.execute(sql, {"group_name":group_name, "creator_id":creator_id})
        db.session.commit()
    except:
        return False
    return True


def get_categories():

    sql = text("""
               SELECT
               DISTINCT g.group_name
               , u.name as username

               FROM groups as g
               LEFT JOIN users as u
               ON g.creator_id = u.id

               """)
    result = db.session.execute(sql)
    categories = result.fetchall()

    return categories


def get_restaurants():

    sql = text("""

                SELECT

                rest.name
                , addr.coordinates

                FROM restaurants AS rest
                JOIN addresses AS addr
                ON rest.id = addr.restaurant_id

                LEFT JOIN reviews as rev
                ON rest.id

               """)
    result = db.session.execute(sql)
    restaurant_list= result.fetchall()

    return convert_result_to_dict(restaurant_list)


def get_top5():
    sql = text(
        """
            SELECT

             rest.name
            , addr.coordinates

                FROM restaurants AS rest
                JOIN addresses AS addr
                ON rest.id = addr.restaurant_id

                LEFT JOIN reviews as rev
                ON rest.id = rev.restaurant_id

            """
    )
    result = db.session.execute(sql)
    restaurant_list= result.fetchall()

    return convert_result_to_dict(restaurant_list)


def convert_result_to_dict(restaurant_list : list):
    new_list= []

    for restaurant in restaurant_list:
        rest = {}
        rest["name"] = restaurant.name
        coord = restaurant.coordinates
        points = coord.split(",")
        rest["lat"] = float(points[0].replace("(", ""))
        rest["lon"] = float(points[1].replace(")", ""))
        new_list.append(rest)

    return new_list
