# printDoc.py
# Represents a single print document/request.
# Stores the document content and the ID of the machine that sent it.

class printDoc:
    def __init__(self, s, senderID):
        """Initialise the document with a string and sender machine ID."""
        self.str = s
        self.senderID = senderID

    def setStr(self, s, senderID):
        """Update the document content and sender ID."""
        self.str = s
        self.senderID = senderID

    def getStr(self):
        """Return the document content string."""
        return self.str

    def getSender(self):
        """Return the ID of the machine that sent this document."""
        return self.senderID
