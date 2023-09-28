from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eosmarket.io'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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

@app.route('/create-nft', methods=['POST'])
def create_nft():
    data = request.json
    nft = NFT(title=data['title'], owner_id=data['owner_id'])
    db.session.add(nft)
    db.session.commit()
    return jsonify({"message": "NFT created successfully"})

@app.route('/list-nfts', methods=['GET'])
def list_nfts():
    nfts = NFT.query.all()
    nft_list = [{"title": nft.title, "owner_id": nft.owner_id} for nft in nfts]
    return jsonify({"nfts": nft_list})

if __name__ == '__main__':
    app.run(debug=True)
