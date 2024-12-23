# Dicrathon - Vista Voyagers

This repository contains the source code for the Dicrathon - Vista Voyagers project. Follow the steps below to set up and run the project on your local machine.

## Prerequisites

1. **Python**: Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. **Visual Studio Code (VS Code)**: Download and install Visual Studio Code from [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download).

## Setup Instructions

### Step 1: Install Python Extension in VS Code

- Open VS Code.
- Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window.
- Search for "Python" and install the official Python extension provided by Microsoft.

### Step 2: Clone the Repository

- Open the terminal in VS Code or your preferred terminal application.
- Run the following command to clone the repository:
  ```bash
  git clone https://github.com/chewkxmy/Dicrathon---Vista-Voyagers.git
  ```

### Step 3: Install Required Modules

- Navigate to the project directory:
  ```bash
  cd Dicrathon---Vista-Voyagers
  ```
- Install the required Python modules using pip:
  ```bash
  pip install django
  ```

> **Note:** If the terminal shows an error like `ModuleNotFoundError: No module named 'xxx'`, repeat this step to install the missing module by replacing `xxx` with the module name.

### Step 4: Run the Server

- Start the Django development server:
  ```bash
  python manage.py runserver
  ```

- After running the command, the terminal will display a link (e.g., `http://127.0.0.1:8000/`).
- Click on the link or copy it into your web browser to view the website.

## Troubleshooting

- Ensure Python and pip are correctly installed and added to your system's PATH.
- If any modules are missing, refer to Step 3 to install them.
- If you encounter any other issues, check the terminal output for error messages and resolve them accordingly.

---

Enjoy exploring the Dicrathon - Vista Voyagers project!
