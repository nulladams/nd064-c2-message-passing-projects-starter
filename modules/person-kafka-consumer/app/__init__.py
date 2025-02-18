# from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# import person_pb2
# import person_pb2_grpc


def create_app(env=None):
    from config import config_by_name
    #from app.routes import register_routes

    #app = Flask(__name__)
    #app.config.from_object(config_by_name[env or "test"])
    #api = Api(app, title="UdaConnect API", version="0.1.0")

    print(config_by_name[env or "test"])

    #CORS(app)  # Set CORS for development

    #register_routes(api, app)
    #db.init_app(app)

    # @app.route("/health")
    # def health():
    #     return jsonify("healthy")

    app = config_by_name

    return app
