/*
text_serializer.cpp - Text serialization implementation

Author: [Student Name]
Date: [Date]
*/

#include "text_serializer.h"

std::string TextSerializer::serialize(const Player& player) {
    std::ostringstream oss;
        oss << player.get_id() << "|"
            << player.get_name() << "|"
            << player.get_x() << "|"
            << player.get_y() << "|"
            << player.get_socket();
        return oss.str();
    
    // TODO: Implement text serialization
    // Format: "id|name|x|y|socket"
    // Example: "1|Alice|400.5|300.2|5"
    
    // Approach:
    // 1. Use std::ostringstream to build the string
    // 2. Get each field from the player using getter methods
    // 3. Separate fields with the pipe character '|'
    // 4. Convert numbers to strings (ostringstream handles this automatically)
    // 5. Return the complete string
    
 // Placeholder
}

Player TextSerializer::deserialize(const std::string& data) {
    // TODO: Implement text deserialization
    // Input format: "id|name|x|y|socket"
    // Example: "1|Alice|400.5|300.2|5"
    
    // Approach:
    // 1. Use std::istringstream to parse the string
    // 2. Use std::getline with '|' as delimiter to extract each field
    // 3. Convert string fields to appropriate types:
    //    - std::stoi for integers
    //    - std::stof for floats
    //    - strings cdstay as strings
    // 4. Create and return a new Player object with the parsed values
    std::istringstream iss(data);
        std::string variable;

        int id, socket;
        std::string name;
        float x, y;

        std::getline(iss, variable, '|'); id = std::stoi(variable);
        std::getline(iss, name, '|');
        std::getline(iss, variable, '|'); x = std::stof(variable);
        std::getline(iss, variable, '|'); y = std::stof(variable);
        std::getline(iss, variable, '|'); socket = std::stoi(variable);
        return Player(id, name, x, y, socket);
  // Placeholder
}

std::string TextSerializer::getName() const {
    return "Text";
}