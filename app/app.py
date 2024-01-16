from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ms/Desktop/Development/python-code-challenge-superheroes/code-challenge/app/db/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        hero_list = [
            {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
            for hero in heroes
        ]
        return jsonify(hero_list)

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {"id": power.id, "name": power.name, "description": power.description}
                    for power in hero.hero_powers
                ],
            }
            return jsonify(hero_data)
        else:
            return jsonify({"error": "Hero not found"}), 404

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        power_list = [
            {"id": power.id, "name": power.name, "description": power.description}
            for power in powers
        ]
        return jsonify(power_list)

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(power_data)
        else:
            return jsonify({"error": "Power not found"}), 404

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        data = request.get_json()
        if 'description' in data and len(data['description']) >= 20:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description,
            })
        else:
            return jsonify({"errors": ["validation errors"]}), 400

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()

        if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
            return jsonify({"errors": ["validation errors"]}), 400

        if data['strength'] not in ['Strong', 'Weak', 'Average']:
            return jsonify({"errors": ["validation errors"]}), 400

        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])

        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found"]}), 404

        hero_power = HeroPower(strength=data['strength'], hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": power.id, "name": power.name, "description": power.description}
                for power in hero.hero_powers
            ],
        }
        return jsonify(hero_data), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)
