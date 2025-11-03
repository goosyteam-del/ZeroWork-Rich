"""
Wallet Manager Module
Handles MetaMask seed phrase import and wallet initialization
"""

from eth_account import Account
from mnemonic import Mnemonic
from typing import Optional
from src.logger_config import setup_logger

# Enable mnemonic features
Account.enable_unaudited_hdwallet_features()

logger = setup_logger("WalletManager")


class WalletManager:
    """
    Manages wallet creation and access from seed phrase
    """
    
    def __init__(self, seed_phrase: str):
        """
        Initialize wallet manager with seed phrase
        
        Args:
            seed_phrase: 12-word MetaMask seed phrase
        """
        self.seed_phrase = seed_phrase.strip()
        self.account: Optional[Account] = None
        self.address: Optional[str] = None
        
    def validate_seed_phrase(self) -> bool:
        """
        Validate the seed phrase format
        
        Returns:
            True if valid, False otherwise
        """
        try:
            words = self.seed_phrase.split()
            if len(words) != 12:
                logger.error(f"Invalid seed phrase: Expected 12 words, got {len(words)}")
                return False
            
            # Validate with mnemonic library
            mnemo = Mnemonic("english")
            if not mnemo.check(self.seed_phrase):
                logger.error("Invalid seed phrase: Failed mnemonic validation")
                return False
            
            logger.info("✓ Seed phrase validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Error validating seed phrase: {str(e)}")
            return False
    
    def initialize_wallet(self) -> bool:
        """
        Initialize wallet from seed phrase
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.validate_seed_phrase():
                return False
            
            # Derive account from seed phrase (using first derivation path)
            self.account = Account.from_mnemonic(self.seed_phrase)
            self.address = self.account.address
            
            logger.info(f"✓ Wallet initialized successfully")
            logger.info(f"  Address: {self.address}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize wallet: {str(e)}")
            return False
    
    def get_address(self) -> Optional[str]:
        """
        Get wallet address
        
        Returns:
            Wallet address or None if not initialized
        """
        return self.address
    
    def get_account(self) -> Optional[Account]:
        """
        Get account object for signing transactions
        
        Returns:
            Account object or None if not initialized
        """
        return self.account
    
    @staticmethod
    def generate_new_wallet() -> dict:
        """
        Generate a new wallet with seed phrase (for testing purposes)
        
        Returns:
            Dictionary with seed phrase and address
        """
        try:
            # Generate new mnemonic
            mnemo = Mnemonic("english")
            seed_phrase = mnemo.generate(strength=128)  # 12 words
            
            # Create account
            account = Account.from_mnemonic(seed_phrase)
            
            logger.info("✓ New wallet generated")
            logger.warning("⚠ IMPORTANT: Save this seed phrase securely!")
            
            return {
                "seed_phrase": seed_phrase,
                "address": account.address,
                "private_key": account.key.hex()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate new wallet: {str(e)}")
            return {}
