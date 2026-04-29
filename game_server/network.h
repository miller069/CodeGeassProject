// network.h
// April 27th 2026
// Ryan Miller (Code Geass)

// used to prevent including the file multiple times during compilation
#ifndef NETWORK_H
#define NETWORK_H

// string library, to include player IDs, Game IDs, and also messagese
#include <string>


// Handles communication between the client, C++ game server, and Python platform server
class Network {

public:

    // Network() is the constructor used to create Network object
    Network();

    // Starts the game server
    void startServer();

    // Receives a request from a player or client
    std::string receiveRequest();

    // Sends a message back to a player or client
    void sendMessage(std::string message);

    // Sends completed game session results back to the Python platform server
    void sendResultsToPython(std::string session_result);

    // Stops the server
    void stopServer();
};


#endif