import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from orge.blockchain import Blockchain

def test_blockchain():
    # Initialize the blockchain
    orge_blockchain = Blockchain()

    # Add some transactions
    orge_blockchain.add_transaction("Alice", "Bob", 50)
    orge_blockchain.add_transaction("Charlie", "Dave", 30)

    # Mine a block
    print("Mining a block...")
    orge_blockchain.mine_block()

    # Add more transactions and mine another block
    orge_blockchain.add_transaction("Eve", "Frank", 100)
    print("Mining another block...")
    orge_blockchain.mine_block()

    # Print the blockchain
    for block in orge_blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Transactions: {block.transactions}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}")
        print("\n")

    # Validate the blockchain
    is_valid = orge_blockchain.is_chain_valid()
    print("Is the blockchain valid?", is_valid)

if __name__ == "__main__":
    test_blockchain()

