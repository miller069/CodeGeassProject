#ifndef NETWORK_H
#define NETWORK_H

// allows the use of strings
#include <string>

// Network class used to start the server, receive requests, send messages, and stop the server
class Network {
private:

    // Stores the server socket file descriptor
    int server_fd;

    // Stores the most recently connected client socket
    int client_socket;

public:

    // Constructor for the Network class; creates a network object
    Network();

    // Starts the game server
    void startServer();

    // function that waits for a request from a player/client
    std::string receiveRequest();

    // sends a message back to the client
    void sendMessage(std::string message);

    // sends completed game results to the Python platform server
    void sendResultsToPython(std::string session_result);

    // Stops the server
    void stopServer();
};

#endif