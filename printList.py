# printList.py
# Implements a linked-list based print queue.
# The queue holds a maximum of 5 print requests at a time.
# If a 6th request arrives, the oldest (head) is dropped (overwritten).
#
# Change 3: Added getLength() method to query current queue size.

class printList:

    class Node:
        """Inner class representing a single node in the linked list."""
        def __init__(self, doc):
            self.document = doc   # The printDoc object stored in this node
            self.next = None      # Pointer to the next node

    def __init__(self):
        """Initialise an empty linked list queue."""
        self.head = None  # Head (front) of the queue

    def queueInsert(self, doc):
        """
        Insert a new print request at the tail of the queue.
        If the queue already has 5 requests, the head is removed
        to make room (oldest request is dropped).
        """
        new_node = printList.Node(doc)

        if self.head is None:
            # Queue is empty - new node becomes the head
            self.head = new_node
            print(f"Inserted a request in the queue from {new_node.document.getSender()}")
            print("Number of requests in the queue 1")
        else:
            # Traverse to the tail and count nodes
            last = self.head
            count = 1
            while last.next is not None:
                last = last.next
                count += 1

            # Append the new node at the tail
            last.next = new_node
            count += 1
            print(f"Inserted a request in the queue from {new_node.document.getSender()}")

            # If queue exceeds 5, remove the head (oldest request)
            if count > 5:
                self.head = self.head.next
                print("!!!!!!Attention: Overwrite!!!!!!")
                count -= 1

            print(f"Number of requests in the queue {count}")

        return self

    def queuePrint(self, printerID):
        """
        Print and remove the document at the head of the queue.
        Does nothing if the queue is empty.
        """
        if self.head is not None:
            currNode = self.head
            print(":::::")
            print(f"Printer {printerID} Printing the request from Machine ID: "
                  f"{currNode.document.getSender()} {currNode.document.getStr()}")
            print(":::::")
            # Remove the printed node from the queue
            self.head = self.head.next

    def getLength(self):
        """
        Return the current number of documents in the queue.
        Useful for monitoring queue load during simulation.
        """
        count = 0
        currNode = self.head
        while currNode is not None:
            count += 1
            currNode = currNode.next
        return count

    def queuePrintAll(self):
        """
        Debug utility: print the contents of the entire queue
        without removing any nodes.
        """
        currNode = self.head
        print("LinkedList:", end=" ")
        while currNode is not None:
            print(currNode.document.getStr(), end=" ")
            currNode = currNode.next
        print()
