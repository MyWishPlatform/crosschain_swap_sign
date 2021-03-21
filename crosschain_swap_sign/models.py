from django.db import models
from encrypted_fields import fields


class BlockchainAccount(models.Model):
    class NetworkType(models.TextChoices):
        ETHEREUM_LIKE = 'ethereum like'
        BINANCE_CHAIN = 'binance chain'

    address = models.CharField(max_length=100, primary_key=True)
    secret = fields.EncryptedTextField()  # private key for Ethereum-like, mnemonic for Binance Chain
    network_type = models.CharField(max_length=50, choices=NetworkType.choices)


class ClientSecret(models.Model):
    key_id = models.CharField(max_length=100, primary_key=True)
    key = fields.EncryptedTextField()
