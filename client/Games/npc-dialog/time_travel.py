"""
time_travel.py - Time travel (rewind / replay) system using two stacks

History stack:
    holds past states (oldest -> ... -> newest/top)

Future stack:
    holds states you rewound from (for replay)

Author: Ibrahim Chatila
Lab: Lab 4 - Time Travel with Stacks
"""

from datastructures.stack import Stack


class TimeTravel:
    def __init__(self, max_history=180):
        # max_history = how many frames/states we keep
        self.max_history = max_history
        self.history = Stack()
        self.future = Stack()

        # track last recorded position so we don't spam duplicates
        self._last_state = None

    def record_state(self, x, y):
        """
        Record the current (x, y) position into history.

        Rules:
        - Don't record duplicates back-to-back.
        - If we've rewound (future not empty) and then move normally,
          we clear the future (new timeline).
        - Keep only the most recent max_history states.
        """
        state = (x, y)

        # ignore exact duplicate consecutive states
        if self._last_state == state:
            return

        # if player moved after rewinding, kill the redo history
        if self.can_replay():
            self.future.clear()

        self.history.push(state)
        self._last_state = state

        # enforce history limit (drop oldest)
        if self.max_history is not None and self.max_history > 0:
            while self.history.size() > self.max_history:
                self._drop_oldest_history_state()

    def _drop_oldest_history_state(self):
        """
        Helper: remove the bottom/oldest element from history.
        Stack only pops from top, so we use a temp stack to rotate.
        """
        temp = Stack()

        # move everything to temp (reverses order)
        while not self.history.is_empty():
            temp.push(self.history.pop())

        # temp's top is the oldest from history, drop it
        if not temp.is_empty():
            temp.pop()

        # move back to history (restore order)
        while not temp.is_empty():
            self.history.push(temp.pop())

        # update last_state to new top (or None)
        if self.history.is_empty():
            self._last_state = None
        else:
            self._last_state = self.history.peek()

    def can_rewind(self):
        # need at least 2 states to go "back" to something different
        return self.history.size() > 1

    def can_replay(self):
        return not self.future.is_empty()

    def rewind(self):
        """
        Go back one frame:
        - pop current from history -> push to future
        - return the new current (top of history)
        """
        if not self.can_rewind():
            return None

        current = self.history.pop()
        self.future.push(current)

        new_current = self.history.peek()
        self._last_state = new_current
        return new_current

    def replay(self):
        """
        Go forward one frame:
        - pop from future -> push to history
        - return that state (now current)
        """
        if not self.can_replay():
            return None

        state = self.future.pop()
        self.history.push(state)

        self._last_state = state
        return state

    def get_history_size(self):
        return self.history.size()

    def get_future_size(self):
        return self.future.size()

    def clear(self):
        self.history.clear()
        self.future.clear()
        self._last_state = None
