import sys
import subprocess
import importlib.util
import os


# Function to check and install the C++ engine if not present
def ensure_cpp_engine_installed():
    """
    Checks if connect4_core is installed.
    1. Tries to install a pre-compiled wheel from the 'wheels' folder (Fast/Windows).
    2. If that fails, attempts to compile from source (Mac/Linux).
    """
    if importlib.util.find_spec("connect4_core") is not None:
        return  # Already installed!

    print("C++ Engine for Connect4 not found...")

    # Define path to the 'wheels' folder relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wheel_dir = os.path.join(base_dir, 'wheels')

    # --- ATTEMPT 1: Install Pre-Compiled Wheel (Priority) ---
    try:
        if os.path.exists(wheel_dir):
            print("Attempting to install pre-compiled wheel...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "connect4_core",
                "--no-index",
                "--force-reinstall",
                f"--find-links={wheel_dir}"
            ])
            print("Installation complete! Launching game...")
            return
        else:
            print(f"Warning: 'wheels' folder not found at: {wheel_dir}")

    except subprocess.CalledProcessError:
        print("Pre-compiled wheel not compatible or not found for this OS.")

    # --- ATTEMPT 2: Compile from Source (Fallback) ---
    print("Attempting to compile from source (This may take a moment)...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "."
        ])
        print("Engine compiled and installed successfully! Launching game...")

    except subprocess.CalledProcessError:
        print("\nCRITICAL ERROR: Could not install the C++ engine.")
        print("1. If you are on Windows, ensure the 'wheels' folder is present.")
        print("2. If you are on Mac/Linux, ensure you have a C++ compiler installed (Xcode/g++).")
        sys.exit(1)


ensure_cpp_engine_installed()

if __name__ == "__main__":
    from ui.Gui import Gui

    gui = Gui()
    gui.start()
