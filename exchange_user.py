from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eosmarket.io'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    wallet_balance = db.Column(db.Float, default=0.0)
    nfts = db.relationship('NFT', backref='owner', lazy=True)

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_listed = db.Column(db.Boolean, default=False)
    current_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    user = User.query.get(data['owner_id'])
    if user:
        nft = NFT(title=data['title'], owner=user)
        db.session.add(nft)
        db.session.commit()
        return jsonify({"message": "NFT created successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/list-nft', methods=['POST'])
def list_nft():
    data = request.json
    nft = NFT.query.get(data['nft_id'])
    if nft and nft.owner_id == data['owner_id']:
        nft.is_listed = True
        db.session.commit()
        return jsonify({"message": "NFT listed for sale"})
    else:
        return jsonify({"message": "NFT not found or not owned by the user"}), 404

@app.route('/buy-nft', methods=['POST'])
def buy_nft():
    data = request.json
    buyer = User.query.get(data['buyer_id'])
    nft = NFT.query.get(data['nft_id'])

    if not nft or not nft.is_listed:
        return jsonify({"message": "NFT not available for purchase"}), 404

    if buyer.wallet_balance < nft.price:
        return jsonify({"message": "Insufficient funds to buy the NFT"}), 400

    seller = nft.owner
    seller.wallet_balance += nft.price
    buyer.wallet_balance -= nft.price
    nft.owner = buyer
    nft.is_listed = False
    db.session.commit()
    return jsonify({"message": "NFT purchased successfully"})

if __name__ == '__main__':
    app.run(debug=True)