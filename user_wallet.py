from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eosmarket.io'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0.0)

db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"username": user.username, "balance": user.balance})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        amount = float(data['amount'])
        if amount > 0:
            user.balance += amount
            db.session.commit()
            return jsonify({"message": "Deposit successful"})
        else:
            return jsonify({"message": "Invalid deposit amount"}), 400
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        amount = float(data['amount'])
        if amount > 0 and user.balance >= amount:
            user.balance -= amount
            db.session.commit()
            return jsonify({"message": "Withdrawal successful"})
        else:
            return jsonify({"message": "Invalid withdrawal amount or insufficient balance"}), 400
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
