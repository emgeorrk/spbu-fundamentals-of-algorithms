from typing import Any

import yaml
import numpy as np


def time_taken(tickets: list[int], k: int) -> int:
    seconds_elapsed = tickets[k]
    # как минимум время потратится на покупку билетов k-го человека

    # если человек стоит в очереди раньше k-го, то он успеет купить tickets[k] билетов
    # раньше, чем это сделает k-й
    # если человек стоит после k-го, то он успеет купить tickets[k]-1 билетов
    for x in range(len(tickets)):
        if x < k:
            seconds_elapsed += min(tickets[x], tickets[k])
        if x > k:
            seconds_elapsed += min(tickets[x], tickets[k] - 1)

    return seconds_elapsed


if __name__ == "__main__":
    # Let's solve Time Needed to Buy Tickets problem from leetcode.com:
    # https://leetcode.com/problems/time-needed-to-buy-tickets/
    with open("practicum_4/time_needed_to_buy_tickets_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = time_taken(tickets=c["input"]["tickets"], k=c["input"]["k"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
