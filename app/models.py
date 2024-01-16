from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    super_name=db.Column(db.String(50), nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow)
    
    hero_powers = db.relationship('HeroPower', back_populates='hero')

class Power(db.Model):
    
    __tablename__="power"
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(50), nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow)
    
    hero_powers= db.relationship('HeroPower', back_populates='power')
    
class HeroPower(db.Model):
    
    __tablename__="hero_power"
    
    id = db.Column(db.Integer, primary_key=True)
    strength=db.Column(db.String(100),nullable=False)
    hero_id=db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id=db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False) 
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow)
    
    power = db.relationship('Power', back_populates='hero_powers')
    hero = db.relationship('Hero', back_populates='hero_powers')
    
# add any models you may need. 