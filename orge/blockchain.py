import time
import hashlib

class Blockchain:
    def __init__(self, block_reward=50):
        self.chain = []  # List of blocks in the chain
        self.pending_transactions = []  # List of unconfirmed transactions
        self.block_reward = block_reward  # Base mining reward
        self.create_genesis_block()  # Create the first block in the chain

    def create_genesis_block(self):
        """Creates the genesis block (the first block in the blockchain)."""
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        """Returns the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount, fee=0.001):
        """Adds a new transaction to the list of pending transactions."""
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        transaction = Transaction(sender, receiver, amount, fee)
        self.pending_transactions.append(transaction)

    def mine_block(self, miner_address):
        """Creates a new block, adds pending transactions, and appends it to the blockchain."""
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        latest_block = self.get_latest_block()  # Get the latest block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash,
        )

        # Add miner reward
        miner_reward_transaction = Transaction(
            sender="Network",
            receiver=miner_address,
            amount=self.block_reward,
            fee=0,
        )
        new_block.transactions.append(miner_reward_transaction)

        # Append the new block to the chain
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear the pending transactions
        print(f"Block {new_block.index} mined and added to the blockchain!")

    def is_chain_valid(self):
        """Validates the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the hash of the block."""
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Transaction:
    def __init__(self, sender, receiver, amount, fee=0.001):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.receiver}, amount: {self.amount}, fee: {self.fee})"
