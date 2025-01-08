import cloudpickle
import tempfile
import os
import pkg_resources

def check_serializable(obj):
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


def generate_requirements_file(requirements, filename="requirements.txt"):
    """Generates a requirements.txt file from a list of requirements.

    Args:
        requirements: A list of requirement strings.
        filename: The name of the output file (default: "requirements.txt").
    """
    with open(filename, "w") as f:
        for req in requirements:
            f.write(req + "\n")


def get_missing_requirements(required_packages):
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
