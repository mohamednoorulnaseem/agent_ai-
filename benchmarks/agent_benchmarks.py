"""
Performance Benchmarks for AI Agent Framework

This module provides benchmarking utilities to measure the performance
of agent operations including planning, execution, and API operations.

Usage:
    python -m benchmarks.agent_benchmarks
    python -m benchmarks.api_benchmarks
"""

import time
import statistics
from typing import Dict, List, Tuple, Any, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BenchmarkResult:
    """Result of a benchmark test."""
    name: str
    iterations: int
    total_time: float
    min_time: float
    max_time: float
    avg_time: float
    median_time: float
    std_dev: float

    def __str__(self) -> str:
        return (
            f"\n{self.name}\n"
            f"  Iterations: {self.iterations}\n"
            f"  Total Time: {self.total_time:.3f}s\n"
            f"  Avg Time: {self.avg_time:.3f}s\n"
            f"  Min Time: {self.min_time:.3f}s\n"
            f"  Max Time: {self.max_time:.3f}s\n"
            f"  Median Time: {self.median_time:.3f}s\n"
            f"  Std Dev: {self.std_dev:.3f}s"
        )


class BenchmarkSuite:
    """Suite for running and tracking benchmarks."""

    def __init__(self, name: str = "Benchmark Suite") -> None:
        """Initialize benchmark suite."""
        self.name: str = name
        self.results: List[BenchmarkResult] = []

    def benchmark(
        self,
        func: Callable[[], Any],
        name: str,
        iterations: int = 10
    ) -> BenchmarkResult:
        """
        Benchmark a function.

        Args:
            func: Function to benchmark (callable with no arguments)
            name: Name of the benchmark
            iterations: Number of times to run the function

        Returns:
            BenchmarkResult with timing statistics
        """
        times: List[float] = []

        print(f"\n⏱️  Running benchmark: {name}")
        print(f"   Iterations: {iterations}")

        for i in range(iterations):
            start: float = time.time()
            try:
                func()
            except Exception as e:
                print(f"   ⚠️  Error in iteration {i + 1}: {e}")
                continue
            end: float = time.time()
            times.append(end - start)
            print(f"   [{i + 1}/{iterations}] {times[-1]:.3f}s")

        # Calculate statistics
        total_time: float = sum(times)
        min_time: float = min(times) if times else 0
        max_time: float = max(times) if times else 0
        avg_time: float = statistics.mean(times) if times else 0
        median_time: float = statistics.median(times) if times else 0
        std_dev: float = statistics.stdev(times) if len(times) > 1 else 0

        result: BenchmarkResult = BenchmarkResult(
            name=name,
            iterations=len(times),
            total_time=total_time,
            min_time=min_time,
            max_time=max_time,
            avg_time=avg_time,
            median_time=median_time,
            std_dev=std_dev
        )

        self.results.append(result)
        print(result)

        return result

    def print_summary(self) -> None:
        """Print summary of all benchmarks."""
        print(f"\n{'=' * 60}")
        print(f"{self.name} - Summary")
        print(f"{'=' * 60}")

        for result in self.results:
            print(result)

        total_time: float = sum(r.total_time for r in self.results)
        print(f"\nTotal Time: {total_time:.3f}s")
        print(f"Benchmarks Run: {len(self.results)}")

    def export_results(self, filepath: str) -> None:
        """Export results to CSV file."""
        import csv

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Name", "Iterations", "Total Time", "Min Time", "Max Time",
                "Avg Time", "Median Time", "Std Dev"
            ])

            for result in self.results:
                writer.writerow([
                    result.name,
                    result.iterations,
                    f"{result.total_time:.3f}",
                    f"{result.min_time:.3f}",
                    f"{result.max_time:.3f}",
                    f"{result.avg_time:.3f}",
                    f"{result.median_time:.3f}",
                    f"{result.std_dev:.3f}"
                ])

        print(f"\n✅ Results exported to {filepath}")


def benchmark_agent_planning() -> None:
    """Benchmark agent planning performance."""
    from src.config import load_config_and_llm
    from src.agent.planner import Planner

    print("\n" + "=" * 60)
    print("Agent Planning Benchmarks")
    print("=" * 60)

    try:
        config, llm = load_config_and_llm("agent.config.yaml")
        planner = Planner(llm)

        suite = BenchmarkSuite("Agent Planning")

        # Benchmark 1: Simple goal planning
        def simple_planning() -> None:
            planner.plan("Create a simple function")

        suite.benchmark(simple_planning, "Simple Goal Planning", iterations=5)

        # Benchmark 2: Complex goal planning
        def complex_planning() -> None:
            planner.plan("Design and implement a complete REST API with authentication")

        suite.benchmark(complex_planning, "Complex Goal Planning", iterations=3)

        suite.print_summary()
        suite.export_results("benchmarks/agent_planning_results.csv")

    except Exception as e:
        print(f"❌ Error running agent benchmarks: {e}")


def benchmark_repository_scanning() -> None:
    """Benchmark repository scanning performance."""
    from src.config import load_config_and_llm
    from src.repo.scanner import RepositoryScanner

    print("\n" + "=" * 60)
    print("Repository Scanning Benchmarks")
    print("=" * 60)

    try:
        config, llm = load_config_and_llm("agent.config.yaml")
        scanner = RepositoryScanner(".")

        suite = BenchmarkSuite("Repository Scanning")

        # Benchmark: Scan current repository
        def scan_repo() -> None:
            scanner.scan_repository()

        suite.benchmark(scan_repo, "Scan Repository", iterations=3)

        suite.print_summary()
        suite.export_results("benchmarks/repo_scanning_results.csv")

    except Exception as e:
        print(f"❌ Error running repository benchmarks: {e}")


def benchmark_memory_usage() -> None:
    """Benchmark memory usage of agent components."""
    import sys
    from src.config import load_config_and_llm
    from src.agent.planner import Planner
    from src.agent.history import ConversationHistory

    print("\n" + "=" * 60)
    print("Memory Usage Analysis")
    print("=" * 60)

    try:
        config, llm = load_config_and_llm("agent.config.yaml")

        print("\nMemory Analysis:")
        print("-" * 60)

        # Analyze planner memory
        planner = Planner(llm)
        planner_size = sys.getsizeof(planner)
        print(f"Planner object size: {planner_size:,} bytes ({planner_size / 1024:.2f} KB)")

        # Analyze history memory
        history = ConversationHistory()
        for i in range(100):
            history.add_message("user", f"Message {i}: " + "x" * 100)
            history.add_message("assistant", f"Response {i}: " + "y" * 200)

        history_size = sys.getsizeof(history)
        print(f"History object size (100 messages): {history_size:,} bytes ({history_size / 1024:.2f} KB)")

        avg_per_message = history_size / 200
        print(f"Average per message: {avg_per_message:.2f} bytes")

    except Exception as e:
        print(f"❌ Error analyzing memory: {e}")


if __name__ == "__main__":
    print("\n🏃 AI Agent Framework - Performance Benchmarks")
    print("=" * 60)

    # Run benchmarks
    try:
        benchmark_agent_planning()
    except Exception as e:
        print(f"Skipping agent planning benchmarks: {e}")

    try:
        benchmark_repository_scanning()
    except Exception as e:
        print(f"Skipping repository scanning benchmarks: {e}")

    try:
        benchmark_memory_usage()
    except Exception as e:
        print(f"Skipping memory analysis: {e}")

    print("\n✅ Benchmarking complete!")
