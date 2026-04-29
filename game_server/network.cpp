// network.cpp
// April 27th 2026
// Ryan Miller (Code Geass)


// includes class definition from network.h
#include "network.h"

// allows input and output to the terminal
#include <iostream>

// allows the use of a standard library without writing 'std::'
using namespace std;


// Constructor for the Network class; creates a network object
Network::Network() {
    
}


// Starts the game server
void Network::startServer() {

    // Prints a message showing the server has started
    cout << "Game server started." << endl;
}


// function that waits for a request from a player/client
string Network::receiveRequest() {

    string request;

    // prompts the user to enter a request
    cout << "Enter player request: ";
    getline(cin, request);      // reads the request from the terminal

    // Returns the request string to the server 
    return request;
}


// sends a message back to the client
void Network::sendMessage(string message) {

    // prints the message to the terminal
    cout << "Sending message: " << message << endl;   // displays teh message being sent
}


// sends completed game results to the Python platform server
void Network::sendResultsToPython(string session_result) {

    // Prints the result message to simulate sending it
    cout << "Sending session results to Python server: " << session_result << endl;
}


// Stops the server
void Network::stopServer() {

    // Prints a message showing the server has stopped
    cout << "Game server stopped." << endl;
}