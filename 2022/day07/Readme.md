# --- Day 7: No Space Left On Device ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/7](https://adventofcode.com/2022/day/7)

Part 1:
The problem presents a file system which is represented as a list of commands and their outputs. The commands that are used to navigate and understand the file system are 'cd' and 'ls'. The 'cd' command is used to change directory and move between different directories in the file system. The 'cd x' command moves into the directory named 'x' inside the current directory, 'cd ..' moves up one level to the parent directory of the current directory, and 'cd /' moves to the outermost directory '/'. The 'ls' command is used to list the contents of the current directory, including files and directories immediately contained by the current directory.

The problem statement gives an example of the file system and asks you to understand the structure of the file system using the commands and the output.

Since the disk is full and the goal is to free up space, the task is to find all the directories in the file system that have a total size of at most 100000. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly, and not to be confused with the size of the directory itself.

The task is to go through the file system, use the given commands and understand the structure of the file system, then calculate the total size of each directory and find the directories that have a total size of at most 100000. Finally, calculate the sum of total sizes of those directories and return that value.


In Part 2 of the problem, the task is to find the smallest directory that if deleted, would free up enough space to run a system update on a filesystem. The available disk space is 70000000 and the update requires at least 30000000 unused space. The total size of used space is given as 48381165, which means that the size of the unused space is currently 21618835, which is not sufficient to run the update. The solution requires finding a directory that when deleted would increase the unused space by at least 8381165. The prompt provides an example solution of finding all directories above 100000, and choosing the smallest among them to increase the unused space on the filesystem to run the update. The prompt wants you to find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?