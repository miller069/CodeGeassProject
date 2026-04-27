// game_session.h
// April 27th 2026
// Ryan Miller (Code Geass)



// used to prevent including the file multiple times during compilation
#ifndef GAME_SESSION_H
#define GAME_SESSION_H

// string library, to include player IDs, Game IDs, etc
#include <string>

#define MAX_PLAYERS 50


// class definition for GameSession; represnts one multiplayer session
class GameSession {

// can only be used in this class [encapsulation]    
private:

    // stores the ID of the session, should be uniqe
    std::string session_id;

    // used to stores ID of game being played
    std::string game_id;

    // Array used for storing players in the session
    std::string players[MAX_PLAYERS];

    // Array storing player scores
    int scores[MAX_PLAYERS];

    // Current number of players in the session
    int player_count;

    // Indicates whether the session is active
    bool active;


// allows other parts of the program to call these 
public:

    // constructor creates new GameSession and initializes its values
    GameSession(std::string session_id, std::string game_id);

    // Adds a player to the session
    void addPlayer(std::string player_id);

    // Removes a player from the session
    void removePlayer(std::string player_id);

    // Updates score of a player
    void updateScore(std::string player_id, int score);

    // Returns the number of players currently in the sesion 
    int getPlayerCount();

    // Returns a player at a spec positoin in array
    std::string getPlayer(int index);

    // Returns a player's score at spec position
    int getScore(int index);

    // Ends the session
    void endSession();

    // Checks if session is active
    bool isActive();
};

#endif