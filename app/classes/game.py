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
import datetime

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from getConfig import getConfig

from flask import current_app

from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Game():

    def __init__(self): 
        pass

    
    def add_question(self, data = None):
        # Data format: {"answers": {"A": {"isCorrect": true, "text": ""}, "B": {"isCorrect": false, "text": ""}, "C": {"isCorrect": false, "text": ""}}, "questionText": ""}
        
        if data != None:
            correctAnswerId = 0
            questionId = 0
            db = Database()

            # Insert question
            db.cursor.execute(f"""
                INSERT INTO questions 
                    (text)
                VALUES
                ("{data["questionText"]}")       
            """)
            questionId = db.cursor.lastrowid


            # Insert answers
            for answer in data["answers"]:

                db.cursor.execute(f"""
                    INSERT INTO answers
                        (questionId, text, type)
                    VALUES
                        ("{questionId}", "{data["answers"][answer]["text"]}", "{answer}")
                """)

                if data["answers"][answer]["isCorrect"]:
                    correctAnswerId = db.cursor.lastrowid


            # Pair correctAnswerId to answerId
            db.cursor.execute(f"""
                UPDATE questions
                SET correctAnswerId = "{correctAnswerId}"
                WHERE questionId = "{questionId}"
            """)
                

            db.close()


    def remove_question(self, questionId = None):
        
        db = Database()
        
        db.cursor.execute(f"""
            DELETE
            FROM questions
            WHERE questionId = "{questionId}"
        """)
        db.cursor.execute(f"""
            DELETE
            FROM answers
            WHERE questionId = "{questionId}"
        """)

        db.close()


    def get_all_questions(self):

        db = Database()
        query = db.fetch_as_json(f"""
            SELECT
                questions.questionId,
                questions.text,
                answers.text AS correctAnswer
            FROM questions
            JOIN answers ON questions.correctAnswerId = answers.answerId
            WHERE questions.questionId NOT IN (SELECT questionId FROM answeredQuestions)
        """)

        db.close()

        return query
    

    def get_all_questions_with_answers(self):

        db = Database()
        query = db.fetch_as_json(f"""
            SELECT*
            FROM questions
        """)

        if query != None and len(query) != 0:
            for question in query:
                answers = db.fetch_as_json(f"""
                    SELECT *
                    FROM answers
                    WHERE questionId = "{ question["questionId"] }"
                    ORDER BY type
                """)

                question["answers"] = answers

        db.close()

        return query
    

    def get_question(self):

        currentQuestionId = getConfig()["currentQuestionId"]

        db = Database()
        question = db.fetch_as_json(f"""
            SELECT *
            FROM questions
            WHERE questionId = "{ currentQuestionId }"
        """)

        if question != None and len(question) != 0:
            question = question[0]

            answers = db.fetch_as_json(f"""
                SELECT *
                FROM answers
                WHERE questionId = "{ currentQuestionId }"
                ORDER BY type
            """)

            question["answers"] = answers

            db.close()

            return question
        
        db.close()
        
        return False
    

    def get_player_answers(self):

        currentQuestionId = getConfig()["currentQuestionId"]
        
        db = Database()
        query = db.fetch_as_json(f"""
            SELECT *
            FROM playersAnswers 
            JOIN players ON playersAnswers.role = players.role
            WHERE playersAnswers.questionId = "{ currentQuestionId }"
        """)

        db.close()

        return query
    

    def get_player_names(self):
        
        db = Database()
        query = db.fetch_as_json(f"""
            SELECT *
            FROM players
        """)

        db.close()

        return query


    def update_config_state(self, state = None, questionId = None):
        
        # The game loop has 4 states
        # INTRO - Admin chooses question
        # GUESS - Player and Chaser are picking an answer
        #   Control over starting the guessing is handled by another socket event
        # SHOW Shows the answers player and chaser have picked
        #   Control over showing the individual answers is handled by another socket event
        # END - Closes current question and switches to INTRO for a new one

        if state not in ["INTRO", "GUESS", "SHOW", "END"]:
            return False
        

        def update_state_db():
            db = Database()
            db.cursor.execute(f"""
                UPDATE config
                SET currentState = "{ state }", currentQuestionId = "{ questionId if questionId != None else "NULL" }"
            """)

            db.close()

        
        try:
            if state == "INTRO":
                update_state_db()

                self.send_local_socket_message(event="INTRO", msg="Changed game state to INTRO", data={})


            if state == "GUESS":
                update_state_db()

                self.send_local_socket_message(event="GUESS", msg="Changed game state to GUESS", data={"question": self.get_question()})


            if state == "SHOW":
                update_state_db()

                # Set answer to "D" (dont wanna answer) if no answer was picked by the user
                self.pick_answer(role="player", pickedAnswer="D")
                self.pick_answer(role="chaser", pickedAnswer="D")

                self.send_local_socket_message(event="SHOW", msg="Changed game state to SHOW", data={"question": self.get_question(), "playerAnswers": self.get_player_answers()})

            if state == "END":
                update_state_db()

                db = Database()
                db.cursor.execute(f"""
                    INSERT INTO answeredQuestions
                        (questionId)
                    VALUES
                        ("{ questionId }")
                """)
                db.close()

                self.send_local_socket_message(event="END", msg="Changed game state to END", data={})

                
            create_log(type="ALERT", message=f"Changed the config state to { state }")
            return True

        except Exception as e:
            create_log(type="ERROR", message=f"Could not change the config state [New State: { state }] [{ e }]")
            return False


    
    def update_player_name(self, role = None, name = None):

        db = Database()
        db.cursor.execute(f"""
            UPDATE players
            SET name = "{ name }"
            WHERE role = "{ role }"
        """)

        db.close()

    
    def pick_answer(self, role = None, pickedAnswer = None):

        for answer in self.get_player_answers():
            if answer["role"] == role:
                return False

        currentQuestionId = getConfig()["currentQuestionId"]

        db = Database()
        db.cursor.execute(f"""
            INSERT INTO playersAnswers
                (questionId, pickedAns, role)
            VALUES
                ("{ currentQuestionId }", "{ pickedAnswer }", "{ role }")      
        """)

        db.close()

        self.send_local_socket_message(event=f"answered-{ role }", msg=f"{ role } chose an answer", data={"pickedAnswer": f"{pickedAnswer}"})

        return True

    
    def clear_session(self):

        db = Database()
        db.cursor.execute("DELETE FROM answeredQuestions")
        db.cursor.execute("DELETE FROM playersAnswers")
        db.cursor.execute("UPDATE config  SET currentQuestionId = NULL")

        db.close()


    def send_local_socket_message(self, event = None, msg = None, data = None):
        # This method requires a valid flask request
        try:
                    
            sioServer = current_app.extensions["sioServer"]

            with current_app.app_context():                
                sioServer.emit(event, {
                    "msg": msg,
                    "data": json.dumps(data)
                })

            create_log(type="ALERT", message=f"Sent message through local socket [{ event } - { msg }]")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not sent message through local socket [{ event } - { msg }] [{ e }]")