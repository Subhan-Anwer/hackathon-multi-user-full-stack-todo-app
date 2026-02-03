#!/usr/bin/env python3
"""
Authentication Flow Test Runner

This script runs the authentication flow tests to verify:
1. JWT token verification works correctly
2. User isolation is enforced properly
3. Cross-user access is prevented
4. Invalid tokens are rejected
"""

import subprocess
import sys
import os

def run_auth_tests():
    """Run the authentication flow tests."""
    print("🔍 Running Authentication Flow Tests...")
    print("=" * 50)

    # Change to the backend directory
    backend_dir = "/mnt/d/GSIT/Hackathon-II-Todo-Spec-Driven-Development/hackathon-multi-user-full-stack-todo-app/backend"
    os.chdir(backend_dir)

    # Install required dependencies for testing
    print("📦 Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-mock", "requests"], check=True)

    # Run the specific auth flow tests
    print("\n🧪 Executing Authentication Tests...")
    result = subprocess.run([
        "python", "-m", "pytest",
        "tests/test_auth_flow.py",
        "-v",
        "--tb=short"
    ])

    print("\n" + "=" * 50)
    if result.returncode == 0:
        print("✅ All Authentication Flow Tests PASSED!")
        print("🔒 JWT verification and user isolation working correctly")
    else:
        print("❌ Some Authentication Flow Tests FAILED!")
        print("⚠️  Please check the test output above for details")

    return result.returncode

if __name__ == "__main__":
    exit(run_auth_tests())