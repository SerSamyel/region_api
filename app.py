from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import Config
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config.from_object(Config)

# for console test
client = app.test_client()

engine = create_engine('sqlite:///db.sqlite', connect_args={'check_same_thread': False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session.configure()
session = Session()
Base = declarative_base()
jwt = JWTManager(app)

from models import *
Base.metadata.create_all(bind=engine)


@app.route('/region', methods=['GET'])
def get_region():
    regions = session.query(Region)
    serialised = []
    for region in regions:
        serialised.append({
            'id': region.id,
            'name': region.name
        })
    return jsonify(serialised)


@app.route('/region', methods=['POST'])
@jwt_required
def add_region():
    new_one = Region(**request.json)
    session.add(new_one)
    session.commit()
    serialised = ({
        'id': new_one.id,
        'name': new_one.name,
        'relation_id': new_one.relation_id}
    )
    return jsonify(serialised)


@app.route('/region/<int:region_id>', methods=['PUT'])
@jwt_required
def update_region(region_id):
    item = session.query(Region).filter(Region.id == region_id).first()
    params = request.json
    if not item:
        return {'message': 'No region with this id.'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'name': item.name,
        'relation_id': item.relation_id}
    return serialised


@app.route('/region/<int:region_id>', methods=['DELETE'])
@jwt_required
def delete_region(region_id):
    item = session.query(Region).filter(Region.id == region_id).first()
    if not item:
        return {'message': 'No region with this id.'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/town/<int:region_id>', methods=['GET'])
def town(region_id):
    towns = session.query(Town).filter(Town.region_id == region_id)
    serialised = []
    for town in towns:
        serialised.append({
            'id': town.id,
            'town_name': town.town_name
        })
    return jsonify(serialised)


@app.route('/town', methods=['POST'])
@jwt_required
def add_town():
    new_one = Town(**request.json)
    session.add(new_one)
    session.commit()
    serialised = ({
        'id': new_one.id,
        'town_name': new_one.town_name,
        'region_id': new_one.region_id}
    )
    return jsonify(serialised)


@app.route('/town/<int:town_id>', methods=['PUT'])
@jwt_required
def update_town(town_id):
    item = session.query(Town).filter(Town.id == town_id).first()
    params = request.json
    if not item:
        return {'message': 'No town with this id.'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'town_name': item.town_name,
        'region_id': item.region_id}
    return serialised


@app.route('/town/<int:town_id>', methods=['DELETE'])
@jwt_required
def delete_town(town_id):
    item = session.query(Town).filter(Town.id == town_id).first()
    if not item:
        return {'message': 'No region with this id.'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


if __name__ == '__main__':
    app.run()