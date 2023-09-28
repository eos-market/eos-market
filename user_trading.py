from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eosmarket.io'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    wallet_balance = db.Column(db.Float, default=10000.0)
    nfts = db.relationship('NFT', backref='owner', lazy=True)
    bids = db.relationship('Bid', backref='user', lazy=True)

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_listed = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0.0)
    bids = db.relationship('Bid', backref='nft', lazy=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nft_id = db.Column(db.Integer, db.ForeignKey('nft.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

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
        nft = NFT(title=data['title'], owner=user, price=data['price'])
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

@app.route('/place-bid', methods=['POST'])
def place_bid():
    data = request.json
    user = User.query.get(data['user_id'])
    nft = NFT.query.get(data['nft_id'])

    if not nft or not nft.is_listed:
        return jsonify({"message": "NFT not available for bidding"}), 404

    if user.wallet_balance < data['bid_amount']:
        return jsonify({"message": "Insufficient funds to place a bid"}), 400

    existing_bid = Bid.query.filter_by(user_id=data['user_id'], nft_id=data['nft_id']).first()
    if existing_bid:
        if data['bid_amount'] > existing_bid.amount:
            existing_bid.amount = data['bid_amount']
        else:
            return jsonify({"message": "Bid amount must be higher than the current highest bid"}), 400
    else:
        bid = Bid(user_id=data['user_id'], nft_id=data['nft_id'], amount=data['bid_amount'])
        db.session.add(bid)

    db.session.commit()
    return jsonify({"message": "Bid placed successfully"})

@app.route('/accept-bid', methods=['POST'])
def accept_bid():
    data = request.json
    nft = NFT.query.get(data['nft_id'])

    if not nft or not nft.is_listed:
        return jsonify({"message": "NFT not available for sale"}), 404

    highest_bid = Bid.query.filter_by(nft_id=data['nft_id']).order_by(Bid.amount.desc()).first()

    if not highest_bid:
        return jsonify({"message": "No bids found for this NFT"}), 400

    buyer = User.query.get(highest_bid.user_id)

    if nft.price <= highest_bid.amount <= buyer.wallet_balance:
        seller = nft.owner
        seller.wallet_balance += highest_bid.amount
        buyer.wallet_balance -= highest_bid.amount
        nft.owner = buyer
        nft.is_listed = False
        db.session.delete(highest_bid)
        db.session.commit()
        return jsonify({"message": "Bid accepted, NFT sold successfully"})
    else:
        return jsonify({"message": "Bid cannot be accepted"}), 400

@app.route('/cancel-listing', methods=['POST'])
def cancel_listing():
    data = request.json
    nft = NFT.query.get(data['nft_id'])

    if not nft or not nft.is_listed:
        return jsonify({"message": "NFT not available for sale"}), 404

    if nft.owner_id == data['owner_id']:
        nft.is_listed = False
        db.session.commit()
        return jsonify({"message": "NFT listing canceled"})
    else:
        return jsonify({"message": "NFT not found or not owned by the user"}), 404

@app.route('/get-bids', methods=['GET'])
def get_bids():
    data = request.json
    nft = NFT.query.get(data['nft_id'])

    if not nft or not nft.is_listed:
        return jsonify({"message": "NFT not available for sale"}), 404

    bids = Bid.query.filter_by(nft_id=data['nft_id']).order_by