#!/usr/bin/env python3
"""
Test runner script for the task_manager application.

This script provides a convenient way to run the pytest test suite with
different configurations and options.

Usage:
    python run_tests.py [options]
    
Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --verbose          # Run with verbose output
    python run_tests.py --fast             # Skip slow tests
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    print(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def install_dependencies():
    """Install testing dependencies."""
    print("📦 Installing testing dependencies...")
    
    # Install requirements
    if not run_command(
        ["pip", "install", "-r", "requirements.txt"],
        "Installing application dependencies"
    ):
        return False
    
    print("✅ Dependencies installed successfully")
    return True


def run_tests(args):
    """Run the pytest test suite with specified options."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add markers based on arguments
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.ai:
        cmd.extend(["-m", "ai"])
    elif args.database:
        cmd.extend(["-m", "database"])
    elif args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Add coverage options
    if args.coverage:
        cmd.extend([
            "--cov=task_manager",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--cov-fail-under=70"
        ])
    
    # Add specific test file if provided
    if args.test_file:
        cmd.append(args.test_file)
    
    # Add parallel execution for faster runs
    if args.parallel:
        cmd.extend(["-n", "auto"])
    
    # Show local variables in tracebacks for debugging
    if args.debug:
        cmd.extend(["--tb=long", "-l"])
    
    # Stop on first failure for quick feedback
    if args.stop_on_fail:
        cmd.append("-x")
    
    # Run the tests
    return run_command(cmd, "Running tests")


def check_code_quality():
    """Run code quality checks."""
    print("\n📋 Running code quality checks...")
    
    # Check if flake8 is available
    try:
        subprocess.run(["flake8", "--version"], 
                      check=True, capture_output=True)
        
        # Run flake8 on the task_manager package
        if run_command(
            ["flake8", "task_manager", "--max-line-length=100", 
             "--ignore=E501,W503", "--exclude=__pycache__,migrations"],
            "Running flake8 code style check"
        ):
            print("✅ Code style check passed")
        else:
            print("⚠️ Code style issues found")
            
    except subprocess.CalledProcessError:
        print("⚠️ flake8 not installed, skipping code style check")


def main():
    """Main function to handle command line arguments and run tests."""
    
    parser = argparse.ArgumentParser(
        description="Test runner for task_manager application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Test selection options
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument(
        "--unit", action="store_true",
        help="Run only unit tests"
    )
    test_group.add_argument(
        "--integration", action="store_true",
        help="Run only integration tests"
    )
    test_group.add_argument(
        "--ai", action="store_true",
        help="Run only AI service tests"
    )
    test_group.add_argument(
        "--database", action="store_true",
        help="Run only database tests"
    )
    test_group.add_argument(
        "--fast", action="store_true",
        help="Skip slow tests"
    )
    
    # Output options
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", "-c", action="store_true",
        help="Run with coverage report"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true",
        help="Show detailed traceback information"
    )
    
    # Execution options
    parser.add_argument(
        "--parallel", "-p", action="store_true",
        help="Run tests in parallel (requires pytest-xdist)"
    )
    parser.add_argument(
        "--stop-on-fail", "-x", action="store_true",
        help="Stop on first failure"
    )
    parser.add_argument(
        "--install-deps", action="store_true",
        help="Install dependencies before running tests"
    )
    parser.add_argument(
        "--check-style", action="store_true",
        help="Run code style checks"
    )
    
    # File selection
    parser.add_argument(
        "--test-file", "-f", type=str,
        help="Run specific test file"
    )
    
    args = parser.parse_args()
    
    # Change to the task_manager directory
    task_manager_dir = Path(__file__).parent / "task_manager"
    if task_manager_dir.exists():
        import os
        os.chdir(task_manager_dir)
        print(f"📁 Changed to directory: {task_manager_dir}")
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Run code quality checks if requested
    if args.check_style:
        check_code_quality()
    
    # Run the tests
    print("\n🧪 Starting test execution...")
    
    success = run_tests(args)
    
    if success:
        print("\n🎉 All tests completed successfully!")
        
        # Show coverage report location if coverage was run
        if args.coverage:
            print("📊 Coverage report available at: htmlcov/index.html")
        
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 