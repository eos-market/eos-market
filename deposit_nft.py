import json
from eospy.cleos import Cleos
from eospy.types import EOSEncoder, Transaction
from eospy.keys import EOSKey
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class EOSNFTDeposit:
    def __init__(self, eos_url, evm_url, eos_contract, evm_contract, private_key):
        self.eos_ce = Cleos(url=eos_url)
        self.evm_url = evm_url
        self.eos_contract = eos_contract
        self.evm_contract = evm_contract
        self.private_key = private_key

    def deposit_nft(self, eos_account, nft_id):
        eos_data = {
            "from": eos_account,
            "to": self.evm_contract,  
            "quantity": "1.0000 EOS",  
            "memo": f"Deposit NFT {nft_id}"
        }

        eos_payload = {
            'account': 'eosio.token',  
            'name': 'transfer',
            'data': eos_data,
            'authorization': [{
                'actor': eos_account,
                'permission': 'active',
            }],
        }

        try:
            eos_trx = Transaction(actions=[eos_payload])
            signed_eos_trx = eos_trx.sign(self.private_key, self.eos_ce.get_chain_id())
            eos_response = self.eos_ce.push_transaction(signed_eos_trx)

            return eos_response  
        except Exception as e:
            logging.error(f"Error in NFT deposit: {e}")
            return None

# Example usage
if __name__ == "__main__":
    nft_depositor = EOSNFTDeposit(
        eos_url='https://api.eosnewyork.io',
        evm_url='your_evm_node_url',  
        eos_contract='eosnftcontract',  
        evm_contract='evmnftcontract',  
        private_key='your_private_key'  
    )

    eos_account = 'your_eos_account'  
    nft_id = 'nft_id_to_deposit'  

    response = nft_depositor.deposit_nft(eos_account, nft_id)
    if response:
        logging.info(f"Deposit successful: {response}")
    else:
        logging.info("Deposit failed")
