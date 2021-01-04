from flask_marshmallow import Marshmallow

ma = Marshmallow()


def initialize_ma(app):
    ma.init_app(app)
