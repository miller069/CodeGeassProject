/*
position_smoother.h - Position smoothing using circular buffer

Smooths network position updates by averaging recent positions.
Reduces visual jitter with minimal added latency.

Author: [Your Name]
Date: [Date]
Project: Project 2 - Network Position Buffering
*/

#ifndef POSITION_SMOOTHER_H
#define POSITION_SMOOTHER_H

#include "circular_buffer.h"
#include "position.h"  // Position struct
#include <cmath>

/**
 * Position smoother using averaging strategies
 * 
 * Inherits from CircularBuffer to store recent positions.
 * Provides different averaging strategies to smooth movement.
 */
class PositionSmoother : public CircularBuffer<Position> {
public:
    /**
     * Constructor
     * 
     * @param buffer_size Number of recent positions to keep (default: 5)
     */
    PositionSmoother(int buffer_size = 5) : CircularBuffer<Position>(buffer_size) {
    };
    
    /**
     * Add a new position to the buffer
     * 
     * @param x X coordinate
     * @param y Y coordinate
     * @param timestamp Time when position was received (optional)
     */
void add_position(float x, float y, long timestamp = 0) {
    Position p;
    p.x = x;
    p.y = y;
    p.timestamp = timestamp;

    
    if (count < capacity) {    
        this->enqueue(p);     
    }
    else {
        this->dequeue();
        this->enqueue(p);
    }
};
    
        



    /**
     * Get simple average of all positions in buffer
     * 
     * Averages all positions equally (each has same weight).
     * 
     * @return Averaged position
     * @throws std::runtime_error if buffer is empty
     */
    Position get_simple_average() const {
        if (count == 0)
            throw std::runtime_error("Buffer empty");

        float sum_x = 0;
        float sum_y = 0;

        for (int i = 0; i < count; i++) {
            int index = (head + i) % capacity;
            sum_x += buffer[index].x;
            sum_y += buffer[index].y;
        }

        Position avg;
        avg.x = sum_x / count;
        avg.y = sum_y / count;
        avg.timestamp = 0;

        return avg;
    }
    
    /**
     * Get weighted average - recent positions weighted more heavily
     * 
     * Oldest position gets weight 1, next gets weight 2, ..., newest gets weight N.
     * This makes recent positions matter more than old positions.
     * 
     * Example with 3 positions:
     *   Oldest (index 0): weight 1
     *   Middle (index 1): weight 2
     *   Newest (index 2): weight 3
     *   Total weight: 1 + 2 + 3 = 6
     *   Weighted avg = (pos0*1 + pos1*2 + pos2*3) / 6
     * 
     * @return Weighted averaged position
     * @throws std::runtime_error if buffer is empty
     */
    Position get_weighted_average() const {
        
        if (count == 0)
            throw std::runtime_error("Buffer empty");

        float sum_x = 0;
        float sum_y = 0;
        float total_weight = 0;

        for (int i = 0; i < count; i++) {

            int index = (head + i) % capacity;

            int weight = i + 1;

            sum_x += buffer[index].x * weight;
            sum_y += buffer[index].y * weight;

            total_weight += weight;
        }

        Position avg;
        avg.x = sum_x / total_weight;
        avg.y = sum_y / total_weight;
        avg.timestamp = 0;

        return avg;
    };

    
    /**
     * Get exponentially smoothed position (bonus)
     * 
     * Uses exponential moving average formula:
     *   smoothed = alpha * newest + (1-alpha) * previous_smoothed
     * 
     * Higher alpha = more responsive (follows new positions quickly)
     * Lower alpha = more smooth (changes slowly)
     * 
     * @param alpha Smoothing factor (0.0 to 1.0, default 0.3)
     * @return Exponentially smoothed position
     * @throws std::runtime_error if buffer is empty
     */
    Position get_exponential_smooth(float alpha = 0.3f) const {

        if (count == 0)
            throw std::runtime_error("Buffer empty");

    
        int index = head;
        float exp_x = buffer[index].x;
        float exp_y = buffer[index].y;

    
        for (int i = 1; i < count; i++) {

            index = (head + i) % capacity;

            exp_x = alpha * buffer[index].x + (1 - alpha) * exp_x;
            exp_y = alpha * buffer[index].y + (1 - alpha) * exp_y;
        }

        Position result;
        result.x = exp_x;
        result.y = exp_y;
        result.timestamp = 0;

        return result;
    };
    Position get_latest() const {
        if (count == 0)
            throw std::runtime_error("Buffer empty");

        int newest = (tail - 1 + capacity) % capacity;

            return buffer[newest];
    };
    
    /**
     * Calculate current variance/jitter in the buffer
     * 
     * Useful for measuring how much positions are jumping around.
     * Higher variance = more jitter.
     * 
     * @return Standard deviation of positions
     */
    float get_variance() const {
    if (count == 0)
            return 0;

        Position mean = get_simple_average();

        float variance = 0;

        for (int i = 0; i < count; i++) {

            int index = (head + i) % capacity;

            float dx = buffer[index].x - mean.x;
            float dy = buffer[index].y - mean.y;

            variance += dx * dx + dy * dy;
        }

        variance /= count;

        return std::sqrt(variance);
    };
};

#endif // POSITION_SMOOTHER_H