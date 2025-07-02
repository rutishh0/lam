import os
import base64
import json
import logging
from typing import Dict, Any, Union, Optional
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import hashlib
import secrets

logger = logging.getLogger(__name__)

class DataEncryption:
    """Handles encryption and decryption of sensitive data"""
    
    def __init__(self, master_key: str = None):
        """Initialize encryption with master key"""
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = os.environ.get('ENCRYPTION_MASTER_KEY', '').encode()
            if not self.master_key:
                # Generate a new key if none provided
                self.master_key = Fernet.generate_key()
                print(f"Generated new master key: {self.master_key.decode()}")
                print("Please save this key securely in your environment variables!")
        
        self.cipher_suite = self._initialize_cipher()
    
    def _initialize_cipher(self) -> Fernet:
        """Initialize Fernet cipher with derived key"""
        # Use PBKDF2 to derive a key from the master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'stable_salt_for_app',  # In production, use a proper salt management
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        return Fernet(key)
    
    def encrypt_data(self, data: Union[str, Dict]) -> str:
        """Encrypt data and return base64 encoded string"""
        if isinstance(data, dict):
            data = json.dumps(data)
        
        encrypted = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Union[str, Dict]:
        """Decrypt base64 encoded data"""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher_suite.decrypt(decoded).decode()
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted)
            except json.JSONDecodeError:
                return decrypted
                
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def hash_email(self, email: str) -> str:
        """Create a consistent hash of email for lookups"""
        return hashlib.sha256(email.lower().encode()).hexdigest()
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a secure random password"""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def encrypt_client_data(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in client data"""
        sensitive_fields = [
            'full_name', 'email', 'phone', 'date_of_birth', 
            'address', 'personal_statement', 'documents'
        ]
        
        encrypted_data = client_data.copy()
        
        # Store original email hash for lookups
        if 'email' in client_data:
            encrypted_data['email_hash'] = self.hash_email(client_data['email'])
        
        # Encrypt sensitive fields
        sensitive_data = {}
        for field in sensitive_fields:
            if field in client_data:
                sensitive_data[field] = client_data[field]
                encrypted_data.pop(field, None)
        
        encrypted_data['encrypted_personal_data'] = self.encrypt_data(sensitive_data)
        
        return encrypted_data
    
    def decrypt_client_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt client data"""
        decrypted_data = encrypted_data.copy()
        
        if 'encrypted_personal_data' in encrypted_data:
            personal_data = self.decrypt_data(encrypted_data['encrypted_personal_data'])
            decrypted_data.update(personal_data)
            decrypted_data.pop('encrypted_personal_data', None)
        
        return decrypted_data


class SecureCredentialStorage:
    """Secure storage for application credentials"""
    
    def __init__(self, encryption: DataEncryption):
        self.encryption = encryption
        self.credentials_file = "credentials.enc"
    
    def store_credentials(self, client_id: str, university: str, credentials: Dict[str, str]) -> bool:
        """Store encrypted credentials"""
        try:
            # Load existing credentials
            all_credentials = self._load_all_credentials()
            
            # Create key for this credential set
            key = f"{client_id}_{university}"
            
            # Add timestamp
            credentials['created_at'] = datetime.utcnow().isoformat()
            
            # Store encrypted
            all_credentials[key] = self.encryption.encrypt_data(credentials)
            
            # Save back to file
            self._save_all_credentials(all_credentials)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to store credentials: {str(e)}")
            return False
    
    def retrieve_credentials(self, client_id: str, university: str) -> Optional[Dict[str, str]]:
        """Retrieve decrypted credentials"""
        try:
            all_credentials = self._load_all_credentials()
            key = f"{client_id}_{university}"
            
            if key in all_credentials:
                return self.encryption.decrypt_data(all_credentials[key])
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve credentials: {str(e)}")
            return None
    
    def _load_all_credentials(self) -> Dict[str, str]:
        """Load all encrypted credentials from file"""
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_all_credentials(self, credentials: Dict[str, str]):
        """Save encrypted credentials to file"""
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f)


# Utility functions
def generate_encryption_key() -> str:
    """Generate a new encryption key"""
    return Fernet.generate_key().decode()


def setup_encryption_environment():
    """Setup encryption environment variables"""
    key = generate_encryption_key()
    print(f"Add this to your .env file:")
    print(f"ENCRYPTION_MASTER_KEY={key}")
    return key 