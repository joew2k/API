
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config = None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #set up CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS' )
        return response

    @app.route('/plants', methods= ['GET', 'POST'])
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formated_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants': formated_plants[start:end],
            'total plants': len(formated_plants)
        })
    
    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message':'This page does not exist'}), 404

    @app.errorhandler(500)
    def special_exception_handler(error):
        return 'Database connection failed', 500


    return app