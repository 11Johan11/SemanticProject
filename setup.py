import subprocess
import sys

def install_packages():
    """Install required Python packages from requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All required packages have been installed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install required packages: {e}")
        sys.exit(1)

def run_project():
    """Run your project."""
    try:
        # Replace 'main.py' with your project’s entry point
        subprocess.check_call([sys.executable, "app.py"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_packages()
    run_project()