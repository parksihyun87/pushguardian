"""
Benchmark runner script for PushGuardian.

Usage:
    python run_benchmark.py
"""

import sys
from pathlib import Path
from pushguardian.benchmark.runner import run_all_benchmarks
from pushguardian.benchmark.report_generator import generate_markdown_report, save_report


def main():
    """Run benchmarks and generate report."""
    print("🔍 PushGuardian Benchmark Suite")
    print("=" * 60)
    print()

    # Locate examples directory
    examples_dir = Path(__file__).parent / "examples" / "test_file"

    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        sys.exit(1)

    print(f"📂 Test files directory: {examples_dir}")
    test_files = list(examples_dir.glob("*.txt"))
    print(f"📝 Found {len(test_files)} test files")
    print()

    # Run benchmarks
    print("🚀 Running benchmarks...")
    print("-" * 60)
    results = run_all_benchmarks(examples_dir)
    print()

    if not results:
        print("❌ No results collected")
        sys.exit(1)

    print(f"✅ Completed {len(results)} benchmarks")
    print()

    # Generate report
    print("📄 Generating markdown report...")
    report = generate_markdown_report(results)

    # Save report
    output_dir = Path(__file__).parent / "benchmark_reports"
    output_dir.mkdir(exist_ok=True)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"benchmark_{timestamp}.md"

    save_report(report, str(report_path))

    print(f"✅ Report saved: {report_path}")
    print()
    print("=" * 60)
    print("✨ Benchmark complete!")


if __name__ == "__main__":
    main()
