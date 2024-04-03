#!/usr/bin/python3
"""
'Contains a Flask web application API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
'''The Flask web application instance.'''
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app_host = getenv("HBNB_API_HOST", default='0.0.0.0')
app_port = int(getenv("HBNB_API_PORT", default=5000))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    The Flask app/request context end event listener.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

if __name__ == "__main__":
    app.run(app_host, app_port, threaded=True)
