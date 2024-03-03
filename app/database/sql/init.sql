/*
********************************************************

    Tento kód je součástí projektu 'Na Lovu'.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


-- 
-- TABLES
--

-- Table to store questions
CREATE TABLE questions (
  questionId INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT,
  correctAnswerId INT
);

-- Table to store answers
CREATE TABLE answers (
  answerId INTEGER PRIMARY KEY AUTOINCREMENT,
  questionId INTEGER,
  type TEXT,
  text TEXT
);

-- Table to store players
CREATE TABLE players (
  role TEXT PRIMARY KEY DEFAULT "PLAYER",
  name TEXT
);

-- Table to store player's answers
CREATE TABLE playersAnswers (
  playerAnswerId INTEGER PRIMARY KEY AUTOINCREMENT,
  questionId INTEGER,
  pickedAns INTEGER,
  role TEXT DEFAULT "PLAYER"
);

-- Table to store config information
CREATE TABLE config (
  currentState TEXT DEFAULT "INTRO",
  currentQuestionId INTEGER,
  answerTime INTEGER
);

-- Table to store answered questions
CREATE TABLE answeredQuestions (
  answeredQuestionId INTEGER PRIMARY KEY AUTOINCREMENT,
  questionId INTEGER
);


-- 
-- INITIAL VALUES
--
INSERT INTO players (role) VALUES ("player");

INSERT INTO players (role) VALUES ("chaser");

INSERT INTO config (currentState, answerTime) VALUES ("INTRO", 5);
