from eospy.cleos import Cleos
from eospy.keys import EOSKey
import json

class EosEvmNftTrader:
    def __init__(self, private_key, node_url='https://eosmarket.io'):
        self.private_key = private_key
        self.public_key = EOSKey(private_key).to_public()
        self.node_url = node_url
        self.ce = Cleos(url=self.node_url)
        self.EVM_CONTRACT_NAME = 'eosioevmcontract'

    def _create_transaction(self, action_name, data, actor):
        return {
            "actions": [{
                "account": self.EVM_CONTRACT_NAME,
                "name": action_name,
                "authorization": [{
                    "actor": actor,
                    "permission": "active",
                }],
                "data": data
            }]
        }

    def check_ownership(self, token_id):
        # Hypothetically, we send a "check" action to the contract, which then should return the owner.
        data = {
            "token_id": token_id
        }
        trx = self._create_transaction('check', data, self.public_key)
        
        # Note: In reality, you may not execute the transaction just to check state; you might use a different method.
        result = self.ce.push_transaction(trx)
        
        # Parsing the hypothetical result
        if 'owner' in result:
            return result['owner']
        else:
            raise Exception("Failed to check ownership")

    def trade_nft(self, token_id, to_account):
        owner = self.check_ownership(token_id)
        if owner != self.public_key:
            raise Exception(f"Current user does not own the token. Owner: {owner}")

        data = {
            "from": owner,
            "to": to_account,
            "token_id": token_id
        }
        
        trx = self._create_transaction('trade', data, owner)

        # Signing and pushing the transaction
        signed_trx = self.ce.sign_transaction(trx, [self.private_key], chain_id=self.ce.get_chain_info()['chain_id'])
        result = self.ce.push_transaction(signed_trx)
        return result

if __name__ == "__main__":
    trader = EosEvmNftTrader(private_key='your_private_key_here')

    # Check ownership
    try:
        owner = trader.check_ownership(123)
        print(f"Token is owned by: {owner}")
    except Exception as e:
        print(f"Error: {e}")

    # Trade NFT
    try:
        result = trader.trade_nft(123, 'bobaccount')
        print(result)
    except Exception as e:
        print(f"Error: {e}")
