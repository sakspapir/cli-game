# Setting Up a Virtual Environment (venv) for Your Project

## Steps to Create a Virtual Environment and Install Dependencies

1. **Open your terminal** (Command Prompt, PowerShell, or any terminal emulator).

2. **Navigate to your project directory** where your requirements.txt file is located:
    ```
    cd path/to/your/project
3. **Create a Virtual Environment**
Run the following command to create a virtual environment named .venv:
    ```  
    python -m venv .venv
4. **Activate the Virtual Environment**

    *4.1 Windows:*
    
        .venv\Scripts\activate

    *4.2 On macOS and Linux:*

        source .venv/bin/activate

5. **Install Dependencies**
With the virtual environment activated, install the dependencies listed in your requirements.txt file:

    ```
    pip install -r requirements.txt
6. **Deactivate the Virtual Environment**
Once you are done working in the virtual environment, you can deactivate it by running:

    ```
    deactivate
Additional Tips
Checking Installed Packages: To see a list of installed packages in your virtual environment, use:
pip list

Freezing Dependencies: If you add new packages and want to update your requirements.txt file, run:
pip freeze > requirements.txt
