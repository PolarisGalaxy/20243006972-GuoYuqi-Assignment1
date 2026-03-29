# Assignment 1 – Print Spooler Simulation

**Student:** Guo Yuqi  
**ID:** 20243006972  

## Overview

This project simulates a **print spooler system** using Python multithreading.

- **50 machine threads** (producers) randomly send print requests to a shared queue.
- **5 printer threads** (consumers) randomly dequeue and print documents from the queue.
- The shared queue is a **linked list** capped at 5 requests. If a 6th arrives, the oldest is dropped.
- A **threading.Lock (mutex)** protects the shared queue from race conditions.

This is a classic **Producer-Consumer** concurrency problem.

## Files

| File | Description |
|------|-------------|
| `Main.py` | Entry point — creates and starts the simulation |
| `Assignment1Task.py` | Core simulation: `Assignment1`, `machineThread`, `printerThread` |
| `printList.py` | Linked-list queue (max 5 nodes) |
| `printDoc.py` | Print document data class |

## How to Run

```bash
python Main.py
```

Requires Python 3.x. No external dependencies.

## Design Notes

- `threading.Lock` is used as a mutex around all `queueInsert` and `queuePrint` calls.
- All threads are set as `daemon=True` so they exit cleanly when the simulation ends.
- Simulation runs for 30 seconds by default (`SIMULATION_TIME = 30`).

## Threading Design Notes

- 	hreading.Lock() used as mutex for all shared queue access
- daemon=True on all threads ensures clean exit when simulation ends
- join(timeout=5) prevents simulation from hanging on exit
- Queue max size is 5; oldest request is dropped if exceeded
