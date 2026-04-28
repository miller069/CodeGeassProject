// main.cpp
// April 27th 2026
// Ryan Miller (Code Geass)



#include <iostream>                 // Includes input/output tools for printing messages
#include "game_instance_manager.h"  // Includes the session manager that controls all game sessions
#include "network.h"                // Includes the networking system used to receive and send messages

// allows the use of a standard library without writing 'std::'
using namespace std;


// Main function where the game server starts running
int main() {

    // Creates the networking system used for communication
    Network network;

    // Creates the session manager that controls all game sessions
    GameInstanceManager manager;

    // Starts the game server
    network.startServer();

    // Variable used to store incoming player requests
    string request;

    // Simple loop to keep the server running
    while (true) {

        // Wait for a player request
        request = network.receiveRequest();

        // If the request is "quit", stop the server
        if (request == "quit") {

            network.stopServer();
            break;
        }

        // For now we simply send a response back to the client
        network.sendMessage("Request received: " + request);
    }

    return 0;
}