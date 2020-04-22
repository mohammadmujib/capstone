
from flask import Flask, request, abort, jsonify, Blueprint
from flask_cors import CORS

from models import setup_db, Movie, Actor, db_drop_and_create_all, db

from auth.auth import requires_auth

casting = Blueprint('casting', __name__)


@casting.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    if movies == []:
        abort(404)
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
        "success": True,
        "movies": formatted_movies
    }), 200


@casting.route('/movies', methods=["POST"])
@requires_auth('post:movies')
def create_movie(payload):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
        movie = Movie(title=new_title,
                      release_date=new_release_date
                      )
        movie.insert()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/movies/<int:movie_id>', methods=["PATCH"])
@requires_auth('patch:movies')
def edit_movie(payload, movie_id):
    body = request.get_json()

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    try:
        movie.title = body.get('title', None)
        movie.release_date = body.get('release_date', None)
        movie.update()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    try:
        movie.delete()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        }),200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    if actors == []:
        abort(404)
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
        "success": True,
        "actors": formatted_actors
    }), 200
    

@casting.route('/actors', methods=["POST"])
@requires_auth('post:actors')
def create_actor(payload):
    body = request.get_json()

    new_name = body.get('name', None)
    new_gender = body.get('gender', None)
    new_age = body.get('age', None)

    try:
        actor = Actor(name=new_name,
                      gender=new_gender, age=new_age)
        actor.insert()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/actors/<int:actor_id>', methods=["PATCH"])
@requires_auth('patch:actors')
def edit_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()

    try:
        actor.name = body.get('name', None)
        actor.gender = body.get('gender', None)
        actor.age = body.get('age', None)
        actor.update()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting.route('/seed')
def add_dummy_data():
    """ Seed Database """
    db_drop_and_create_all()
    actor1 = Actor(name="Robert De Niro", gender='m', age=25)
    actor2 = Actor(name="Angelina Jolie", gender='f', age=22)
    actor3 = Actor(name="Nick Jonas", gender='f', age=32)

    movie1 = Movie(title="Titanic", release_date='01/01/2018')
    movie2 = Movie(title="Avenger", release_date='01/01/2019')
    movie3 = Movie(title="Amazing Spider man", release_date='01/01/2020')

    actor1.insert()
    actor2.insert()
    actor3.insert()
    movie1.insert()
    movie2.insert()
    movie3.insert()

    db.session.commit()
    db.session.close()

    return jsonify({
        "success": 200,
        "message": "db Populated"
    })
