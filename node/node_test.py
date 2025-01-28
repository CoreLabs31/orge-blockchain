import unittest
from node.node import Node
from orge.blockchain import Blockchain

class TestNode(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.node = Node(self.blockchain, port=5000)

    def test_add_peer(self):
        self.node.peers.add("http://127.0.0.1:5001")
        self.assertIn("http://127.0.0.1:5001", self.node.peers)

    def test_get_chain(self):
        with self.node.app.test_client() as client:
            response = client.get('/chain')
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

