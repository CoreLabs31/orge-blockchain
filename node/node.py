import json
import requests
from flask import Flask, request

class Node:
    """Represents a peer-to-peer node in the network."""

    def __init__(self, blockchain, port):
        self.blockchain = blockchain
        self.port = port
        self.peers = set()  # Set of connected peer nodes
        self.app = Flask(__name__)

        # Define Flask routes
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes for handling P2P requests."""
        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            return json.dumps([block.__dict__ for block in self.blockchain.chain]), 200

        @self.app.route('/add_peer', methods=['POST'])
        def add_peer():
            data = request.get_json()
            peer = data.get("peer")
            if peer:
                self.peers.add(peer)
                return {"message": f"Peer {peer} added."}, 201
            return {"error": "Invalid peer data."}, 400

        @self.app.route('/add_block', methods=['POST'])
        def add_block():
            data = request.get_json()
            block_data = data.get("block")
            if block_data:
                block = self.blockchain.add_block_from_data(block_data)
                if block:
                    return {"message": "Block added to the chain."}, 201
                return {"error": "Invalid block."}, 400
            return {"error": "No block data provided."}, 400

    def start(self):
        """Start the Flask server."""
        self.app.run(host='0.0.0.0', port=self.port)

