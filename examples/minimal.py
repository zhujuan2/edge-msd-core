"""Synthetic API example, not paper data. Runs without creating output files."""

from edge_msd.config import Settings
from edge_msd.models import Node, Scenario, Service, TaskType, User
from edge_msd.simulation import Simulator


def make_scenario(rate_per_second=0.0):
    services = {
        "prepare": Service(
            "prepare",
            "light",
            (1, 0, 1, 0),
            0.1,
            1,
            0.1,
            0.1,
            work_mb=1,
            gamma_shape=2,
            gamma_scale=2,
        ),
        "infer": Service("infer", "core", (2, 0, 2, 0), 0.1, 2, 0.2, 0, processing_ms=2),
    }
    task = TaskType("pipeline", {"prepare": [], "infer": ["prepare"]}, 30, 0.1)
    nodes = {
        name: Node(name, (6, 0, 6, 0), light_reserve=(2, 0, 2, 0)) for name in ("edge", "server")
    }
    users = [User("user", (0, 0), "edge", {"pipeline": rate_per_second}, 2, 1)]
    return Scenario(services, {task.name: task}, nodes, [("edge", "server", 1, 0)], users)


def main():
    # Declares r(y)=y*work/1 ms as a stationary scheduling proxy. It is not a
    # measured arrival rate and does not turn epsilon into an end-to-end bound.
    settings = Settings(duration_ms=50, ec_admission_window_ms=1, record_trace=True)
    simulator = Simulator(make_scenario(), settings)
    simulator.add_request("user", "pipeline", arrival_ms=0, uplink_ms=0)
    result = simulator.run()
    assert result["overall"]["completed"] == 1
    print("Synthetic pipeline completed; model and method interfaces are connected.")


if __name__ == "__main__":
    main()
