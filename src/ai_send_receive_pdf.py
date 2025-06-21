import subprocess
import sys
from os import environ
from dotenv import load_dotenv

#used for getting folder and file path for resume.
from pathlib import Path 

# # Create an llm object to use for the QueryEngine and the ReActAgent
# llm = OpenAI(model="gpt-4")
from google import genai
from google.genai import types
import pathlib
import httpx

import builtins
import os
import weasyprint


def GetFirstFile(directory_path):
    try:
        resume_folder = pathlib.Path(directory_path)
        for resume in resume_folder.iterdir():
            #only look for pdf files.
            if resume.is_file() and resume.suffix == ".pdf":
                return resume.absolute()
        return None
    except FileNotFoundError:
        return None

def GetFileData(file_path):
    return file_path.read_bytes()

def create_directory_if_not_exists(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created or already exists.")
    except OSError as e:
        print(f"Error creating directory '{path}': {e}")

def run_command(command):
    """
    Runs a shell command and prints its output.
    Exits if the command fails.
    """
    try:
        process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(process.stdout)
        if process.stderr:
            print(process.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1) # Exit the script if a command fails




def GetUpdatedResume(prompt, input_resume_data, output_resume_folder, output_resume_name):
    load_dotenv()
    GEMINI_API_KEY = environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
            data=input_resume_data,
            mime_type='application/pdf',
        ),
        prompt])

    #Clean up the response text for html processing.
    resume_html = response.text
    first_bracket = resume_html.find('<')
    last_bracket = resume_html.rfind('>')
    if first_bracket != -1 and last_bracket != -1 and first_bracket < last_bracket :
        resume_html = resume_html[first_bracket : last_bracket+1]
    print("Printing html: " + resume_html)
    create_directory_if_not_exists(output_resume_folder)
    weasyprint.HTML(string = resume_html).write_pdf(output_resume_folder + "/" + output_resume_name)




if __name__ == "__main__":
    # Install uv
    print("Attempting to install uv...")
    run_command("pip install uv")

    # Install google-genai using uv
    print("Attempting to install google-genai using uv...")
    run_command("uv pip install -q -U google-genai")

    # Install weasyprint using uv
    print("Attempting to install weasyprint using uv...")
    run_command("uv pip install weasyprint")

    print("All specified packages have been processed.")
    GetUpdatedResume("Tailor this resume for a programming job posting. Only return the resume in html format.", "../InputResume/", "../OutputResume", "UpdatedResume.pdf")
