class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
        self.activeNode = self.head
        self.size = len(nodes)

    def findNode(self, data):
        for node in self:
            if node.data == data:
                return(node)

    def nextCircular(self):
        if self.activeNode.next == None:
            self.activeNode = self.head
        else:
            self.activeNode = self.activeNode.next
        return(self.activeNode)


    def __repr__(self):
        startingNode = self.activeNode
        node = startingNode
        nodes = []
        for i in range(self.size+1):
            if i == 0:
                nodes.append("("+str(node.data)+")")
            else:
                nodes.append(str(node.data))
            node = self.nextCircular()
        nodes.append("None")
        self.activeNode = startingNode
        return " -> ".join(nodes)


    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next




class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
            return str(self.data)


if __name__ == '__main__':
    cups_test = [3,8,9,1,2,5,4,6,7]
    cups = LinkedList(cups_test)
    print(cups)



    hop = cups.findNode(9)
    cups.activeNode = hop
    print(f"Youpi {cups}")
    for i in range(15):
        cups.nextCircular()
        print(cups)
    cups.activeNode = hop
    print(f"Youpi {cups}")
