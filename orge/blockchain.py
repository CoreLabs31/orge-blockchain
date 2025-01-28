import hashlib
import time


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.receiver}, amount: {self.amount})"


class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions  # List of transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = "".join(str(tx) for tx in self.transactions)
        block_string = f"{self.index}{transactions_str}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []  # List of unconfirmed transactions
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)

    def mine_block(self):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear pending transactions after mining
        print(f"Block {new_block.index} has been mined!")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
