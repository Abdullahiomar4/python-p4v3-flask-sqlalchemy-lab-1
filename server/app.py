
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake
import os, sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# Initialize app
app = Flask(__name__)
app.config.from_object(config)

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)  # For flask db commands

# ------------------------------
# Create tables & seed data
# ------------------------------
with app.app_context():
    db.create_all()
    
    # Seed if empty
    if Earthquake.query.count() == 0:
        eq1 = Earthquake(magnitude=9.5, location="Chile", year=1960)
        eq2 = Earthquake(magnitude=9.2, location="Alaska", year=1964)
        eq3 = Earthquake(magnitude=8.6, location="Alaska", year=1946)
        eq4 = Earthquake(magnitude=8.5, location="Banda Sea", year=1934)
        eq5 = Earthquake(magnitude=8.4, location="Chile", year=1922)
        db.session.add_all([eq1, eq2, eq3, eq4, eq5])
        db.session.commit()

# ------------------------------
# Routes
# ------------------------------
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    return jsonify(quake.to_dict()), 200

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
