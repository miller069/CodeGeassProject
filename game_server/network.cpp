// network.cpp
// April 27th 2026
// Ryan Miller (Code Geass)


// includes class definition from network.h
#include "network.h"

// allows input and output to the terminal
#include <iostream>

// allows the use of strings
#include <string>

// allows clearing memory buffers
#include <cstring>

// allows closing sockets on Linux
#include <unistd.h>

// allows internet address functions
#include <arpa/inet.h>

// allows socket functions
#include <sys/socket.h>

// allows the use of a standard library without writing 'std::'
using namespace std;


// Constructor for the Network class; creates a network object
Network::Network() {

    // Initializes the server socket as not created yet
    server_fd = -1;

    // Initializes the client socket as not connected yet
    client_socket = -1;
}


// Starts the game server
void Network::startServer() {

    // Port number that players/clients will connect to
    int port = 8080;

    // Creates a TCP socket for the server
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    // Checks if the socket was created successfully
    if (server_fd == -1) {
        cerr << "Error creating socket." << endl;
        return;
    }

    // Allows the server to reuse the port after restarting
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // Stores the server address information
    sockaddr_in address;

    // Uses IPv4
    address.sin_family = AF_INET;

    // Allows connections from any available network interface
    address.sin_addr.s_addr = INADDR_ANY;

    // Converts the port number to network byte order
    address.sin_port = htons(port);

    // Binds the socket to the IP address and port
    if (bind(server_fd, (sockaddr*)&address, sizeof(address)) < 0) {
        cerr << "Bind failed." << endl;
        return;
    }

    // Starts listening for incoming client connections
    if (listen(server_fd, 25) < 0) {
        cerr << "Listen failed." << endl;
        return;
    }

    // Prints a message showing the server has started
    cout << "Game server started on port " << port << "." << endl;
}


// function that waits for a request from a player/client
string Network::receiveRequest() {

    // Stores information about the connecting client
    sockaddr_in client_address;
    socklen_t client_len = sizeof(client_address);

    // Prints a message showing the server is waiting for a player/client
    cout << "Waiting for player/client request..." << endl;

    // Accepts one incoming client connection
    client_socket = accept(server_fd, (sockaddr*)&client_address, &client_len);

    // Checks if the client connection was accepted successfully
    if (client_socket < 0) {
        cerr << "Accept failed." << endl;
        return "";
    }

    // Stores the incoming message from the client
    char buffer[1024] = {0};

    // Receives data from the connected client
    int bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);

    // Checks if data was actually received
    if (bytes_received <= 0) {
        close(client_socket);
        return "";
    }

    // Converts the received character buffer into a string request
    string request(buffer);

    // Prints the received request to the terminal
    cout << "Received player request: " << request << endl;

    // Returns the request string to the server
    return request;
}


// sends a message back to the client
void Network::sendMessage(string message) {

    // Sends the message back to the most recently connected client
    send(client_socket, message.c_str(), message.length(), 0);

    // Closes the client connection after sending the response
    close(client_socket);

    // prints the message to the terminal
    cout << "Sending message: " << message << endl;
}


// sends completed game results to the Python platform server
void Network::sendResultsToPython(string session_result) {

    // Prints the result message to simulate sending it
    cout << "Sending session results to Python server: " << session_result << endl;
}


// Stops the server
void Network::stopServer() {

    // Closes the server socket if it was opened
    if (server_fd != -1) {
        close(server_fd);
    }

    // Prints a message showing the server has stopped
    cout << "Game server stopped." << endl;
}