from web3 import Web3

# Connect to EOS EVM (assuming it's running on localhost:8545 or adjust as necessary)
w3 = Web3(Web3.HTTPProvider('http://eosmarket.io'))

# Ensure connection
if not w3.isConnected():
    raise ValueError("Failed to connect to EOS EVM")

def get_balance(address):
    """Retrieve the balance of a given address."""
    balance = w3.eth.getBalance(address)
    return w3.fromWei(balance, 'ether')

def send_tokens(sender_private_key, recipient_address, amount_in_eos):
    """Send EOS tokens from one address to another."""
    
    # Calculate nonce for sender
    sender_address = w3.eth.account.privateKeyToAccount(sender_private_key).address
    nonce = w3.eth.getTransactionCount(sender_address)
    
    # Create a transaction
    txn = {
        'nonce': nonce,
        'to': recipient_address,
        'value': w3.toWei(amount_in_eos, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }

    # Sign and send the transaction
    signed_txn = w3.eth.account.signTransaction(txn, sender_private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    return txn_hash.hex()

# Test
address = "0xYourAddressHere"
print(f"Balance of address {address}: {get_balance(address)} EOS")

# Sending tokens (Replace with actual private key and recipient address)
# txn_hash = send_tokens("YOUR_PRIVATE_KEY", "RECIPIENT_ADDRESS", 1.0)
# print(f"Transaction hash: {txn_hash}")

