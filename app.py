from flask import Flask, Blueprint
from api import api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['RESTPLUS_VALIDATE'] = True
app.config['ERROR_404_HELP'] = False
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
# app.config['SERVER_NAME'] = 'localhost:5000'
app.url_map.strict_slashes = False

blueprint = Blueprint('api', __name__)
api.init_app(blueprint)
app.register_blueprint(blueprint)


@app.route('/ping')
def ping():
    return {'pong': 'ok'}


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
