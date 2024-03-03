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
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.game import Game

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_screens = Blueprint(
    "screens", 
    __name__,
    template_folder='templates'
)


@b_screens.route("/admin")
def page_screenAdmin():
    return render_extended_template("/screens/admin.html",
        players = Game().get_player_names()                                
    )


@b_screens.route("/player")
def page_screenPlayer():
    return render_extended_template("/screens/player.html",
        role = request.args.get("role", "player")    
    )


@b_screens.route("/player/config", methods=["POST", "GET"])
def page_screenPlayerConfig():
    if request.method != "POST":
        return render_extended_template("/screens/player-config.html")
    
    else:
        Game().update_player_name(role=request.form.get("role", None), name=request.form.get("name", None))

        return redirect(f"/screens/player?role={ request.form.get('role', None) }")
    

@b_screens.route("/stream")
def page_screenStream():
    return render_extended_template("/screens/stream.html",
        players = Game().get_player_names()                                    
    )


@b_screens.route("/questions", methods=["POST", "GET"])
def page_screenQuestions():
    if request.method != "POST":
        return render_extended_template("/screens/questions.html",
            questions = Game().get_all_questions_with_answers()
        )
    
    else:

        question = {"questionText": request.form.get("questionText", None)}
        question["answers"] = {
            "A": {
                "text": request.form.get("answerA", None),
                "isCorrect": True if request.form.get("correctAnswerType") == "A" else False
            },
            "B": {
                "text": request.form.get("answerB", None),
                "isCorrect": True if request.form.get("correctAnswerType") == "B" else False
            },
            "C": {
                "text": request.form.get("answerC", None),
                "isCorrect": True if request.form.get("correctAnswerType") == "C" else False
            },
        }

        Game().add_question(question)

        return redirect("/screens/questions")
    