import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from orge.blockchain import Blockchain

def test_blockchain():
    # Initialize the blockchain
    orge_blockchain = Blockchain()

    # Add some blocks with sample data
    orge_blockchain.add_block("First block data")
    orge_blockchain.add_block("Second block data")
    orge_blockchain.add_block("Third block data")

    # Print the blockchain details
    for block in orge_blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Data: {block.data}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}")
        print("\n")

    # Validate the blockchain
    is_valid = orge_blockchain.is_chain_valid()
    print("Is the blockchain valid?", is_valid)

if __name__ == "__main__":
    test_blockchain()
