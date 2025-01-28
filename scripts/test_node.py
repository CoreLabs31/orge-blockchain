import requests
import json
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from threading import Lock

# Flask app setup
app = Flask(__name__)
socketio = SocketIO(app)
lock = Lock()


class Node:
    def __init__(self, port):
        self.port = port
        self.peers = set()  # To store connected nodes
        self.blockchain = None  # Reference to the blockchain instance

    def set_blockchain(self, blockchain):
        """Links the blockchain instance to this node."""
        self.blockchain = blockchain

    def add_peer(self, peer_url):
        """Adds a peer to the node's peer list."""
        if peer_url not in self.peers:
            self.peers.add(peer_url)
            print(f"Peer added: {peer_url}")
        else:
            print(f"Peer {peer_url} is already connected.")

    def broadcast_transaction(self, transaction):
        """Broadcasts a transaction to all peers."""
        with lock:
            for peer in self.peers:
                try:
                    response = requests.post(f"{peer}/add_transaction", json=transaction)
                    if response.status_code == 200:
                        print(f"Transaction broadcasted to {peer}")
                except Exception as e:
                    print(f"Error broadcasting to {peer}: {e}")

    def broadcast_block(self, block):
        """Broadcasts a mined block to all peers."""
        with lock:
            for peer in self.peers:
                try:
                    response = requests.post(f"{peer}/add_block", json=block)
                    if response.status_code == 200:
                        print(f"Block broadcasted to {peer}")
                except Exception as e:
                    print(f"Error broadcasting to {peer}: {e}")

    def sync_blockchain(self):
        """Synchronizes the blockchain by fetching the longest chain from peers."""
        longest_chain = None
        max_length = len(self.blockchain.chain)

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/get_chain")
                if response.status_code == 200:
                    peer_chain = response.json()["chain"]
                    peer_length = response.json()["length"]

                    if peer_length > max_length:
                        max_length = peer_length
                        longest_chain = peer_chain
            except Exception as e:
                print(f"Error syncing with {peer}: {e}")

        if longest_chain:
            self.blockchain.replace_chain(longest_chain)
            print("Blockchain synchronized with the longest chain.")


# Flask Routes for P2P
@app.route('/connect_node', methods=['POST'])
def connect_node():
    """Connects this node to another peer."""
    json_data = request.get_json()
    peer_url = json_data.get('peer_url')
    if not peer_url:
        return jsonify({"message": "Peer URL is required"}), 400

    node.add_peer(peer_url)
    return jsonify({"message": f"Connected to peer {peer_url}"}), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Adds a transaction received from a peer."""
    transaction_data = request.get_json()
    if not transaction_data:
        return jsonify({"message": "Invalid transaction data"}), 400

    try:
        sender = transaction_data["sender"]
        receiver = transaction_data["receiver"]
        amount = transaction_data["amount"]
        fee = transaction_data["fee"]
        node.blockchain.add_transaction(sender, receiver, amount, fee)
        return jsonify({"message": "Transaction added successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/add_block', methods=['POST'])
def add_block():
    """Adds a block received from a peer."""
    block_data = request.get_json()
    if not block_data:
        return jsonify({"message": "Invalid block data"}), 400

    try:
        new_block = Block(
            index=block_data["index"],
            transactions=block_data["transactions"],
            previous_hash=block_data["previous_hash"],
        )
        new_block.hash = block_data["hash"]
        new_block.nonce = block_data["nonce"]

        if node.blockchain.is_chain_valid() and node.blockchain.add_block(new_block):
            return jsonify({"message": "Block added successfully"}), 200
        else:
            return jsonify({"message": "Block is invalid"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """Returns the blockchain."""
    chain_data = [block.__dict__ for block in node.blockchain.chain]
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200


if __name__ == "__main__":
    # Initialize the node
    port = 5000
    node = Node(port)

    # Import the blockchain instance and link it to the node
    from orge.blockchain import Blockchain

    blockchain = Blockchain()
    node.set_blockchain(blockchain)

    # Start Flask app
    socketio.run(app, host="0.0.0.0", port=port)
