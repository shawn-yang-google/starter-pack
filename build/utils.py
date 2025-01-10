import argparse
import cloudpickle
import tempfile
import os
import pkg_resources

from app import app
from build import utils
from vertexai.preview import reasoning_engines

def is_serializable_or_raise(obj):
    """Checks if an object is serializable using cloudpickle.

    Args:
        obj: The object to check.

    Raises:
        Exception: If the object is not serializable.
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "temp_pickle.pkl")
            with open(temp_file, "wb") as f:
                cloudpickle.dump(obj, f)

    except Exception as e:
        raise Exception(f"Object is not serializable: {e}")

def get_missing_packages(required_packages):
    """
    Compares the provided list of required packages with the installed packages
    and returns a list of packages that are installed but not in the required list.

    Args:
        required_packages: A list of package names (e.g., ["requests", "numpy"]).

    Returns:
        A list of strings, where each string represents a missing package
        in the format "package==version".
    """
    installed_packages = []
    for dist in pkg_resources.working_set:
        installed_packages.append(f"{dist.project_name}=={dist.version}")
        
    # Create a set of required package names (lowercase for case-insensitive comparison)
    required_packages_set = {pkg.lower() for pkg in required_packages}

    missing_packages = []
    for package in installed_packages:
        package_name = package.split("==")[0].lower()
        if package_name not in required_packages_set:
            missing_packages.append(package)
    
    return missing_packages

def get_args():
    parser = argparse.ArgumentParser(description="Deploy a Reasoning Engine agent.")
    parser.add_argument(
        "--requirements",
        type=str,
        help="Comma-separated list of requirements, or path to requirements.txt.",
    )
    parser.add_argument(
        "--extra_packages",
        type=str,
        help="Comma-separated list of extra packages to include, or a directory.",
    )
    parser.add_argument(
        "--project_id",
        type=str,
        help="The default project to use when making API calls.",
    )
    parser.add_argument(
        "--location",
        type=str,
        default="us-central1",
        help="The default location to use when making API calls. If not set defaults to us-central-1.",
    )
    parser.add_argument(
        "--staging_bucket",
        type=str,
        help="The default staging bucket to use to stage artifacts when making API calls. In the form gs://...",
    )
    return parser.parse_args()
    

def main():
    """Deploys the agent to Vertex AI."""

    args = get_args()
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

    # Authentication.
    vertexai.init(
        project=args.project_id,
        location=args.location,
        staging_bucket=args.staging_bucket,
    )

    agent = app.create_agent()
    # Check if the agent is serializable
    try:
        check_serializable(agent)
        print("Agent is serializable.")
    except Exception as e:
        print(f"Agent serialization check failed: {e}")
        return

    missing_packages = get_missing_packages(requirements)
    if missing_packages:
        print("The following packages are installed but not listed in requirements:")
        for pkg in missing_packages:
            print(pkg)
    else:
        print("All installed packages are listed in requirements")

    reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=requirements,
        extra_packages=extra_packages,
    )

if __name__ == "__main__":
    main()
