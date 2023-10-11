from web3 import Web3

# Initialize Web3. Assuming EOS EVM is running locally on 8545
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Ensure you're connected
assert w3.isConnected()

# Contract ABI and address (after deploying)
ABI = '...'  # Contract ABI (Application Binary Interface)
CONTRACT_ADDRESS = '...'  # Your deployed contract address

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def trade_nft(token_id, sender_private_key, recipient_address):
    nonce = w3.eth.getTransactionCount(w3.eth.account.privateKeyToAccount(sender_private_key).address)
    
    txn = contract.functions.trade(token_id, recipient_address).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    })
    
    signed_txn = w3.eth.account.signTransaction(txn, sender_private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    return txn_hash

ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    # ... other functions and events ...
]

CONTRACT_ADDRESS = '0x1234567890aBCdef1265654890AbCDEf12345678'
