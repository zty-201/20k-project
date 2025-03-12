# run_dashboard.py
import subprocess
import os

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    subprocess.run(["streamlit", "run", file_path])