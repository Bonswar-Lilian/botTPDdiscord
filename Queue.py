class Queue:
    # Linked list implementation of a queue.
    class QueueNode:
        def __init__(self,value):
            # Nodes store a value and a reference to the next node
            self.value = value
            self.next = None

    def __init__(self):
        #Queues all have a head and a tail (references to the first and last objects in the list)
        self.head = None
        self.tail = None

    def __str__(self):
        # Solely used for debugging.Used to print queues
        node = self.head
        res = "["
        
        while(node != None):
            res += str(node.value) + ","
            node = node.next
        return res[0:-1] + "]"

    def enqueue(self,value):
        # To enqueue just change the tail next element to be the new node and then change the tail to be a reference to the new node
        # O(1) cost
        newNode = self.QueueNode(value)

        if self.tail == None:
            # If no elements in the queue then we set the head and the tail to reference the new element
            self.head = newNode
            self.tail = newNode
            return
        else:
            # If not just add a new element next to the tail of the list and make that element the tail
            self.tail.next = newNode
            self.tail = newNode

    def dequeue(self):
        # To dequeue just make the second element the new head. Python's garbage collector will automatically deallocate the memory
        # O(1) cost
        if self.head == None:
            return None
            # Throw error??
        res = self.head.value
        
        if self.head == self.tail:
            # If there was only one element in the queue
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        # return the value of the head before the deletion
        return res
    
    def isEmpty(self):
        return self.head == None

    def length(self):
        # O(n) complexity
        i=0
        current = self.head

        while current != None:
            current= current.next
            i+=1
        return i