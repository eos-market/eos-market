from eospy.cleos import Cleos
from eospy.types import EOSEncoder
import json

# Function to deposit an NFT
def deposit_nft(contract, from_account, to_account, nft_id, private_key):
    ce = Cleos(url='https://api.eosnewyork.io')

    # Define the payload
    data = {
        "from": from_account,
        "to": to_account,
        "nft_id": nft_id,
    }

    # Define the transaction
    payload = {
        'account': contract,
        'name': 'transfer',  
        'data': data,
        'authorization': [{
            'actor': from_account,
            'permission': 'active',
        }],
    }

    # Encode the transaction
    encoded = ce.abi_json_to_bin(payload['account'], payload['name'], payload['data'])
    payload['data'] = encoded['binargs']
    trx = {"actions": [payload]}

    # Sign the transaction
    resp = ce.push_transaction(trx, private_key, broadcast=True)
    return resp

# Example usage
if __name__ == "__main__":
    contract = 'nftcontractacc'  
    from_account = 'useraccount'  
    to_account = 'recipientacc'   
    nft_id = 12345                
    private_key = 'your_private_key'  

    try:
        response = deposit_nft(contract, from_account, to_account, nft_id, private_key)
        print("Transaction response:", response)
    except Exception as e:
        print("An error occurred:", e)
