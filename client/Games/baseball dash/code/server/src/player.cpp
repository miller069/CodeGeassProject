/*
player.cpp - Player class implementation

Students implement all methods here.

Author: Nicholas Waller
Date: [Date]
*/

#include "player.h"

// Default constructor
Player::Player() {
    // TODO: Initialize all member variables to default values
    // Default values: id=0, name="", x=400.0, y=300.0, socket=-1, connected=false
    id = 0;             
    name = "";    
    x = 400.0f; 
    y = 300.0f;          
    socket = -1;         
    connected = false; 
}
// Parameterized constructor
Player::Player(int id, std::string name, float x, float y, int socket) {
    // TODO: Initialize all member variables with provided values
    // Remember to set connected=true for a newly connected player
    //p2(42, "Alice", 100.5f, 200.3f, 5);
    this->id = id;
    this->name = name;
    this->x = x;
    this->y = y;
    this->socket = socket;
    this->connected = true;
}

// Destructor
Player::~Player() {
    // TODO: Clean up if needed
    // Note: For this class, there's nothing to clean up
}

// Getters
int Player::get_id() const {
    // TODO: Return the player's ID
    return id;  // Placeholder
}

std::string Player::get_name() const {
    // TODO: Return the player's name
    return name;  // Placeholder
}

float Player::get_x() const {
    // TODO: Return the player's x coordinate
    return x;  // Placeholder
}

float Player::get_y() const {
    // TODO: Return the player's y coordinate
    return y;  // Placeholder
}

int Player::get_socket() const {
    // TODO: Return the player's socket file descriptor
    return socket;  // Placeholder
}

bool Player::is_connected() const {
    // TODO: Return the player's connection status
    return connected;  // Placeholder
}

// Setters
void Player::set_position(float new_x, float new_y) {
    // TODO: Update the player's x and y coordinates
    x = new_x;
    y = new_y;
}

void Player::set_name(std::string new_name) {
    // TODO: Update the player's name
    name = new_name;
}

void Player::set_connected(bool status) {
    // TODO: Update the player's connection status
    connected = status;
}

void Player::set_socket(int sock) {
    // TODO: Update the player's socket file descriptor
    socket = sock;
}

// Equality operator
bool Player::operator==(const Player& other) const {
    // TODO: Compare two players by their ID
    // Return true if IDs are equal, false otherwise
    if (id == other.id) {
        return true;
    } else {
        return false;
    }  // Placeholder
}

Player alice(1, "Alice", 400.5f, 300.2f, 5);