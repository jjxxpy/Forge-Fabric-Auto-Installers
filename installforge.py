import os
import tkinter as tk
import requests
import subprocess
import tempfile
import atexit
import sys
from tqdm import tqdm

def download_resource(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    
    progress_bar.close()
    print("Resource downloaded successfully!")
    print("File saved to:", file_path)
    return file_path

def download_and_install_java():
    java_url = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/372925194/af25c85b-cc58-47b7-b5eb-bd07dc33185d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230715%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230715T091116Z&X-Amz-Expires=300&X-Amz-Signature=3b4e0a2e0d5005fb91c235352dd74f561bc28b54ff8ac73f6c701d2938f52ffe&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=372925194&response-content-disposition=attachment%3B%20filename%3DOpenJDK17U-jdk_x64_windows_hotspot_17.0.7_7.msi&response-content-type=application%2Foctet-stream"
    java_filename = "OpenJDK17U-jdk_x64_windows_hotspot_17.0.7_7.msi"
    
    file_path = download_resource(java_url, java_filename)
    
    print("Installing Java...")
    subprocess.call(['msiexec', '/i', file_path, '/quiet'])
    print("Java installation completed.")

def check_java_version():
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    output = result.stderr

    if "version \"17" in output:
        print("Java 17 or above is already installed.")
    else:
        print("Java 17 or above not found. Downloading and installing Java...")
        download_and_install_java()

def run_jar_file():
    url = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.1.0/forge-1.20.1-47.1.0-installer.jar"
    filename = "forge-1.20.1-47.1.0-installer.jar"

    file_path = download_resource(url, filename)

    # Execute the downloaded JAR file using Java
    java_executable = "java"
    subprocess.Popen([java_executable, "-jar", file_path])

def cleanup():
    temp_dir = tempfile.gettempdir()
    filename = "forge-1.20.1-47.1.0-installer.jar"
    file_path = os.path.join(temp_dir, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Temporary file deleted.")

# Register the cleanup function to run on program exit
atexit.register(cleanup)

# Check Java version
check_java_version()

# Call the run_jar_file function automatically
run_jar_file()

# Create the main window
window = tk.Tk()
window.title("Install Forge than close the windows.")

# Start the main event loop
window.mainloop()
sys.exit()