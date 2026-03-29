# Assignment1Task.py
# Main simulation file for Assignment 1.
#
# Producer-Consumer pattern:
#   Machines (producers) --> shared queue --> Printers (consumers)

import threading
import time
import random

from printDoc import printDoc
from printList import printList


class Assignment1:
    NUM_MACHINES = 50
    NUM_PRINTERS = 5
    SIMULATION_TIME = 30
    MAX_PRINTER_SLEEP = 3
    MAX_MACHINE_SLEEP = 5

    def __init__(self):
        self.sim_active = True
        self.print_list = printList()
        self.mThreads = []
        self.pThreads = []
        self.lock = threading.Lock()
        self.total_requests_sent = 0
        self.total_requests_printed = 0

    def startSimulation(self):
        for i in range(self.NUM_MACHINES):
            machine = self.machineThread(i, self)
            self.mThreads.append(machine)

        for j in range(self.NUM_PRINTERS):
            printer = self.printerThread(j, self)
            self.pThreads.append(printer)

        for t in self.mThreads + self.pThreads:
            t.start()

        print(f"[Simulation] Started: {self.NUM_MACHINES} machines, "
              f"{self.NUM_PRINTERS} printers, running for {self.SIMULATION_TIME}s")

        time.sleep(self.SIMULATION_TIME)

        self.sim_active = False
        print("[Simulation] Time elapsed. Waiting for threads to finish...")

        # timeout=5 prevents hanging forever if a thread gets stuck
        for printer in self.pThreads:
            printer.join(timeout=5)

        for machine in self.mThreads:
            machine.join(timeout=5)

        print("[Simulation] All threads finished. Simulation complete.")
        print(f"[Statistics] Total requests sent:    {self.total_requests_sent}")
        print(f"[Statistics] Total requests printed: {self.total_requests_printed}")

    class printerThread(threading.Thread):

        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer
            self.daemon = True

        def run(self):
            while self.outer.sim_active:
                self.printerSleep()
                self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            with self.outer.lock:
                if self.outer.print_list.head is not None:
                    self.outer.print_list.queuePrint(printerID)
                    self.outer.total_requests_printed += 1
                else:
                    print(f"Printer ID: {printerID} : queue is empty, standing by...")

    class machineThread(threading.Thread):

        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer
            self.daemon = True

        def run(self):
            while self.outer.sim_active:
                self.machineSleep()
                self.printRequest(self.machineID)

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            doc = printDoc(f"My name is machine {id}", id)
            with self.outer.lock:
                self.outer.print_list.queueInsert(doc)
                self.outer.total_requests_sent += 1
