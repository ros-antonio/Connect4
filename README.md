# 🔴 Connect 4: Turbo Edition (Python + C++)

A high-performance implementation of the classic Connect Four strategy game, featuring a polished Python `tkinter` GUI backed by a **compiled C++ calculation engine**.

This project utilizes a hybrid architecture: application logic, state management, and the user interface are implemented in Python for flexibility, while computationally intensive AI decision-making is offloaded to a custom C++ module via `pybind11` for optimal execution speed.

## 🚀 Key Features

* **Hybrid Computation Engine:**
    * **Python Frontend:** Manages the user interface, game loop, and heuristics for lower difficulty levels.
    * **C++ Backend:** Powers the "Hard" and "Impossible" difficulty settings using a highly optimized Minimax algorithm with Alpha-Beta pruning.
* **Adaptive Difficulty Levels:**
    * **Easy:** Executes random valid moves (introductory level).
    * **Medium:** Prioritizes immediate defensive blocks and winning opportunities (heuristic-based).
    * **Hard:** Utilizes the C++ engine at **Depth 5** for strong tactical gameplay.
    * **Impossible:** Utilizes the C++ engine at **Depth 9**, analyzing approximately 40 million positions instantly for near-perfect play.
* **Smart Installation System:** The application includes a self-installing script.
    * **Windows:** Installs a pre-compiled binary wheel (no compiler required).
    * **Mac/Linux:** Automatically compiles the engine from source upon first launch.
* **Enhanced User Interface:**
    * **Visual Aids:** Includes "Ghost Piece" indicators for move prediction and highlights the most recent move.
    * **Dynamic Configuration:** Allows users to modify difficulty settings seamlessly during gameplay via the menu system.

## 📸 Interface

<img src="game_ss.png" width="40%" alt="Connect Four Game Board">

## 🛠️ System Architecture

The project adheres to a layered architecture to ensure separation of concerns:

* **Presentation Layer (`ui/`):** Manages the graphical interface and user interactions using Tkinter.
* **Service Layer (`services/`):** Acts as the controller, synchronizing the Python game state with the C++ backend logic (`game.py`).
* **Core Engine (`services/connect4_core.cpp`):** The high-performance core. A pure C++ implementation of the game rules and Minimax algorithm, exposed to the Python environment via `pybind11` bindings.

## 📦 Installation & Usage

**Prerequisites:** Python 3.10+

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ros-antonio/Connect4.git
    cd Connect4
    ```

2.  **Initialize Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Launch the Application:**
    Run the entry script to initialize the game. This script handles the installation of the C++ engine automatically.
    ```bash
    python start.py
    ```
    * **Windows:** The game will launch immediately using the included binary.
    * **Mac/Linux:** The first run may take a few seconds to compile the engine.

## ❓ Troubleshooting

* **Windows: "Script cannot be loaded / Access Denied"**
  If you see a security error when activating the virtual environment, this is a default PowerShell setting. You can fix it by running this command in PowerShell once:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

* **Mac/Linux: "Could not compile the engine"**
  If the automatic compilation fails, ensure you have standard C++ build tools installed:
    * **macOS:** Run `xcode-select --install` in your terminal.
    * **Linux:** Ensure `g++` is installed (e.g., `sudo apt install build-essential`).

## 📝 License

This project is open-source software licensed under the MIT License.