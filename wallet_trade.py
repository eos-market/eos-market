import json
from eospy.cleos import Cleos
from eospy.types import EOSEncoder, Transaction
from eospy.keys import EOSKey
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class EOSNFTTrader:
    def __init__(self, url, contract, private_key):
        self.ce = Cleos(url)
        self.contract = contract
        self.private_key = private_key

    def get_account(self, account_name):
        try:
            return self.ce.get_account(account_name)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None
        except Exception as e:
            logging.error(f"Error fetching account: {e}")
            return None

    def trade_nft(self, from_account, to_account, nft_id, quantity):
        data = {
            "from": from_account,
            "to": to_account,
            "nft_id": nft_id,
            "quantity": quantity
        }

        payload = {
            'account': self.contract,
            'name': 'tradenft',  
            'data': data,
            'authorization': [{
                'actor': from_account,
                'permission': 'active',
            }],
        }

        try:
            # Create transaction
            trx = Transaction(actions=[payload])
            # Sign transaction
            signed_trx = trx.sign(self.private_key, self.ce.get_chain_id())
            # Push transaction
            response = self.ce.push_transaction(signed_trx)
            return response
        except Exception as e:
            logging.error(f"Error in NFT trade: {e}")
            return None

if __name__ == "__main__":
    trader = EOSNFTTrader(
        url='https://api.eosnewyork.io',
        contract='nftcontractacc',  
        private_key='your_private_key'  
    )

    from_account = 'useraccount'  
    to_account = 'recipientacc'  
    nft_id = 123  
    quantity = 1  

    response = trader.trade_nft(from_account, to_account, nft_id, quantity)
    if response:
        logging.info(f"Trade successful: {response}")
    else:
        logging.info("Trade failed")
