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
import sqlite3
import json

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))    
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()


    def close(self):
        self.connection.commit()
        self.connection.close()


    def initialize(self):
        # Initializes a new database with all the necessary tables, etc.
        # SQL script is saved in sql/init.sql and sql/procedures.sql files.
        try:
            for x in self.handle_sql_file(filename="init.sql"):
                self.cursor.execute(x)
                

            create_log(type="ALERT", message="Database has been initialized.")
            print("[ALERT] Database has been initialized.")

        except sqlite3.Error as e:
            create_log(type="ERROR", message=f"Could not initialize the database [{e}]")
            print(f"[ERROR] Could not initialize the database [{e}]")


    def clear(self):
        # Clears the used database.
        # SQL script is saved in sql/clear.sql file.
        try:
            for x in self.handle_sql_file(filename="clear.sql"):
                self.cursor.execute(x)

            create_log(type="ALERT", message="Database has been cleaned.")
            print("[ALERT] Database has been cleaned.")


        except sqlite3.Error as e:
            create_log(type="ERROR", message=f"Could not clear the database [{e}]")
            print(f"[ERROR] Could not clear the database [{e}]")


    def handle_sql_file(self, filename=None):
        # This function takes a SQL script file and splits it into individual statements.
        # I'm doing this because I had problems with executing multiple statements
        # as one using cursor.execute(x, multi=True)

        # This function only takes files from the /sql/ directory
        with open(os.path.join(os.path.dirname(__file__), "sql/" + str(filename)), "r+") as f:
            script = f.read()

            if filename == "init.sql" or filename == "clear.sql":
                script = script.split(";")
                for i, x in enumerate(script):
                    script[i] = x.strip()

            elif filename == "procedures.sql":
                script = script.split("//")
                for i, x in enumerate(script):
                    script[i] = x.strip()            
            
            elif filename == "triggers.sql":
                script = script.split("//")
                for i, x in enumerate(script):
                    script[i] = x.strip()            

        return script
    

    def fetch_as_json(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in self.cursor.description]

        # Convert the rows to a list of dictionaries
        results = [dict(zip(column_names, row)) for row in rows]
        
        return results

    

# Inicialize the DB if the file is called directly
if __name__ == "__main__":
    db = Database()

    db.clear()
    db.initialize()
    db.close()
