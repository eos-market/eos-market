from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nft_display.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    wallet_balance = db.Column(db.Float, default=10000.0)
    nfts = db.relationship('NFT', backref='owner', lazy=True)

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, default=0.0)

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

@app.route('/list-nfts', methods=['GET'])
def list_nfts():
    nfts = NFT.query.all()
    nft_list = [{
        "id": nft.id,
        "title": nft.title,
        "description": nft.description,
        "owner": nft.owner.username,
        "price": nft.price,
    } for nft in nfts]
    return jsonify({"nfts": nft_list})

@app.route('/view-nft/<int:nft_id>', methods=['GET'])
def view_nft(nft_id):
    nft = NFT.query.get(nft_id)
    if nft:
        nft_info = {
            "title": nft.title,
            "description": nft.description,
            "owner": nft.owner.username,
            "price": nft.price,
        }
        return jsonify(nft_info)
    else:
        return jsonify({"message": "NFT not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
