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

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database


# CONFIG
def getConfig():

    db = Database()
    config = db.fetch_as_json("""
        SELECT * 
        from config
    """)
    db.close()

    return config[0] if len(config) != 0 else None