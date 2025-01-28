from node.node import Node
from orge.blockchain import Blockchain

def main():
    # Initialize the blockchain
    blockchain = Blockchain()

    # Start a node on port 5000
    node = Node(blockchain, port=5000)
    print("Starting node on port 5000...")
    node.start()

if __name__ == "__main__":
    main()
