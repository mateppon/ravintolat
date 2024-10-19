from flask import session, request, abort
from sqlalchemy.sql import text
from db import db


def form_ok(address, name, description, categories):
    if len(name) > 50 or len(name) < 1:
        return False
    if len(description) > 500 or len(description) < 5:
        return False
    if not address:
        return False
    return True


def add_restaurant(name :str, info :str, categories : list, address : str):

    creator_id = session.get("user_id")
    visible = True
    coordinates = f"{address['lat']},{address['lng']}"

    try:
        sql = text("INSERT INTO restaurants (creator_id, name, info, visible) VALUES (:creator_id, :name, :info, :visible) RETURNING id")
        result = db.session.execute(sql, {"creator_id":creator_id, "name":name, "info":info, "visible": visible})
        restaurant_id = result.fetchone()[0]

        sql = text("INSERT INTO addresses (restaurant_id, coordinates) VALUES (:restaurant_id, :coordinates)")
        db.session.execute(sql, {"restaurant_id":restaurant_id, "coordinates":coordinates})

        for group in categories:
            group_id = int(group)
            sql = text("INSERT INTO restaurantsGroups (restauranst_id, group_id) VALUES (:restaurant_id, :group_id)")
            db.session.execute(sql,{"restaurant_id":restaurant_id, "group_id":group_id})
            db.session.commit()
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
               g.id
               , g.group_name
               , u.name as username

               FROM groups as g
               LEFT JOIN users as u
               ON g.creator_id = u.id

               ORDER BY group_name

               """)
    result = db.session.execute(sql)
    categories = result.fetchall()

    return categories


def get_rest_categories(name : str):
    sql = text("""
               SELECT

               DISTINCT
               g.group_name

               FROM restaurants as res
               LEFT JOIN restaurantsGroups as rg
               ON res.id = rg.restauranst_id

               LEFT JOIN groups as g
               ON rg.group_id = g.id

               WHERE res.name = :name

               """)
    result = db.session.execute(sql, {"name" : name})
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

               """)
    result = db.session.execute(sql)
    restaurant_list= result.fetchall()

    return convert_result_to_dict(restaurant_list)


def get_top5():
    sql = text(
        """
            SELECT

             distinct rest.name
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


def get_restaurant(name :str):

    sql = text("""

                SELECT

                rest.id
                , rest.name
                , rest.info
                , addr.coordinates

                FROM restaurants AS rest
                JOIN addresses AS addr
                ON rest.id = addr.restaurant_id

                WHERE rest.name = :name


               """)
    result = db.session.execute(sql, {"name":name})
    restaurant_info= result.fetchone()


    return restaurant_info