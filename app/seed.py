from app import create_app, db
from models import Hero, Power, HeroPower
import random

def seed_powers():
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    powers = [Power(**power_info) for power_info in powers_data]
    db.session.add_all(powers)
    db.session.commit()

def seed_heroes():
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    heroes = [Hero(**hero_info) for hero_info in heroes_data]
    db.session.add_all(heroes)
    db.session.commit()

def add_powers_to_heroes():
    strengths = ["Strong", "Weak", "Average"]
    heroes = Hero.query.all()

    for hero in heroes:
        for _ in range(random.randint(1, 3)):
            power = random.choice(Power.query.all())
            hero_power = HeroPower(hero=hero, power=power, strength=random.choice(strengths))
            db.session.add(hero_power)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("🦸‍♀️ Seeding powers...")
        seed_powers()

        print("🦸‍♀️ Seeding heroes...")
        seed_heroes()

        print("🦸‍♀️ Adding powers to heroes...")
        add_powers_to_heroes()

        print("🦸‍♀️ Done seeding!")
