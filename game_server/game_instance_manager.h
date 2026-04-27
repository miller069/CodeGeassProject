// game_instance_manager.h
// April 27th 2026
// Ryan Miller (Code Geass)


// used to prevent including the file multiple times during compilation
#ifndef GAME_INSTANCE_MANAGER_H
#define GAME_INSTANCE_MANAGER_H

// string library, to include player IDs, Game IDs, etc; also includes game_sesion header file
#include <string>
#include "game_session.h"

#define MAX_SESSIONS 100


// Manages all active game sessions on the C++ game server
class GameInstanceManager {

private:

    // Stores all game sessions currently known by the server
    GameSession sessions[MAX_SESSIONS];

    // Keeps track of how many sessions have been created
    int session_count;

    // Creates a simple session ID using the session count
    std::string createSessionId();


public:

    // Constructor initializes the manager with zero active sessions
    GameInstanceManager();

    // Routes a player to a game session and returns the session index
    int routePlayer(std::string player_id, std::string game_id);

    // Removes a player from a specific session
    void removePlayer(int session_index, std::string player_id);

    // Updates a player's score in a specific session
    void updateScore(int session_index, std::string player_id, int score);

    // Ends a specific session
    void endSession(int session_index);

    // Returns the number of sessions being tracked
    int getSessionCount();

    // Returns a session by index
    GameSession getSession(int index);
};

#endif