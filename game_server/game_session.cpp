// game_session.cpp
// April 27th 2026
// Ryan Miller (Code Geass)
// This file runs functions that execute for when a new session is created, adds and removes players, updates players scores, 
// returns player lists, returns a scoreboard, marks matches as finished, checks for running sessions.


// includes header file
#include "game_session.h"


// Default constructor that creates an empty and inactive session
GameSession::GameSession() {
    session_id = "";
    game_id = "";
    player_count = 0;
    active = false;

    for (int i = 0; i < MAX_PLAYERS; i++) {
        scores[i] = 0;
    }
}

// Constructor initializes session ID, game ID, player count, active status; creates a real session that can run
GameSession::GameSession(std::string session_id, std::string game_id) {
    this->session_id = session_id;
    this->game_id = game_id;
    this->player_count = 0; 
    this->active = true;

    // Initializes all scores to 0
    for (int i = 0; i < MAX_PLAYERS; i++) {
        scores[i] = 0;
    }
}


// Adds a player to the session if there is room for another player to be added
void GameSession::addPlayer(std::string player_id) {
    if (player_count < MAX_PLAYERS) {
        players[player_count] = player_id;
        scores[player_count] = 0;
        player_count++;
    }
}


// Removes a player from the session 
void GameSession::removePlayer(std::string player_id) {
    for (int i = 0; i < player_count; i++) {
        if (players[i] == player_id) {

            // Shift remaining players and scores left in array
            for (int j = i; j < player_count - 1; j++) {
                players[j] = players[j + 1];
                scores[j] = scores[j + 1];
            }

            player_count--;
            break;
        }
    }
}


// Updates the score for a specific player in session
void GameSession::updateScore(std::string player_id, int score) {
    for (int i = 0; i < player_count; i++) {
        if (players[i] == player_id) {
            scores[i] = score;
            break;
        }
    }
}

// ---- GETTER FUNCTIONS -----

// Returns the number of players in the session; needed to access this data for other parts of prgoram
int GameSession::getPlayerCount() {
    return player_count;
}


// Returns the player ID at a specific index; needed to access this data for other parts of prgoram
std::string GameSession::getPlayer(int index) {
    if (index >= 0 && index < player_count) {
        return players[index];
    }

    return "";
}


// Returns the score at a specific index; needed to access this data for other parts of prgoram
int GameSession::getScore(int index) {
    if (index >= 0 && index < player_count) {
        return scores[index];
    }

    return -1;
}


// Ends the session
void GameSession::endSession() {
    active = false;
}


// Returns whether the session is active
bool GameSession::isActive() {
    return active;
}