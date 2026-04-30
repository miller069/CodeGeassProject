/*
position_smoother.cpp - Implementation of PositionSmoother class

Author: [Your Name]
Date: [Date]
Project: Project 2 - Network Position Buffering
*/

#include "position_smoother.h"
#include <stdexcept>
#include <cmath>

void PositionSmoother::add_position(float x, float y, long timestamp) {
    // TODO: Create a Position object with x, y, timestamp
    // TODO: Try to enqueue it
    // TODO: If buffer is full (enqueue returns false):
    //       - Dequeue the oldest position to make room
    //       - Then enqueue the new position
}

Position PositionSmoother::get_simple_average() const {
    // TODO: Check if buffer is empty
    // TODO: If empty, throw std::runtime_error("No positions to average")
    // TODO: Initialize sum_x = 0, sum_y = 0
    // TODO: Loop through all positions (use size() and get(i)):
    //       - sum_x += position.x
    //       - sum_y += position.y
    // TODO: Calculate average: avg_x = sum_x / size(), avg_y = sum_y / size()
    // TODO: Return Position(avg_x, avg_y)
    throw std::runtime_error("Not implemented");
}

Position PositionSmoother::get_weighted_average() const {
    // TODO: Check if buffer is empty
    // TODO: Initialize sum_x = 0, sum_y = 0, total_weight = 0
    // TODO: Loop through positions with index i from 0 to size()-1:
    //       - weight = i + 1 (oldest gets 1, newest gets size())
    //       - Position p = get(i)
    //       - sum_x += p.x * weight
    //       - sum_y += p.y * weight
    //       - total_weight += weight
    // TODO: Calculate weighted average:
    //       - avg_x = sum_x / total_weight
    //       - avg_y = sum_y / total_weight
    // TODO: Return Position(avg_x, avg_y)
    throw std::runtime_error("Not implemented");
}

Position PositionSmoother::get_exponential_smooth(float alpha) const {
    // BONUS: Implement exponential smoothing
    // TODO: Check if buffer is empty
    // TODO: Start with first position as initial smooth value
    // TODO: For each subsequent position:
    //       - smooth_x = alpha * pos.x + (1-alpha) * smooth_x
    //       - smooth_y = alpha * pos.y + (1-alpha) * smooth_y
    // TODO: Return final smoothed position
    throw std::runtime_error("Not implemented - bonus feature");
}

Position PositionSmoother::get_latest() const {
    // TODO: Check if empty
    // TODO: Return get(size() - 1)  (last/newest position)
    throw std::runtime_error("Not implemented");
}

float PositionSmoother::get_variance() const {
    if (is_empty()) {
        return 0.0f;
    }
    
    // Calculate mean
    Position mean = get_simple_average();
    
    // Calculate variance: average of squared distances from mean
    float sum_sq_dist = 0.0f;
    for (int i = 0; i < size(); i++) {
        Position p = get(i);
        float dx = p.x - mean.x;
        float dy = p.y - mean.y;
        sum_sq_dist += (dx*dx + dy*dy);
    }
    
    return std::sqrt(sum_sq_dist / size());
}
