"""Class providing support for storing and reading Ethereum
contracts. It is univeral in meaning there are no hardcoded
field names and it can store securely any serializable
Python dictionary."""

import hashlib
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from solc import compile_source
from web3.middleware import geth_poa_middleware
from ..settings import INFURA_URL, KEYFILE, PASSWORD, CHAIN_ID, ACCOUNT


class Contract:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(INFURA_URL))
        self.account = self.w3.toChecksumAddress(ACCOUNT)
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.content = ''

    def source(self):
        return '''
        pragma solidity ^0.4.18;
        contract Fingerprint {
          function Fingerprint() {
            value = '%s';
          }

          function get() public constant returns (string) {
            return value;
          }

          string value;
        }
        '''
    
    def hash(self):
        for key in self.content:
            self.content[key] = hashlib.sha224(
              str(self.content[key]).encode('utf-8')
            ).hexdigest()

    def compile(self):
        # Return compiled source code with content injected
        content = json.dumps(self.content)
        source = self.source()
        contract = source % content
        return compile_source(contract)

    def contractInterface(self):
        # Instantiate contract
        compiled_sol = self.compile()
        return compiled_sol['<stdin>:Fingerprint']

 
    def read(self, transaction):
        # Contract instance in concise mode
        tx_receipt = self.w3.eth.getTransactionReceipt(transaction)
        if tx_receipt:
            contract_interface = self.contractInterface()
            contract_instance = self.w3.eth.contract(
              address=tx_receipt.contractAddress,
              abi = contract_interface['abi'],
              ContractFactoryClass=ConciseContract
            )
            content = contract_instance.get()
            return json.loads(content)

    def deploy(self):
        nonce = self.w3.eth.getTransactionCount(self.account, "pending")
        self.w3 = Web3()
        contract_interface = self.contractInterface()
        # Deploy contract and get transaction hash
        contract = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        with open(KEYFILE) as keyfile:
          data = contract._encode_constructor_data()
          encrypted_key = keyfile.read()
          self.w3.eth.enable_unaudited_features()
          private_key = self.w3.eth.account.decrypt(encrypted_key, PASSWORD)
          transaction = {
            'data': data,
            'gas': 1000000,
            'chainId': CHAIN_ID,
            'gasPrice': self.w3.toWei('40', 'gwei'),
            'value': 0,
            'nonce': nonce,
            'to': '',
          }
          signed = self.w3.eth.account.signTransaction(transaction, private_key=private_key)
          self.w3 = Web3(HTTPProvider(INFURA_URL))
          tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
          return self.w3.toHex(tx_hash)
