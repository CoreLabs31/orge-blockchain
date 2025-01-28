import hashlib
import time


class Transaction:
    def __init__(self, sender, receiver, amount, fee=0.001):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee  # Transaction fee

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.receiver}, amount: {self.amount}, fee: {self.fee})"


class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions  # List of transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()
        self.miner_reward = self.calculate_miner_reward()

    def calculate_hash(self):
        transactions_str = "".join(str(tx) for tx in self.transactions)
        block_string = f"{self.index}{transactions_str}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def calculate_miner_reward(self):
        """
        Calculate the total fees in this block.
        This will be the reward for the miner, in addition to any block reward.
        """
        total_fees = sum(tx.fee for tx in self.transactions)
        return total_fees


class Blockchain:
    class Blockchain:
    def __init__(self, block_reward=50):
        self.chain = []
        self.pending_transactions = []  # List of unconfirmed transactions
        self.block_reward = block_reward  # Base reward for mining a block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount, fee=0.001):
        """
        Add a new transaction to the list of pending transactions.
        :param sender: Address of the sender
        :param receiver: Address of the receiver
        :param amount: Amount being transferred
        :param fee: Transaction fee
        """
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        transaction = Transaction(sender, receiver, amount, fee)
        self.pending_transactions.append(transaction)


    def mine_block(self, miner_address):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        latest_block = self.get_latest_block()

        # Create a new block with the pending transactions
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash
        )

        # Add the miner's reward to the block reward
        miner_reward_transaction = Transaction(
            sender="Network",
            receiver=miner_address,
            amount=self.block_reward + new_block.miner_reward,  # Block reward + total fees
            fee=0  # No fee for the reward transaction
        )
        new_block.transactions.append(miner_reward_transaction)

        # Add the block to the chain
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear the pending transactions
        print(f"Block {new_block.index} has been mined! Reward: {miner_reward_transaction.amount} ORGE")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
