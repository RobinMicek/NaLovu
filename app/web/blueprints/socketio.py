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
import json

import socketio

# IMPORTS FROM PACKAGES
from flask import request, Blueprint
from flask_socketio import SocketIO, emit, disconnect, join_room

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from logs import create_log
from database.handle_database import Database
from flask import current_app

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# EVENTS 
# SERVER - Communication with the frontend screens

# Initialize and run the Socket.IO server
def start_socketio_server(sioServer):

    @sioServer.on('connect', namespace='/')
    def socketioServer_handle_connection():

        try:
            create_log(type="ALERT", message=f"'{request.sid}' connected to the local socketio server [Local Connection]")
        
        except:
            create_log(type="ERROR", message=f"'{request.sid}' could not connect to the local socketio server [Local Connection]")


    @sioServer.on('disconnect', namespace='/')
    def socketioServer_handle_connection():
        create_log(type="ALERT", message=f"'{request.sid}' disconnected from the local socketio server [Local Connection]")
