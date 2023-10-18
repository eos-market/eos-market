from cryptography.fernet import Fernet
import os

class EOSVault:
    def __init__(self, key_file='key.key', vault_file='vault.vlt'):
        self.key_file = key_file
        self.vault_file = vault_file
        
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)

        with open(self.key_file, 'rb') as f:
            self.key = f.read()
            self.cipher = Fernet(self.key)

    def store_private_key(self, private_key):
        encrypted_data = self.cipher.encrypt(private_key.encode())
        with open(self.vault_file, 'wb') as f:
            f.write(encrypted_data)

    def retrieve_private_key(self):
        with open(self.vault_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()

vault = EOSVault()

# Storing EOS private key
private_key = "test_private_key"
vault.store_private_key(private_key)

# Retrieving EOS private key
retrieved_key = vault.retrieve_private_key()
print(retrieved_key)

