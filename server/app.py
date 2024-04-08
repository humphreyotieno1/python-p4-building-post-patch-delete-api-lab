#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)

    if not bakery:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(bakery.to_dict()), 200)
    
    if request.method == 'PATCH':
        data = request.form

        if 'name' in data:
            bakery.name = data['name']

        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 200)


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form

    baked_good = BakedGood(
        name=data['name'],
        price=int(data['price']),
        bakery_id=int(data['bakery_id'])
    )

    db.session.add(baked_good)
    db.session.commit()

    return make_response(jsonify(baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)

    if not baked_good:
        abort(404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response(jsonify({'message': 'Baked good deleted successfully.'}), 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(jsonify(baked_goods_by_price_serialized), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response(jsonify(most_expensive_serialized), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
