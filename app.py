from flask import Flask
from flask_cors import CORS

from config import Config

from flask_jwt_extended import JWTManager

from app.user import user_blueprint
from app.object_detection import objectDetection_blueprint
from app.object_detection_report import objectDetectionReport_blueprint

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(objectDetection_blueprint)
app.register_blueprint(objectDetectionReport_blueprint)

@app.route('/api', methods=['GET'])
def get_root():
    return 'Hello, World!', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
