# server/app.py
#!/usr/bin/env python3


from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# View to get earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    '''Has a resource available at "/earthquakes/<id>".'''
    earthquake = Earthquake.query.get(id)

    if earthquake is None:
        # Return error message if no earthquake is found
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

    # Return earthquake details in JSON format
    return jsonify({
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    }), 200


# View to get earthquakes matching a minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    '''Fetches earthquakes with a magnitude greater than or equal to the provided value.'''
    
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare a list of earthquake details
    quakes_list = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]

    # Return count of results and the earthquake data
    return jsonify({
        'count': len(quakes_list),
        'quakes': quakes_list
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)