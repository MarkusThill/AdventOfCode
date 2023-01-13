# --- Day 10: Cathode-Ray Tube ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/10](https://adventofcode.com/2022/day/10)

Part 1:

In this programming problem, you need to simulate a cathode-ray tube screen and simple CPU which is driven by a precise clock circuit. The clock circuit ticks at a constant rate; each tick is called a cycle. The CPU has a single register, X, which starts with the value 1. It supports only two instructions: addx V and noop. "addx V" takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.) "noop" takes one cycle to complete and has no other effect. The goal is to understand the signal being sent by the CPU and analyze it by looking at the value of the X register throughout execution. The task requires to compute the signal strength (the cycle number multiplied by the value of the X register) during the 20th cycle and every 40 cycles after that (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).

In part 2 of the problem, you are to continue simulating the cpu program from part 1. Now the CPU's register X is also controlling the horizontal position of a sprite which is 3 pixels wide on a screen that is 40 pixels wide and 6 pixels tall. The CPU's instruction and the CRT's drawing operations need to be timed properly to determine whether the sprite is visible during each cycle of drawing. The end result is the rendering of an image which has 8 capital letters that need to be identified by solving the problem.