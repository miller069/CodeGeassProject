/*
json_serializer.cpp - JSON serialization implementation

Author: [Student Name]
Date: [Date]
*/

#include "json_serializer.h"

std::string JSONSerializer::serialize(const Player& player) {
    // TODO: Implement JSON serialization
    // Format: {"id":1,"name":"Alice","x":400.5,"y":200.2,"socket":5}
    
    // Approach:
    // 1. Build the JSON string manually using std::ostringstream
    // 2. Start with opening brace: {
    // 3. Add each field in the format: "fieldname":value
    //    - String values need quotes: "name":"Alice"
    //    - Numeric values don't need quotes: "id":1
    // 4. Separate fields with commas
    // 5. End with closing brace: }
    // 6. Return the complete string
    
    // Remember: You need to escape quotes in the string itself
    // Example: \" creates a quote character in the output
    
    std::ostringstream oss;
    oss << "{"
        << "\"id\":" << player.get_id() << ","
        << "\"name\":\"" << player.get_name() << "\","
        << "\"x\":" << player.get_x() << ","
        << "\"y\":" << player.get_y() << ","
        << "\"socket\":" << player.get_socket()
        << "}";
    return oss.str();  // Placeholder
}

Player JSONSerializer::deserialize(const std::string& data) {
    int id = extractInt(data, "id");
    std::string name = extractString(data, "name");
    float x = extractFloat(data, "x");
    float y = extractFloat(data, "y");
    int socket = extractInt(data, "socket");

    return Player(id, name, x, y, socket);
    // TODO: Implement JSON deserialization
    // Input format: {"id":1,"name":"Alice","x":400.5,"y":200.2,"socket":5}
    
    // Approach:
    // 1. Use the helper functions (extractInt, extractFloat, extractString)
    //    to parse each field from the JSON string
    // 2. Extract all required fields (id, name, x, y, socket)
    // 3. Create and return a new Player object with the extracted values
    
      // Placeholder
}

std::string JSONSerializer::getName() const {
    return "JSON";
}

// Helper function to extract integer from JSON
int JSONSerializer::extractInt(const std::string& json, const std::string& key) {
   
    // Approach:
    // 1. Build a search string: "key":
    // 2. Use json.find() to locate it in the JSON string
    // 3. Move position past the search string
    // 4. Find where the number ends (comma, }, or space)
    // 5. Extract the substring containing the number
    // 6. Convert to int using std::stoi
    // 7. Return the integer
    
    int pos = json.find("\"" + key + "\":");
    pos += key.length() + 3; 
    int end = json.find_first_of(",}", pos);
    return std::stoi(json.substr(pos, end - pos));
     // Placeholder
}

// Helper function to extract float from JSON
float JSONSerializer::extractFloat(const std::string& json, const std::string& key) {
    
    int pos = json.find("\"" + key + "\":");
    pos += key.length() + 3;
    int end = json.find_first_of(",}", pos);
    return std::stof(json.substr(pos, end - pos));
     // Placeholder
}

// Helper function to extract string from JSON
std::string JSONSerializer::extractString(const std::string& json, const std::string& key) {
  
    int pos = json.find("\"" + key + "\":\"");
    pos += key.length() + 4; 
    int end = json.find("\"", pos);
    return json.substr(pos, end - pos);
    // Approach:
    // 1. Build a search string: "key":"
    // 2. Use json.find() to locate it
    // 3. Move position past the search string
    // 4. Find the closing quote (marks end of string value)
    // 5. Extract substring between the quotes
    // 6. Return the extracted string
    
  // Placeholder
}