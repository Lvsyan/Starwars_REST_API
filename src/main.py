"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Characters, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods= ['GET'])
def get_all_people():
    characters = Characters.query.all()
    characters_serialized = list(map(lambda character: character.serialize(), characters))
    return jsonify({'characters': characters_serialized}), 200

@app.route('/people/<int:people_id>', methods= ['GET'])
def get_one_people(people_id):
    character = Characters.query.get(people_id)
    character_serialized = character.serialize()
    return jsonify({'character': character_serialized}), 200

@app.route('/planets', methods= ['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda planet: planet.serialize(), planets))
    return jsonify({'planets': planets_serialized}), 200

@app.route('/planets/<int:planet_id>', methods= ['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    planet_serialized = planet.serialize()
    return jsonify({'planet': planet_serialized}), 200

@app.route('/users', methods= ['GET'])
def get_all_users():
    user = User.query.all()
    user_serialized = list(map(lambda user: user.serialize(), user))
    return jsonify({'user': user_serialized}), 200

@app.route('/users/favorites', methods= ['GET'])
def get_favorite_user():
    user = Favorite.query.all()
    user_serialized = list(map(lambda user: user.serialize(), user))
    return jsonify({'user': user_serialized}), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods= ['POST'])
def add_new_favorite_planet(user_id, planet_id):
    favorite = Favorite(favorite_user = user_id, favorite_planets = planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(({'favorite': favorite.serialize()})), 200

@app.route('/favorite/<int:user_id>/character/<int:char_id>', methods= ['POST'])
def add_new_favorite_people(user_id,char_id):
    favorite = Favorite(favorite_user = user_id, favorite_char = char_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(({'favorite': favorite.serialize()})), 200

@app.route('/favorite/planet/<int:planet_id>', methods= ['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(favorite_planets = planet_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(({'favorite': 'Se ha eliminado el planeta favorito con id: ' + str(favorite.id)})), 200

@app.route('/favorite/people/<int:people_id>', methods= ['DELETE'])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(favorite_char = people_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(({'favorite': 'Se ha eliminado el character favorito con id: ' + str(favorite.id)})), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
