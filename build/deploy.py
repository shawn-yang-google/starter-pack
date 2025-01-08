import argparse
import os
from build import utils
from app import app
from vertexai.preview import reasoning_engines

def main(requirements, extra_packages):
    """Deploys the agent to Vertex AI."""

    agent = app.create_agent()
    # Check if the agent is serializable (add this to utils.py later)
    try:
        utils.check_serializable(agent)
        print("Agent is serializable.")
    except Exception as e:
        print(f"Agent serialization check failed: {e}")
        return

    # You might want to add pip freeze here if needed

    reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=requirements,
        extra_packages=extra_packages,
        # Add other parameters as needed
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy a Reasoning Engine agent.")
    parser.add_argument(
        "--requirements",
        type=str,
        help="Comma-separated list of requirements, or path to requirements.txt",
    )
    parser.add_argument(
        "--extra_packages",
        type=str,
        help="Comma-separated list of extra packages to include, or a directory",
    )

    args = parser.parse_args()

    # Handle requirements
    if os.path.isfile(args.requirements):
        with open(args.requirements, 'r') as f:
            requirements = [line.strip() for line in f]
    else:
        requirements = [r.strip() for r in args.requirements.split(",")]

    # Handle extra packages
    if os.path.isdir(args.extra_packages):
        extra_packages = [
            os.path.join(args.extra_packages, f)
            for f in os.listdir(args.extra_packages)
            if os.path.isfile(os.path.join(args.extra_packages, f))
        ]
    else:
        extra_packages = [pkg.strip() for pkg in args.extra_packages.split(",")]

    main(requirements, extra_packages)
