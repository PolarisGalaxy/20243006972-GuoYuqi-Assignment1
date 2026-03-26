# Main.py
# Entry point for the Assignment 1 print spooler simulation.
# Creates an Assignment1 instance and starts the simulation.
# Change 5: Added startup banner and keyboard interrupt handling.

from Assignment1Task import Assignment1

if __name__ == "__main__":
    print("========================================")
    print(" Print Spooler Simulation - Assignment 1")
    print(" Student: Guo Yuqi  ID: 20243006972")
    print("========================================")

    try:
        # Create simulation object and run it
        sim = Assignment1()
        sim.startSimulation()
    except KeyboardInterrupt:
        # Allow user to stop the simulation early with Ctrl+C
        print("\n[Simulation] Interrupted by user. Exiting...")
