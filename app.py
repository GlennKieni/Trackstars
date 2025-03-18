from flask import Flask
from auth_routes import auth_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

app.register_blueprint(auth_routes)

if __name__ == '__main__':
    app.run(debug=True)
