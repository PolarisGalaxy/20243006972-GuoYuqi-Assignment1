# Assignment1Task.py
# Main simulation file for Assignment 1.
#
# This program simulates a print spooler system using Python threads.
# - 50 'machine' threads act as clients that send print requests.
# - 5  'printer' threads act as servers that dequeue and print documents.
# - A shared linked-list queue (printList) holds up to 5 pending requests.
# - A threading.Lock (mutex) ensures only one thread accesses the queue at a time,
#   preventing race conditions (data corruption from concurrent access).
#
# Producer-Consumer pattern:
#   Machines (producers) --> shared queue --> Printers (consumers)
#
# Change 2: Added request counters to track total prints and requests sent.

import threading
import time
import random

from printDoc import printDoc
from printList import printList


class Assignment1:
    # ----------------------------------------------------------------
    # Simulation configuration constants
    # ----------------------------------------------------------------
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum random sleep for printers (seconds)
    MAX_MACHINE_SLEEP = 5    # Maximum random sleep for machines (seconds)

    # ----------------------------------------------------------------
    # Initialise simulation state
    # ----------------------------------------------------------------
    def __init__(self):
        self.sim_active = True             # Flag: threads run while True
        self.print_list = printList()      # Shared print request queue
        self.mThreads = []                 # List of machine threads
        self.pThreads = []                 # List of printer threads
        # Mutex lock: prevents simultaneous queue access by multiple threads
        self.lock = threading.Lock()
        # Counters to track simulation statistics (protected by lock)
        self.total_requests_sent = 0
        self.total_requests_printed = 0

    # ----------------------------------------------------------------
    # Start and manage the simulation
    # ----------------------------------------------------------------
    def startSimulation(self):
        # Create NUM_MACHINES machine threads, each with a unique ID
        for i in range(self.NUM_MACHINES):
            machine = self.machineThread(i, self)
            self.mThreads.append(machine)

        # Create NUM_PRINTERS printer threads, each with a unique ID
        for j in range(self.NUM_PRINTERS):
            printer = self.printerThread(j, self)
            self.pThreads.append(printer)

        # Start all machine and printer threads
        for t in self.mThreads + self.pThreads:
            t.start()

        print(f"[Simulation] Started: {self.NUM_MACHINES} machines, "
              f"{self.NUM_PRINTERS} printers, running for {self.SIMULATION_TIME}s")

        # Let the simulation run for SIMULATION_TIME seconds
        time.sleep(self.SIMULATION_TIME)

        # Signal all threads to stop their loops
        self.sim_active = False
        print("[Simulation] Time elapsed. Waiting for threads to finish...")

        # Join printer threads - wait for each to finish its current job
        for printer in self.pThreads:
            printer.join()

        # Join machine threads - wait for each to exit cleanly
        for machine in self.mThreads:
            machine.join()

        # Print final simulation statistics
        print("[Simulation] All threads finished. Simulation complete.")
        print(f"[Statistics] Total requests sent:    {self.total_requests_sent}")
        print(f"[Statistics] Total requests printed: {self.total_requests_printed}")

    # ================================================================
    # Inner class: printerThread
    # A printer repeatedly sleeps (simulating printing time), then
    # dequeues and prints the next document from the shared queue.
    # ================================================================
    class printerThread(threading.Thread):

        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer    # Reference to outer Assignment1 instance
            self.daemon = True    # Exit automatically when main thread ends

        def run(self):
            """Thread entry point: loop until simulation ends."""
            while self.outer.sim_active:
                # Simulate the time taken to print a document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                self.printDox(self.printerID)

        def printerSleep(self):
            """Sleep for a random duration between 1 and MAX_PRINTER_SLEEP seconds."""
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            """
            Acquire the mutex lock, then dequeue and print one document.
            The lock ensures no two printers print the same document.
            Increments the total_requests_printed counter.
            """
            print(f"Printer ID: {printerID} : now available")
            # Critical section: only one thread may access the queue at a time
            with self.outer.lock:
                # Check if there is something to print before counting
                if self.outer.print_list.head is not None:
                    self.outer.print_list.queuePrint(printerID)
                    self.outer.total_requests_printed += 1
                else:
                    self.outer.print_list.queuePrint(printerID)

    # ================================================================
    # Inner class: machineThread
    # A machine repeatedly sleeps (simulating work), then sends a
    # print request by inserting a document into the shared queue.
    # ================================================================
    class machineThread(threading.Thread):

        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer    # Reference to outer Assignment1 instance
            self.daemon = True    # Exit automatically when main thread ends

        def run(self):
            """Thread entry point: loop until simulation ends."""
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time before requesting
                self.machineSleep()
                # Machine wakes up and sends a print request to the queue
                self.printRequest(self.machineID)

        def machineSleep(self):
            """Sleep for a random duration between 1 and MAX_MACHINE_SLEEP seconds."""
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            """
            Build a printDoc and insert it into the shared queue.
            The lock ensures no two machines corrupt the queue simultaneously.
            Increments the total_requests_sent counter.
            """
            print(f"Machine {id} Sent a print request")
            # Create a document with the machine's message and ID
            doc = printDoc(f"My name is machine {id}", id)
            # Critical section: only one thread may access the queue at a time
            with self.outer.lock:
                self.outer.print_list.queueInsert(doc)
                self.outer.total_requests_sent += 1
