import hashlib
import time
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, transactions, nonce=0, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calcule le hash SHA-256 du bloc."""
        block_data = (
            str(self.index) +
            str(self.timestamp) +
            str(self.transactions) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}..., previous_hash={self.previous_hash[:10]}..., transactions={len(self.transactions)})"

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        """Crée le premier bloc (genesis) de la blockchain."""
        return Block(0, "0", ["Genesis Block"], timestamp=1630500000)

    def add_transaction(self, transaction):
        """Ajoute une transaction à la liste en attente."""
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        """Mine un nouveau bloc avec les transactions en attente."""
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            previous_hash=last_block.hash,
            transactions=self.pending_transactions
        )
        self.mine_block(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []  # Réinitialise les transactions

    def mine_block(self, block):
        """Effectue la Proof of Work (PoW) pour miner un bloc."""
        print(f"Mining block {block.index}...")
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined! Hash: {block.hash}")

    def is_chain_valid(self):
        """Vérifie si la blockchain est valide."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Vérifie la liaison entre blocs
            if current_block.previous_hash != previous_block.hash:
                return False

            # Vérifie le hash du bloc actuel
            if current_block.hash != current_block.calculate_hash():
                return False

            # Vérifie la Proof of Work
            if not current_block.hash.startswith('0' * self.difficulty):
                return False

        return True

    def __repr__(self):
        return f"Blockchain(len={len(self.chain)}, difficulty={self.difficulty})"
