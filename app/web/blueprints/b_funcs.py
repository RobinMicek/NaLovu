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

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session, abort

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.game import Game

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_funcs = Blueprint(
    "b_funcs", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_funcs.route("/remove-question")
def func_removeQuestion():

    Game().remove_question(questionId=request.args.get("questionId", None))
    
    return redirect("/screens/questions")


@b_funcs.route("/get-questions")
def func_getQuestions():

    return Game().get_all_questions()
    


@b_funcs.route("/get-question")
def func_getQuestion():

    return Game().get_question()


@b_funcs.route("/get-player-names")
def func_getPlayerNames():

    return Game().get_player_names()


@b_funcs.route("/change-state")
def func_changeState():

    return str(Game().update_config_state(state=request.args.get("state", None), questionId=request.args.get("questionId", None)))


@b_funcs.route("/pick-answer")
def func_pickAnswer():

    return str(Game().pick_answer(role=request.args.get("role", None), pickedAnswer=request.args.get("pickedAnswer", None)))


@b_funcs.route("/clear-session")
def func_clearSession():
    
    Game().clear_session()
    Game().update_config_state(state="INTRO")

    return "OK!"


# Socket control
@b_funcs.route("/socket-guess-start")
def func_socket_guessStart():

    Game().send_local_socket_message(event="guessStart", msg="Players may now start picking their answers", data={})

    return "OK!"


@b_funcs.route("/socket-show-answer")
def func_socket_showAnswer():
    role = request.args.get("role", None)

    Game().send_local_socket_message(event=f"showAnswer-{ role }", msg=f"Show answer for { role }", data={})

    return "OK!"


@b_funcs.route("/socket-reload-screens")
def func_socket_reloadScreens():
    
    Game().send_local_socket_message(event=f"reloadScreens", msg=f"Reload all the screens", data={})

    return "OK!"