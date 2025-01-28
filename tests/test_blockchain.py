if __name__ == "__main__":
    # Initialize the blockchain
    orge_blockchain = Blockchain()

    # Add some blocks
    orge_blockchain.add_block("First block data")
    orge_blockchain.add_block("Second block data")

    # Print the blockchain
    for block in orge_blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Data: {block.data}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}")
        print("\n")

    # Verify blockchain validity
    print("Is blockchain valid?", orge_blockchain.is_chain_valid())
