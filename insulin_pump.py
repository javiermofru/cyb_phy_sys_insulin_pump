import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import secrets
from cryptography.hazmat.primitives import padding
import requests

class InsulinPump:
    def __init__(self):
        self.dos_vulnerability = False
        self.non_authorized_access_vulnerability = False
        self.eavesdropping_vulnerability = False
        self.data_integrity_vulnerability = False
        self.authorized_users = {'AuthorizedUser1', 'AuthorizedUser2'}
        self.user_attempting_access = ''
        self.secret_key = secrets.token_hex(16)
        self.glucose_ideal = 30
        self.glucose_level = self.glucose_ideal
        self.dose_to_administer = 0
        self.message = ''
        self.message_enc = ''
        self.message_hash = ''
        self.msg = ''

    def print_msg(self, msg):
        print(msg)
        requests.post("http://localhost:5000/update_message", json={"message": msg})
        self.msg = msg

    def dosAttack(self):
        if self.dos_vulnerability:
            self.print_msg('Denial of Service (DoS) attack initiated...')
            time.sleep(5)
            self.print_msg('Denial of Service (DoS) attack completed.')
        else:
            self.print_msg('Denial of Service (DoS) attack avoided.')

    def unauthorizedAccess(self, attacker_name):
        self.user_attempting_access = attacker_name
        if not self.non_authorized_access_vulnerability:
            self.print_msg(f'Unauthorized Access: {attacker_name} attempts to access the insulin pump without authorization.')
            self.print_msg(f'Authorized users: {self.authorized_users}')
            if attacker_name in self.authorized_users:
                self.print_msg(f'Access for {attacker_name} has been authorized.')
            else:
                self.print_msg(f'Unauthorized Access: Access for {attacker_name} has been blocked.')
        else:
            self.print_msg(f'Unauthorized Access: {attacker_name} has gain access to the insulin pump without authorization.')
            

    def interceptMessage(self, encrypted_message, attacker_name):
        self.print_msg(f'Eavesdropping: {attacker_name} attempts to intercept the encrypted message.')
        if self.eavesdropping_vulnerability or attacker_name in self.authorized_users:
            self.print_msg(f'Encrypted message intercepted by {attacker_name}: {encrypted_message}')
        else:
            self.print_msg('Eavesdropping Vulnerability not activated. Encrypting the message before sending...')
            encrypted_message_aes, _ = self.encryptMessage(encrypted_message)
            self.print_msg(f'Encrypted message with AES key: {encrypted_message_aes}')
            

    def encryptMessage(self, message):
        cipher = Cipher(algorithms.AES(self.secret_key.encode()), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        # Encrypt the message
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

        # Add integrity code
        sha_message = hashlib.sha256(message.encode()).hexdigest()
        self.message_enc = encrypted_message
        self.message_hash = sha_message

        encrypted_message_with_integrity = encrypted_message + sha_message.encode()

        return encrypted_message, encrypted_message_with_integrity

    
    def decryptMessage(self, message):
        cipher = Cipher(algorithms.AES(self.secret_key.encode()), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        # Encrypt the message
        des_encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        desc_sha_message = hashlib.sha256(message.encode()).hexdigest()


        if self.data_integrity_vulnerability:
            self.print_msg('Data Integrity Vulnerability activated. Changing the hash content.')
            desc_sha_message = hashlib.sha256(b'ModificatedHash').hexdigest()
            if self.message_hash != desc_sha_message or self.message_enc != des_encrypted_message:                             
                self.print_msg(f'Hash Decrypted message {desc_sha_message} is different to {self.message_hash}')
        else: 
            self.print_msg('Data Integrity Vulnerability is not activated.')
            if self.message_hash == desc_sha_message and self.message_enc == des_encrypted_message:
                self.message_enc == des_encrypted_message
                self.message_hash == desc_sha_message
                self.print_msg('Data Integrity: Data has been verified successfully.')
                self.print_msg(f'Encrypted hash message {self.message_hash} is the same as the hash decrypted message {desc_sha_message}')

        return message


    def measureGlucose(self, level):
        self.print_msg(f"Glucose has been measured: {level}")
        self.glucose_level = level

    def administerInsulin(self):
        # Adjust the amount of insulin based on the glucose level
        glucose_difference = self.glucose_level - self.glucose_ideal

        if glucose_difference > 0:
            # Glucose level is higher than the ideal, so more insulin is needed
            self.dose_to_administer = glucose_difference / 10  # Adjust as needed
            self.message = f"{self.dose_to_administer} units of insulin will be administered to reduce glucose."
            self.print_msg(self.message)
            self.encryptMessage(self.message)
        elif glucose_difference < 0:
            # Glucose level is lower than the ideal, so less insulin is needed
            self.dose_to_administer = abs(glucose_difference) / 10  # Adjust as needed
            self.message = f"{self.dose_to_administer} units of insulin will be administered to increase glucose."
            self.print_msg(self.message)
            self.encryptMessage(self.message)
        else:
            self.print_msg("Glucose level is in the ideal range. Insulin administration is not needed.")

        

    # Method to update parameters from the frontend
    def updateParameters(self, glucose_ideal):
        self.glucose_ideal = glucose_ideal
