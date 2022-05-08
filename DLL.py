#Doubly Linked List

class Node:
 
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
 
class DLL:
 
    def __init__(self, data=None):
        self.head = None

        if data != None:
            for d in data:
                self.append(d)

    def push(self, new_data):
 
        new_node = Node(new_data)
 
        new_node.next = self.head
 
        if self.head is not None:
            self.head.prev = new_node
 
        self.head = new_node
 
    def insertAfter(self, prev_node, new_data):
 
        if prev_node is None:
            print("the given previous node cannot be NULL")
            return
 
        new_node = Node(new_data)

        new_node.next = prev_node.next

        prev_node.next = new_node
 
        new_node.prev = prev_node
 
        if new_node.next:
            new_node.next.prev = new_node
 

    def append(self, new_data):
 
        new_node = Node(new_data)
 
        if self.head is None:
            self.head = new_node
            return

        last = self.head
        while last.next:
            last = last.next
 
        last.next = new_node

        new_node.prev = last
 
        return
 

    def printList(self, node = None):

        if node == None:
            self.printList(self.head)
            return
 
        print("\nTraversal in forward direction")
        while node:
            print(" {}".format(node.data))
            last = node
            node = node.next
 
        print("\nTraversal in reverse direction")
        while last:
            print(" {}".format(last.data))
            last = last.prev
 
    def __str__(self) -> str:
        self.printList()
        return ''
 

# llist = DLL()
 
# # Insert 6. So the list becomes 6->None
# llist.append(6)
 
# # Insert 7 at the beginning.
# # So linked list becomes 7->6->None
# llist.push(7)
 
# # Insert 1 at the beginning.
# # So linked list becomes 1->7->6->None
# llist.push(1)
 
# # Insert 4 at the end.
# # So linked list becomes 1->7->6->4->None
# llist.append(4)
 
# # Insert 8, after 7.
# # So linked list becomes 1->7->8->6->4->None
# llist.insertAfter(llist.head.next, 8)
 
# print ("Created DLL is: ")
# llist.printList(llist.head)