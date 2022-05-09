#Doubly Linked List
from copy import deepcopy


class Node:
 
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def get_next(self):
        if self.next != None:
            return self.next

        node = self

        while True:
            if node.prev == None:
                return node
            
            node = node.prev

    def get_prev(self):
        if self.prev != None:
            return self.prev

        node = self

        while True:
            if node.next == None:
                return node
            
            node = node.next


 
class DLL:
 
    def __init__(self, data=None):
        self.head = None
        self.size = 0

        if data != None:
            for d in data:
                self.append(d)

    def pop(self, node:Node):

        if node.prev != None:
            if node.next != None:
                node.prev.next = node.next
            else:
                node.prev.next = None

        if node.next != None:
            if node.prev != None:
                node.next.prev = node.prev
            else:
                node.next.prev = None

        self.size -= 1
        del node

    def get(self, find):
        
        node = self.head

        while True:
            if node == None:
                return None
            
            if node.data == find:
                return node
            
            node = node.prev

    def get_id(self, id):
        
        this_id = self.size - 1

        node = self.head

        while True:
            if node == None:
                return None

            if this_id == id:
                return node

            this_id -= 1

            if this_id < 0:
                return None

    def remove(self, find):

        node = self.get(find)
        
        if node == None:
            return 

        self.pop(node)


    def remove_id(self, id):
        node = self.get_id(id)
        
        if node == None:
            return 

        self.pop(node)

    def push(self, new_data):
 
        new_node = Node(new_data)
 
        new_node.next = self.head
 
        if self.head is not None:
            self.head.prev = new_node
 
        self.head = new_node

        self.size += 1
 
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

        self.size += 1
 

    def append(self, new_data):
 
        new_node = Node(new_data)
 
        if self.head is None:
            self.head = new_node
            self.size += 1
            return

        last = self.head
        while last.next:
            last = last.next
 
        last.next = new_node

        new_node.prev = last

        self.size += 1
 
        return
 
    def out(self):
        node = self.head

        Text = ''

        while node != None:
            Text = ' => ' + str(node.data) + Text
            node = node.next
        
        return Text
 
    def __str__(self) -> str:
        return self.out()


    def __repr__(self):
        return self.out()

    def copy(self):
        return deepcopy(self)

 

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