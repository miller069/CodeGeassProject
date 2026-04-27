// Prevents the header file from being included multiple times during compilation
#ifndef GAME_SESSION_H
#define GAME_SESSION_H

// Standard libraries used for storing session information
#include <string>   // for session IDs, game IDs, and player IDs
#include <vector>   // for storing a list of players in the session
#include <map>      // for storing player scores mapped to player IDs


// Represents a single multiplayer game session and tracks its players and scores
class GameSession {

private:

    // Unique identifier for the session
    std::string session_id;

    // Identifier for the game being played
    std::string game_id;

    // List of players currently in the session
    std::vector<std::string> players;

    // Stores each player's score using their player ID as the key
    std::map<std::string, int> scores;

    // Indicates whether the session is still active
    bool active;


public:

    // Constructor that initializes a new game session with a session ID and game ID
    GameSession(std::string session_id, std::string game_id);

    // Adds a player to the session
    void addPlayer(std::string player_id);

    // Removes a player from the session
    void removePlayer(std::string player_id);

    // Updates the score for a specific player in the session
    void updateScore(std::string player_id, int score);

    // Returns the list of players currently in the session
    std::vector<std::string> getPlayers();

    // Returns all player scores for the session
    std::map<std::string, int> getScores();

    // Ends the session and marks it as inactive
    void endSession();

    // Returns whether the session is currently active
    bool isActive();
};


// End of the header guard
#endif