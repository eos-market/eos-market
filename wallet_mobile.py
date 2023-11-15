from eospy.cleos import Cleos

def main():
    # Connect to EOS node
    ce = Cleos(url='https://api.eosnewyork.io')

    def get_account_info(account_name):
        return ce.get_account(account_name)

    def get_blockchain_info():
        return ce.get_info()

    # Usage
    account_name = 'market'  
    print(get_account_info(account_name))
    print(get_blockchain_info())

if __name__ == "__main__":
    main()
