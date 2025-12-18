import sys
import subprocess
import importlib.util
import os


# Function to check and install the C++ engine if not present
def ensure_cpp_engine_installed():
    """
    Checks if connect4_core is installed. If not, finds the .whl file
    in the 'wheels' folder and installs it automatically.
    """
    if importlib.util.find_spec("connect4_core") is not None:
        return  # Already installed!

    print("C++ Engine for Connect4 not found. Installing pre-compiled wheel...")

    # Define path to the 'wheels' folder relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wheel_dir = os.path.join(base_dir, 'wheels')

    if not os.path.exists(wheel_dir):
        print(f"Error: Could not find 'wheels' folder at: {wheel_dir}")
        print("Please ensure you have downloaded the full repository.")
        sys.exit(1)

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "connect4_core",
            "--no-index",
            f"--find-links={wheel_dir}"
        ])
        print("Installation complete! Launching game...")
    except subprocess.CalledProcessError:
        print("Critical Error: Could not find a compatible version of the engine for your OS.")
        print("Please ensure the 'wheels' folder contains a version for your platform (Windows/Linux/Mac).")
        sys.exit(1)


ensure_cpp_engine_installed()

if __name__ == "__main__":
    from ui.Gui import Gui

    gui = Gui()
    gui.start()
