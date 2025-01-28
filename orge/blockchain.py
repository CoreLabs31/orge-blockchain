import hashlib
import time


class Transaction:
    """Represents a single transaction in the blockchain."""

    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction(sender='{self.sender}', receiver='{self.receiver}', amount={self.amount})"


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.index)
            + str(self.timestamp)
            + str(self.transactions)
            + self.previous_hash
            + str(self.nonce)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    """Represents the blockchain."""

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2  # Setting the difficulty attribute
        self.mining_reward = 50  # Reward for mining a block
        self.balances = {}  # Tracks wallet balances

    def create_genesis_block(self):
        """Creates the genesis block (first block of the blockchain)."""
        return Block(0, [], "0")

    def get_latest_block(self):
        """Returns the latest block in the chain."""
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        """Adds a new transaction to the list of pending transactions."""
        if sender != "Network" and self.balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance for transaction.")
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        """Mines a new block with all pending transactions and rewards the miner."""
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        # Create a new block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash,
        )
        new_block.mine_block(self.difficulty)

        # Add the new block to the chain
        self.chain.append(new_block)

        # Reward the miner
        self.add_transaction("Network", miner_address, self.mining_reward)

        # Update balances
        self.update_balances(new_block)

        # Clear pending transactions
        self.pending_transactions = []

        print(f"Block {new_block.index} mined successfully! Hash: {new_block.hash}")

    def update_balances(self, block):
        """Updates wallet balances based on the transactions in the block."""
        for transaction in block.transactions:
            if transaction.sender != "Network":
                self.balances[transaction.sender] = self.balances.get(transaction.sender, 0) - transaction.amount
            self.balances[transaction.receiver] = self.balances.get(transaction.receiver, 0) + transaction.amount

    def is_chain_valid(self):
        """Validates the entire blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the block is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the block points to the correct previous hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
