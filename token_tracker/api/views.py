from rest_framework.decorators import api_view
from rest_framework.response import Response
from web3 import Web3
from .models import HistoricalData
import os
import json

with open('path/to/token_abi.json', 'r') as abi_file:
    token_abi = json.load(abi_file)
# Configure Web3
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

@api_view(['GET'])
def token_balance(request):
    try:
        address = request.GET.get('address')
        token = request.GET.get('token')
        contract = web3.eth.contract(address=token, abi=token_abi)
        balance = contract.functions.balanceOf(address).call()
        return Response({'balance': Web3.fromWei(balance, 'ether')})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def historical_data(request):
    try:
        token = request.GET.get('token')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        data = HistoricalData.objects.filter(token=token, date__range=[start_date, end_date])
        return Response([{'date': entry.date, 'balance': entry.balance} for entry in data])
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def transfer_token(request):
    try:
        recipient = request.data['recipient']
        amount = Web3.toWei(request.data['amount'], 'ether')
        private_key = os.getenv('PRIVATE_KEY')  # Ensure you have the private key securely stored
        sender_address = web3.eth.account.privateKeyToAccount(private_key).address

        contract = web3.eth.contract(address=request.data['token'], abi=token_abi)
        nonce = web3.eth.getTransactionCount(sender_address)
        txn = contract.functions.transfer(recipient, amount).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = web3.eth.account.signTransaction(txn, private_key=private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return Response({'status': 'success', 'tx_hash': web3.toHex(tx_hash)})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def token_allowance(request):
    try:
        address = request.GET.get('address')
        token = request.GET.get('token')
        contract = web3.eth.contract(address=token, abi=token_abi)
        allowance = contract.functions.allowance(address, contract.address).call()
        return Response({'allowance': Web3.fromWei(allowance, 'ether')})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def approve_token(request):
    try:
        spender = request.data['spender']
        amount = Web3.toWei(request.data['amount'], 'ether')
        private_key = os.getenv('PRIVATE_KEY')  # Ensure you have the private key securely stored
        sender_address = web3.eth.account.privateKeyToAccount(private_key).address

        contract = web3.eth.contract(address=request.data['token'], abi=token_abi)
        nonce = web3.eth.getTransactionCount(sender_address)
        txn = contract.functions.approve(spender, amount).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = web3.eth.account.signTransaction(txn, private_key=private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return Response({'status': 'success', 'tx_hash': web3.toHex(tx_hash)})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

