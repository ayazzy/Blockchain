"""

A Primitive Blockchain implementation to learn about the ins-and-outs of
the underlying technology of crytpassets and the blockchain technology.
Written by: Ayaz Vural
Date: Monday December 6th 2021

"""
import hashlib
import json
from time import time


class Blockchain(object):
    # Defining the variables.
    """
    hashlib: for encryption
    JSON: to format our blocks
    time: for each block's timestamp
    """

    def __init__(self):
        # empty list we will add blocks to. Literally our "blockchain"
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout of banks.", proof=100)

    """
    block variable describing JSON object with the properties:
    index:take the length of our blockchain and add 1 to it. Will be used to reference an individual block
    timestamp: stamp the block when it is created
    transactions: any transactions that are sitting in the "pending list" will be included in the new block
    proof: this comes from our miner who thinks they found a valid "nonce" or "proof"
    previous hash: a hashed version of the most recent approved block
    
    Every block will contain these properties
    """

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # empty the pending list of transactions as we added them to our new block on line 42
        self.pending_transactions = []
        # add our new block to self.chain
        self.chain.append(block)

        return block

    """
    last_block(): call our chain and receive the block that was added most recently
    On line 67 we add our transaction JSON object to our pool of pending_transactions.
    These will sit in limbo until a new block is mined and added to our blockchain.
    
    For reference, let's return the index of the block which our new transaction's going to be added to
    """

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    """
     Bitcoin and many other blockchains use SHA-256, an encryption hash function, which takes in some string
     (stored as a Unicode value) and spits out a 64-character long encrypted string. In a blockchain,
     the text that we encrypt is actually our block.
     
     Blockchains are considered "tamper-proof" because every single block contains a copy of the previous block's hash.
     Since your new hash is derived from the previous block, you can't change any aspect of a block without 
     changing every single hash in front of it.
     
    """

    def hash(self, block):
        # takes new block and changes its key/value pairs all into strings
        string_object = json.dumps(block, sort_keys=True)
        # turns that string into Unicode
        block_string = string_object.encode()

        # pass the Unicode string into SHA-256 method and create a hexadecimal string from its return value.
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        # return our new hash
        return hex_hash


if __name__ == '__main__':
    blockchain = Blockchain()
    t1 = blockchain.new_transaction("Satoshi", "Ayaz", '11 BTC')
    t2 = blockchain.new_transaction("Ayaz", "Pars", '6 BTC')
    t3 = blockchain.new_transaction("Satoshi", "Cem", '120 BTC')
    t4 = blockchain.new_transaction("Cem", "Kerem", '15 BTC')
    t5 = blockchain.new_transaction("Kerem", "Ayda", '1 BTC')
    blockchain.new_block(12345)

    t6 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
    t7 = blockchain.new_transaction("Alice", "Bob", '0.1 BTC')
    t8 = blockchain.new_transaction("Bob", "Mike", '0.8 BTC')
    blockchain.new_block(6789)

print("Blockchain", blockchain.chain)
