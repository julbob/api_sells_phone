"""Main module to launch API to manage Database of sells and product"""

from flask import Flask, Response
from waitress import serve
from src.shops.routes.sell import blp_sells
from src.shops.routes.product import blp_products


app: Flask = Flask(__name__)


@app.route("/health", methods=["GET"])
def healthcheck() -> Response:
    """Function called by health probe"""
    return Response("App is ready", 200)


if __name__ == "__main__":
    app.register_blueprint(blp_sells, url_prefix="/sells")
    app.register_blueprint(blp_products, url_prefix="/products")
    serve(app, host="0.0.0.0", port=8080)
