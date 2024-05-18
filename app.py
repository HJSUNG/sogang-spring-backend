from flask import Flask
from flask_cors import CORS

from app.user import user_blueprint
from app.object_detection import objectDetection_blueprint

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
# cors = CORS(app, resources={r"/user/*": {"origins": "*"}})

app.register_blueprint(user_blueprint)
app.register_blueprint(objectDetection_blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
