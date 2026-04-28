// game_instance_manager.cpp
// April 27th 2026
// Ryan Miller (Code Geass)


// Includes the class definitions for GameInstanceManager
#include "game_instance_manager.h"

// Allows string operations
#include <string>


// Constructor initializes the session manager
GameInstanceManager::GameInstanceManager() {

    // No sessions exist when the server starts, so auto starts at 0
    session_count = 0;
}


// Creates a session ID based on how many sessions exist by adding session_# (# of sessions)
std::string GameInstanceManager::createSessionId() {

    // ex; "session_3"
    return "session_" + std::to_string(session_count);
}


// Routes a player to a session for the selected game
int GameInstanceManager::routePlayer(std::string player_id, std::string game_id) {

    // First check if a session for this game already exists
    for (int i = 0; i < session_count; i++) {

        // If we find a session for this game and it is active
        if (sessions[i].isActive()) {

            // Add the player to that session
            sessions[i].addPlayer(player_id);

            // Return the session index
            return i;
        }
    }

    // If no session exists then we create a new one
    if (session_count < MAX_SESSIONS) {

        std::string new_id = createSessionId();

        // Create a new session in the array
        sessions[session_count] = GameSession(new_id, game_id);

        // Add the player to the new session
        sessions[session_count].addPlayer(player_id);

        // Increase the session count if a players added
        session_count++;

        // Return the new session index
        return session_count - 1;
    }

    // If the server is full, return -1
    return -1;
}


// Removes a player from a specific session
void GameInstanceManager::removePlayer(int session_index, std::string player_id) {

    // Make sure the session index is valid
    if (session_index >= 0 && session_index < session_count) {

        sessions[session_index].removePlayer(player_id);
    }
}


// Updates a player's score in a session
void GameInstanceManager::updateScore(int session_index, std::string player_id, int score) {

    // Make sure the session index is valid
    if (session_index >= 0 && session_index < session_count) {

        sessions[session_index].updateScore(player_id, score);
    }
}


// Ends a specific game session
void GameInstanceManager::endSession(int session_index) {

    // Make sure the session index is valid
    if (session_index >= 0 && session_index < session_count) {

        sessions[session_index].endSession();
    }
}


// Returns the total number of sessions
int GameInstanceManager::getSessionCount() {

    return session_count;
}


// Returns a specific session by index
GameSession GameInstanceManager::getSession(int index) {

    return sessions[index];
}