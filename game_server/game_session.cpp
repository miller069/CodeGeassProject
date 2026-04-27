// game_session.cpp
// April 27th 2026
// Ryan Miller (Code Geass)
// This file runs functions that execute for when a new session is created, adds and removes players, updates players scores, 
// returns player lists, returns a scoreboard, marks matches as finished, checks for running sessions.


#include "game_session.h"

#include <algorithm> // used for removing players from vector


// Constructor initializes session values and sets session as active
GameSession::GameSession(std::string session_id, std::string game_id) {
    this->session_id = session_id;
    this->game_id = game_id;
    active = true;
}


// Adds a player to the session
void GameSession::addPlayer(std::string player_id) {
    players.push_back(player_id);

    // initialize player's score to 0
    scores[player_id] = 0;
}


// Removes a player from the session
void GameSession::removePlayer(std::string player_id) {

    // remove player from players vector
    players.erase(
        std::remove(players.begin(), players.end(), player_id),
        players.end()
    );

    // remove player score
    scores.erase(player_id);
}


// Updates the score for a specific player
void GameSession::updateScore(std::string player_id, int score) {

    if (scores.find(player_id) != scores.end()) {
        scores[player_id] = score;
    }
}


// Returns list of players in the session
std::vector<std::string> GameSession::getPlayers() {
    return players;
}


// Returns all scores for the session
std::map<std::string, int> GameSession::getScores() {
    return scores;
}


// Ends the game session
void GameSession::endSession() {
    active = false;
}


// Returns whether the session is still active
bool GameSession::isActive() {
    return active;
}