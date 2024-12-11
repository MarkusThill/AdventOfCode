# --- Day 2: Red-Nosed Reports ---

You can find the original problem statement here: [https://adventofcode.com/2024/day/2](https://adventofcode.com/2024/day/2)

## Part One
The task involves analyzing reactor reports to determine how many are "safe." Each report is a list of numerical levels. A report is considered safe if:

The levels are either all strictly increasing or all strictly decreasing.
The difference between any two adjacent levels is between 1 and 3 (inclusive).
For example, in the provided data, only 2 out of 6 reports meet these criteria.

## Part Two
A "Problem Dampener" allows the safety rules to tolerate one "bad level" per report. This means if removing one level makes an otherwise unsafe report safe, the report is now considered safe.

With this adjustment, more reports are classified as safe — 4 out of 6 in the example.


## Results
Part One: 585 reports are safe.
Part Two: With the Problem Dampener, 626 reports are safe.