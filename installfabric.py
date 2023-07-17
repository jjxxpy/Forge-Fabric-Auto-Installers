import os
import tkinter as tk
import requests
import subprocess
import tempfile

def download_resource():
    url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.exe"
    filename = "fabric-installer-0.11.2.exe"

    response = requests.get(url)
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    print("Resource downloaded successfully!")
    print("File saved to:", file_path)

    # Open or execute the downloaded file
    subprocess.Popen(file_path)

# Call the download_resource function automatically
download_resource()

# Create the main window
window = tk.Tk()
window.title("Fabric Installer close when done")

# Start the main event loop
window.mainloop()
