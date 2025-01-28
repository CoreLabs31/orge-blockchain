from node.node import Node

if __name__ == "__main__":
    port = int(input("Enter the port number for this node: "))
    node = Node(port)
    node.run()
