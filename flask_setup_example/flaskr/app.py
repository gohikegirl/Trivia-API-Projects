from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
import os
from flask_cors import CORS


def create_app(test_config = None):
    app = Flask(__name__) #instance_relative_config=True)
    setup_db(app)
    CORS(app) #, resources{r'*/api/*: {origins:*'}})
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    # )
    # if test_config is None:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response. headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/plants', methods=['GET'])
    #@cross_origin()<--option to make this route specifically cross-original allowed
    # def hello():
    #     return jsonify({'message': 'HELLO WORLD' })
    def get_plants():
        #enable pagination of results, looking first to see if client has passed an argument
        #for certain pages and if not, then defaulting to 1
        page = request.args.get('page', 1, type = int)
        start = (page-1)*10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
        'success': True,
        'plants': formatted_plants[start:end],
        'total_plants': len(formatted_plants) #let's requester know that there are more plants not shown
        })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
        if plant == None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404
    return app
