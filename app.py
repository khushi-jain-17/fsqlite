from flask import Flask

from route import get_routes

app = Flask(__name__)

app.register_blueprint(get_routes)


if __name__ == '__main__':
    app.run(debug=True)
