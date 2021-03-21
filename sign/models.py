from django.db import models
from encrypted_fields import fields
from hdwallet import BIP44HDWallet
from hdwallet.symbols import ETH


class NetworkType(models.TextChoices):
    ETHEREUM_LIKE = 'ethereum like'
    BINANCE_CHAIN = 'binance chain'


class BlockchainAccount(models.Model):
    network_type = models.CharField(max_length=50, choices=NetworkType.choices)
    address = models.CharField(max_length=100, primary_key=True)
    mnemonic = fields.EncryptedTextField(default='')
    _private_key = fields.EncryptedTextField(default='')

    @property
    def private_key(self):
        if self.mnemonic and self.network_type == NetworkType.ETHEREUM_LIKE:
            hd_wallet = BIP44HDWallet(symbol=ETH, account=0, change=False, address=0)
            hd_wallet.from_mnemonic(mnemonic=self.mnemonic)
            return hd_wallet.private_key()
        else:
            return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value


class ClientSecret(models.Model):
    key_id = models.CharField(max_length=100, primary_key=True)
    key = fields.EncryptedTextField()
