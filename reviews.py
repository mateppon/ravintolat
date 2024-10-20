from flask import session
from sqlalchemy.sql import text
from db import db


def review_ok(review_text : str, stars):
    if not stars:
        return False
    if len(review_text) < 2 or len(review_text) > 1000:
        return False
    return True


def delete_review(review_id):
    sql= text(

    """
    DELETE FROM reviews
    WHERE id = :id

    """
    )
    db.session.execute(sql,{ "id":review_id})
    db.session.commit()



def get_reviews(restaurant_id : int):

    sql = text("""
               SELECT
               rev.id
               , rev.restaurant_id
               , rev.reviewer_id
               , u.name as username
               , rev.review
               , rev.stars

               FROM reviews as rev
               LEFT JOIN users as u
               ON rev.reviewer_id = u.id

               WHERE rev.restaurant_id = :restaurant_id

               """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchall()

    return reviews


def add_review(restaurant_id : int, reviewer_id : int, review: str, stars:int):

    if session.get("user_id"):
        print(session.get("user_id"))

        sql = text("""
                   INSERT INTO reviews
                   (restaurant_id, reviewer_id, review, stars)

                   VALUES
                   (:restaurant_id, :reviewer_id, :review, :stars)
                   """)
        db.session.execute(sql, {"restaurant_id":restaurant_id,
                                 "reviewer_id":reviewer_id,
                                 "review":review, "stars":stars})
        db.session.commit()

    else:
        print("vain kirjautuneet voivat jättää arvosteluja")



def get_avg(restaurant_id : int):

    sql = text("""
               SELECT
               ROUND(AVG(stars),1) as star_avg

               FROM reviews as rev

               WHERE rev.restaurant_id = :restaurant_id

               """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchone()

    return reviews
