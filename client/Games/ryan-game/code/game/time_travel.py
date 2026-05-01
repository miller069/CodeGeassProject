"""
time_travel.py - Time travel system using stacks

Author: Ryan Miller
Date: 2/20/26
Lab: Lab 4 - Time Travel with Stacks
"""

from datastructures.stack import Stack


class GameState:
    """Stores player position at a given frame."""
    
    def __init__(self, player_x, player_y, timestamp):
        self.player_x = player_x
        self.player_y = player_y
        self.timestamp = timestamp
    
    def __repr__(self):
        return f"GameState(x={self.player_x:.1f}, y={self.player_y:.1f}, frame={self.timestamp})"


class TimeTravel:
    """
    Handles rewind/replay using two stacks:
    history = past states
    future = states after rewinding
    """
    
    def __init__(self, max_history=180, sample_rate=10):
        self.history = Stack()
        self.future = Stack()
        self.max_history = max_history
        self.sample_rate = sample_rate
        self.frame_counter = 0
        self.frames_since_last_record = 0
        self.rewinding = False
    
    def record_state(self, player_x, player_y):
        """Record position every N frames."""
        self.frames_since_last_record += 1

        if self.frames_since_last_record >= self.sample_rate:
            state = GameState(player_x, player_y, self.frame_counter)
            self.history.push(state)

            # keep history within limit
            while self.history.size() > self.max_history:
                temp = Stack()

                while not self.history.is_empty():
                    temp.push(self.history.pop())

                temp.pop()

                while not temp.is_empty():
                    self.history.push(temp.pop())

            self.future.clear()
            self.frames_since_last_record = 0

        self.frame_counter += 1
    
    def can_rewind(self):
        return self.history.size() >= 2
    
    def can_replay(self):
        return not self.future.is_empty()
    
    def rewind(self):
        if not self.can_rewind():
            return None

        self.rewinding = True
        self.future.push(self.history.pop())
        return self.history.peek()
    
    def replay(self):
        if not self.can_replay():
            return None

        state = self.future.pop()
        self.history.push(state)

        if self.future.is_empty():
            self.rewinding = False

        return state
    
    def get_history_size(self):
        return self.history.size()
    
    def get_future_size(self):
        return self.future.size()
    
    def clear(self):
        """Reset stored states."""
        self.history.clear()
        self.future.clear()
        self.frame_counter = 0
        self.frames_since_last_record = 0
        self.rewinding = False