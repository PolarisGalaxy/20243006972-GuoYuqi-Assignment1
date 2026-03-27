# printDoc.py
# Represents a single print document/request.
# Stores the document content, the ID of the machine that sent it,
# and a timestamp recording when the request was created.
# Change 5: Added timestamp to track when each print request was created.

import time

class printDoc:
    def __init__(self, s, senderID):
        """Initialise the document with content, sender ID, and creation timestamp."""
        self.str = s
        self.senderID = senderID
        # Record the time this print request was created
        self.timestamp = time.strftime("%H:%M:%S", time.localtime())

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

    def getTimestamp(self):
        """Return the time this print request was created."""
        return self.timestamp
