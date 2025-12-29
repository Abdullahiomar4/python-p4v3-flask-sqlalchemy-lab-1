from flask import Flask, jsonify
from models import db, Earthquake
import os
import sys

# Ensure the server directory is in sys.path so config can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

app = Flask(__name__)
app.config.from_object(config)

# Initialize the database
db.init_app(app)

# ✅ REQUIRED FOR TESTS
with app.app_context():
    db.create_all()

    # ------------------------------
    # Seed data for testing
    # ------------------------------
    if Earthquake.query.count() == 0:
        eq1 = Earthquake(location="Alaska", magnitude=9.2, year=1964)
        eq2 = Earthquake(location="Chile", magnitude=9.5, year=1960)
        eq3 = Earthquake(location="Sumatra", magnitude=9.1, year=2004)
        db.session.add_all([eq1, eq2, eq3])
        db.session.commit()

# ------------------------------
# Routes
# ------------------------------

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # SQLAlchemy 2.0 compatible session.get()
    with db.session() as session:
        quake = session.get(Earthquake, id)

    if quake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

    return jsonify(quake.to_dict()), 200


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # SQLAlchemy 2.0 style session query
    with db.session() as session:
        quakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()

    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
