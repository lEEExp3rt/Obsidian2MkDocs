"""
Obsidian2MkDocs module: utils/algorithm

This module includes some algorithms for the conversion process.

:author: !EEExp3rt
:date: 2025-02-02
"""


def merge_intervals(origin: str) -> str:
    """
    Merge the hightlight intervals into 1 big interval with order and no duplicates.            

    :param origin: The original highlight intervals in `string` format, e.g. "1-3,2,5,4,7"
    :return: The merged highlight intervals, e.g. "1-5 7"
    """
    
    striped = origin.split(',') # Split the intervals, e.g. ["1-3", "2", "5", "4", "7"].
    intervals = [[int(i), int(i)] if i.isdigit() else [int(i.split('-')[0]), int(i.split('-')[1])] for i in striped] # Convert the intervals to tuple.

    # Sort the intervals by start position.
    intervals.sort(key=lambda x: x[0]) 

    # Merge the intervals.
    merged = []
    current = intervals[0]
    for interval in intervals[1:]:
        if interval[0] <= current[1] + 1: # Merge the intervals.
            current[1] = max(current[1], interval[1])
        else: # Add the current interval to the output.
            merged.append(current)
            current = interval
    merged.append(current) # Add the last interval to the output.

    # Convert the merged intervals to string.
    output = ""
    for interval in merged:
        if interval[0] == interval[1]: # Single line highlight.
            output += str(interval[0]) + " "
        else: # Multi-line highlight.
            output += str(interval[0]) + "-" + str(interval[1]) + " "

    return output[:-1]
