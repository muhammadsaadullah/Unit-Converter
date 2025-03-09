import subprocess

def install_package(package):
    subprocess.run(["pip", "install", package])

install_package("python-dotenv")

import dotenv
print("dotenv is installed and imported successfully!")
