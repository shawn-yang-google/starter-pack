import argparse
import cloudpickle
import logging
import os
import tempfile

from app.app import create_agent
from vertexai.preview import reasoning_engines
import vertexai

def serializable_or_raise(obj):
    """Checks if an object is serializable using cloudpickle.

    Args:
        obj: The object to check.

    Raises:
        Exception: If the object is not serializable.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "temp_pickle.pkl")
        with open(temp_file, "wb") as f:
            try:
                cloudpickle.dump(obj, f)
            except Exception as e:
                raise Exception(f"Object cannot be dumped: {e}")

        with open(temp_file, "rb") as f:
            try:
                obj = cloudpickle.load(f)
            except Exception as e:
                raise Exception(f"Object cannot be loaded: {e}")


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
    try:
        import pkg_resources
    except ImportError:
        # Handle the case where pkg_resources is not available
        # Likely due to the deprecation (i.e., https://github.com/mu-editor/mu/issues/2485).
        logging.info("pkg_resources not found.  Functionality relying on it will be disabled.")
        return installed_packages
    
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
        default="dependencies/requirements.txt",
        help="Comma-separated list of requirements, or path to requirements.txt.",
    )
    parser.add_argument(
        "--extra_packages",
        type=str,
        default="dependencies/extra_packages.txt",
        help="Comma-separated list of extra packages to include, or path to extra_packages.txt.",
    )
    parser.add_argument(
        "--project_id",
        type=str,
        help="The default project to use when making API calls.",
        required=True,
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
        required=True,
    )
    return parser.parse_args()
    

def main():
    """Deploys the agent to Vertex AI."""

    args = get_args()

    # Authentication.
    logging.warning(f"project_id: {args.project_id}; location: {args.location}; staging_bucket: {args.staging_bucket}")
    vertexai.init(
        project=args.project_id,
        location=args.location,
        staging_bucket=args.staging_bucket,
        api_endpoint='us-central1-autopush-aiplatform.sandbox.googleapis.com',
    )
    
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

    agent = create_agent()
    # Check if the agent is serializable
    serializable_or_raise(agent)

    # Warning the missing packages.
    missing_packages = get_missing_packages(requirements)
    if missing_packages:
        logging.warning(f"The following packages are installed but not listed in requirements: {missing_packages}")
    else:
        logging.info("All installed packages are listed in requirements")

    reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=requirements,
        extra_packages=extra_packages,
    )

if __name__ == "__main__":
    main()
