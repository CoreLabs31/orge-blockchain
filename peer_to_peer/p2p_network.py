import json
import threading
import time
from flask import Flask, request
from flask_socketio import SocketIO, emit
from orge.blockchain import Blockchain

# Initialize Flask and Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Global blockchain instance
blockchain = Blockchain()
peers = set()  # To store connected peer nodes


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    """
    API to receive a new transaction from a client or another node.
    """
    transaction_data = request.get_json()
    try:
        blockchain.add_transaction(
            sender=transaction_data['sender'],
            receiver=transaction_data['receiver'],
            amount=transaction_data['amount'],
            fee=transaction_data['fee']
        )
        broadcast_transaction(transaction_data)
        return "Transaction added and broadcasted successfully.", 201
    except ValueError as e:
        return str(e), 400


@app.route('/mine_block', methods=['POST'])
def mine_block():
    """
    API to mine a new block and broadcast it to all peers.
    """
    miner_address = request.get_json().get('miner_address')
    new_block = blockchain.mine_block(miner_address)
    if new_block:
        broadcast_block(new_block)
        return f"Block {new_block.index} mined successfully.", 201
    return "Mining failed. No transactions to mine.", 400


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    API to get the blockchain data.
    """
    chain_data = [block.__dict__ for block in blockchain.chain]
    return json.dumps(chain_data), 200


@app.route('/connect_node', methods=['POST'])
def connect_node():
    """
    API to connect with a new peer node.
    """
    node_address = request.get_json().get('node_address')
    if node_address:
        peers.add(node_address)
        return f"Node {node_address} connected successfully.", 201
    return "Invalid node address.", 400


@app.route('/get_peers', methods=['GET'])
def get_peers():
    """
    API to get the list of peer nodes.
    """
    return json.dumps(list(peers)), 200


def broadcast_transaction(transaction_data):
    """
    Broadcast a transaction to all connected peers.
    """
    for peer in peers:
        try:
            socketio.emit('transaction', transaction_data, namespace=f'/{peer}')
        except Exception as e:
            print(f"Error broadcasting to {peer}: {e}")


def broadcast_block(block):
    """
    Broadcast a new block to all connected peers.
    """
    block_data = block.__dict__
    for peer in peers:
        try:
            socketio.emit('block', block_data, namespace=f'/{peer}')
        except Exception as e:
            print(f"Error broadcasting to {peer}: {e}")


@socketio.on('transaction')
def receive_transaction(transaction_data):
    """
    Handle a transaction broadcast by another node.
    """
    try:
        blockchain.add_transaction(
            sender=transaction_data['sender'],
            receiver=transaction_data['receiver'],
            amount=transaction_data['amount'],
            fee=transaction_data['fee']
        )
        print("Transaction added from peer.")
    except ValueError as e:
        print(f"Transaction validation failed: {e}")


@socketio.on('block')
def receive_block(block_data):
    """
    Handle a block broadcast by another node.
    """
    new_block = Block(
        index=block_data['index'],
        transactions=[Transaction(**tx) for tx in block_data['transactions']],
        previous_hash=block_data['previous_hash']
    )
    new_block.hash = block_data['hash']
    new_block.timestamp = block_data['timestamp']
    new_block.nonce = block_data['nonce']

    added = blockchain.add_block(new_block)
    if not added:
        print("Invalid block received. Rejected.")


def start_node():
    """
    Start the P2P node server.
    """
    socketio.run(app, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    # Run the node in a separate thread
    threading.Thread(target=start_node).start()
    print("Node is running and ready to accept connections.")

