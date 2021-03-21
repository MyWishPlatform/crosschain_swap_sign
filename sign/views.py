from web3 import Web3
from django.http import JsonResponse
from requests_http_signature import HTTPSignatureAuth
from rest_framework.decorators import api_view
from sign.models import BlockchainAccount, ClientSecret
from rest_framework.exceptions import PermissionDenied


def key_resolver(key_id, algorithm):  # used for HTTPSignatureAuth.verify(), do not change arg names!
    secret = ClientSecret.objects.get(key_id=key_id)
    return secret.key.encode('utf-8')


@api_view(http_method_names=['POST'])
def sign_view(request):
    try:
        HTTPSignatureAuth.verify(request, key_resolver=key_resolver)
    except (AssertionError, ClientSecret.DoesNotExist):
        raise PermissionDenied

    tx_params = request.data

    try:
        account = BlockchainAccount.objects.get(address=tx_params.pop('from'))
    except BlockchainAccount.DoesNotExist:
        raise PermissionDenied

    if account.network_type == BlockchainAccount.NetworkType.ETHEREUM_LIKE:
        signed_tx = Web3().eth.account.sign_transaction(tx_params, account.private_key)
        raw_hex_tx = signed_tx.rawTransaction.hex()
        return JsonResponse({'signed_tx': raw_hex_tx})
    elif account.network_type == BlockchainAccount.NetworkType.BINANCE_CHAIN:
        raise PermissionDenied
