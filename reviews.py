from flask import session
from sqlalchemy.sql import text
from db import db


def get_reviews(restaurant_id : int):

    sql = text("""
               SELECT
               rev.id
               , rev.restaurant_id
               , rev.reviewer_id
               , u.name as username
               , rev.review
               , rev.stars
               , rev.visible

               FROM reviews as rev
               LEFT JOIN users as u
               ON rev.reviewer_id = u.id

               WHERE rev.restaurant_id = :restaurant_id
               AND rev.visible = True

               """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchall()

    return reviews


def add_review(restaurant_id : int, reviewer_id : int, review: str, stars:int):

    if session.get("user_id"):
        print(session.get("user_id"))

        visible = True

        sql = text("""
                   INSERT INTO reviews
                   (restaurant_id, reviewer_id, review, stars, visible)

                   VALUES
                   (:restaurant_id, :reviewer_id, :review, :stars, :visible)
                   """)
        db.session.execute(sql, {"restaurant_id":restaurant_id, "reviewer_id":reviewer_id, "review":review, "stars":stars, "visible": visible})
        db.session.commit()

    else:
        print("vain kirjautuneet voivat jättää arvosteluja")
        print(session.get("user_id"))


def get_avg(restaurant_id : int):

    sql = text("""
               SELECT
               ROUND(AVG(stars),1) as star_avg

               FROM reviews as rev

               WHERE rev.restaurant_id = :restaurant_id
               AND rev.visible = True

               """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchone()


    return reviews