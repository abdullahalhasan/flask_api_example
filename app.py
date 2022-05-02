from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return "Hello"


@app.route('/drinks/<id>/update', methods=['POST'])
def update_drink(id):
    data = request.get_json()
    drink = Drink.query.get(id)
    if drink is None:
        return {'Error': 'Drink Not Found'}
    drink.name = data['name']
    drink.description = data['description']
    db.session.commit()
    return {'code': 202, 'message': 'Drink Updated Successfully!'}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {'Error': 'Drink Not Found'}
    db.session.delete(drink)
    db.session.commit()
    return {'code': 203, 'message': 'Drink Deleted Successfully!'}


@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.get_json()
    drink = Drink(name=data['name'], description=data['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id, 'code': 201, 'message': 'Drink Added Successfully!'}
    # return {'id': drink.id, 'code': 201, 'message': 'Drink Added Successfully!'}


@app.route('/drinks/<id>', methods=['GET'])
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return jsonify({'name': drink.name, 'description': drink.description})


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.order_by(desc(Drink.name)).all()
    #drink = db.session.query(Drink).order_by(desc(Drink.id)).all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"Drinks": output}


if __name__ == "__main__":
    app.run(debug=True)
