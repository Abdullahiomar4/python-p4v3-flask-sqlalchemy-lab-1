from models import db, Earthquake
from app import app

with app.app_context():
    # Clear old data
    Earthquake.query.delete()

    # Add seed data in the order tests expect
    eq1 = Earthquake(location="Chile", magnitude=9.5, year=1960)
    eq2 = Earthquake(location="Alaska", magnitude=9.2, year=1964)

    db.session.add_all([eq1, eq2])
    db.session.commit()

    print("Seeded database with earthquakes.")
