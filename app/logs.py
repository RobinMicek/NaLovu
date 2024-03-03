"""
********************************************************

    Tento kód je součástí projektu 'Na Lovu'.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
"""

# PACKAGES IMPORTS
import os
import sys

# IMPORTS FROM PACKAGES
from datetime import datetime

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


def create_log(type = None, message = None):

    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%d-%m-%Y")

    log_directory = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, f"{current_day}.txt")

    with open(log_file_path, "a") as f:
        f.write(f"{current_datetime} [{type}] {message}\n\n")