# Edge MSD Core

A modular simulator for two-stage microservice deployment in edge inference systems.

The project models task DAGs, heterogeneous edge nodes, network transmission, core-service placement, and online lightweight-service scheduling. Scenarios are supplied through Python objects, keeping the methods independent of a particular experimental dataset.

## Components

| Module | Purpose |
|---|---|
| `models.py` | Services, task DAGs, nodes, users, requests, instances, and decisions |
| `network.py` | Wireless access, multi-hop transfer delay, and DAG data readiness |
| `capacity.py` | Gamma effective capacity and delay approximations |
| `placement.py` | Resource-constrained core-service placement |
| `controller.py` | Online deployment, routing, and parallelism control |
| `simulation.py` | Slotted simulation and state transitions |
| `config.py` | Algorithm and simulation settings |

Supported controllers are `proposed`, `propavg`, `lbrr`, and `ga`.

## Installation

Python 3.11 or later is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Quick start

Run the synthetic example and test suite:

```bash
python -m examples.minimal
python -m pytest -q
```

To run a custom scenario:

```python
from edge_msd.config import Settings
from edge_msd.simulation import Simulator

settings = Settings(
    duration_ms=1000,
    ec_admission_window_ms=1.0,
    wireless=False,
)

simulator = Simulator(scenario, settings, method="proposed")
diagnostics = simulator.run()
```

Construct `scenario` with the `Service`, `TaskType`, `Node`, `User`, and `Scenario` classes in `edge_msd.models`. See [`examples/minimal.py`](examples/minimal.py) for a complete example.

## Modeling notes

- Time is measured in milliseconds, data in decimal MB, wired bandwidth in Gbps, and wireless bandwidth in Hz.
- Resource vectors follow `(CPU, GPU, RAM, VRAM)`.
- `ec_admission_window_ms` explicitly defines the load proxy used by the effective-capacity controller.
- `Node.light_reserve` can reserve resources for online lightweight-service deployment.
- Effective-capacity delay is a scheduling approximation; it is not an end-to-end probabilistic guarantee for a finite DAG.

Detailed definitions and assumptions are documented in [`docs/MODEL_AND_METHOD.md`](docs/MODEL_AND_METHOD.md).
