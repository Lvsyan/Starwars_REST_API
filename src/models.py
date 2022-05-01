from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    password = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            'username': self.username
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', backref='favorites')
    favorite_char = db.Column(db.Integer, db.ForeignKey('characters.id'))
    chars = db.relationship('Characters', backref='favorites')
    favorite_planets = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', backref='favorites')
    favorite_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicles = db.relationship('Vehicles', backref='favorites')

    def serialize(self):
        return {
            'id': self.id
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))

    def serialize(self):
        return {
            'name': self.name
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    population = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    gravity = db.Column(db.String(250))

    def serialize(self):
        return {
            'name': self.name
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    cargo_capacity = db.Column(db.String(250))
    cansumables = db.Column(db.String(250))

    def serialize(self):
        return {
            'name': self.name
        }