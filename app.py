import os
import json
import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from database import initialize_db, db
from api.schema import initialize_ma
from api.resources.routes import initialize_routes


# init app
app = Flask(__name__)
api = Api(app)

# database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)

initialize_db(app)
initialize_ma(app)
initialize_routes(api)


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


# run server
port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
