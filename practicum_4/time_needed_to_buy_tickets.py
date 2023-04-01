from typing import Any

import yaml
import numpy as np
from numpy.typing import NDArray

from src.common import ProblemCase


class Queue:
    """FIFO queue implemented using an array with circular order.
    This is also known as ring buffer
    """

    def __init__(self, max_n: int, dtype: Any) -> None:
        self._array: NDArray = np.zeros((max_n,), dtype=dtype)  # internal array
        self._head_i: int = 0  # index of the head of the array
        # (the oldest element in the array)
        self._tail_i: int = 0  # index of the next location at
        # which a newly arriving element will be inserted into the queue

    def empty(self) -> bool:
        return self._head_i == self._tail_i

    def enqueue(self, x: Any) -> None:
        """Insert an element to the queue
        Complexity: O(1)
        """
        if self._head_i == self._increment_according_to_circular_order(self._tail_i):
            raise QueueOverflowException("Queue is already full")

        self._array[self._tail_i] = x
        self._tail_i = self._increment_according_to_circular_order(self._tail_i)

    def dequeue(self) -> Any:
        """Remove an element from the queue
        Complexity: O(1)
        """
        if self.empty():
            raise QueueUnderflowException("Queue is already empty")

        x = self._array[self._head_i]
        self._head_i = self._increment_according_to_circular_order(self._head_i)
        return x

    def _increment_according_to_circular_order(self, i: int) -> int:
        if i == len(self._array) - 1:  # last element
            i = 0
        else:
            i += 1
        return i


class QueueUnderflowException(BaseException):
    pass


class QueueOverflowException(BaseException):
    pass


def time_taken(tickets: list[int], k: int) -> int:
    q = Queue(max_n=100, dtype=int)
    for t in tickets:
        q.enqueue(t)
    seconds_elapsed = 0
    while not q.empty():
        t = q.dequeue()
        if t != 1:
            q.enqueue(t - 1)
        seconds_elapsed += 1
    return seconds_elapsed


if __name__ == "__main__":
    # Let's solve Time Needed to Buy Tickets problem from leetcode.com:
    # https://leetcode.com/problems/time-needed-to-buy-tickets/
    # Here we show a toy solution which does not make use of k and simply returns
    # the number of seconds the whole queue spent to disappear.
    # It should be modified to solve the original problem (and it can be solved without a queue)
    with open("practicum_4/time_needed_to_buy_tickets_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = time_taken(tickets=c["input"]["tickets"], k=c["input"]["k"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
