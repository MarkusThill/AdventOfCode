# --- Day 22: Monkey Map ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/22](https://adventofcode.com/2022/day/22)

Part 1:

The problem is about a path that you have to trace on a board. The board is represented by a grid of open tiles (.) and solid walls (#). The path is described by a sequence of alternating numbers and letters. Each number represents the number of tiles to move in the direction you are facing, while each letter represents the direction to turn (90 degrees clockwise or counterclockwise). You start at the leftmost open tile of the top row facing right. If a movement instruction would take you off of the board, you wrap around to the other side of the board. The goal is to determine the final row, column and facing, and calculate the final password as the sum of 1000 times the row, 4 times the column, and the facing.

Part 2:

In the second part of the problem, the board is now a large cube with six square faces of 50x50 tiles. Each face is represented by a small grid. The starting position and facing are the same as before, but the wrapping rules are different. Now if you would walk off the board, you instead proceed around the cube. Walls still block your path, even if they are on a different face of the cube. The final password is still calculated from your final position and facing from the perspective of the map. The task is to fold the map into a cube and follow the path given in the monkeys' notes.

## Rough Solution Sketch

The `fold_cube` function takes in a 2D array called flat_cube, which represents a flattened version of a cube, as well as two optional parameters n and visited. The function's purpose is to take this flattened version of the cube and fold it into a 3D cube, such that each face of the cube is represented by a 2D matrix.

The function starts by initializing some variables such as the number of sides in the cube, and matrices that will be used for rotating the cube. It then checks if the input parameter n has been visited before, and if not, it adds it to the visited set. If all sides have been visited, the function returns the folded cube.

Otherwise, the function proceeds to loop through all the possible directions (right, left, down, up) and for each direction, it applies a corresponding rotation matrix to the current side of the cube and then moves the side to its new location. This process is repeated for all the possible directions.

Finally, the function returns a dictionary where each key represents a side of the cube, and its corresponding value is a 2D matrix representing that side.


The function `find_side_neighbor` is used to find the neighboring side of a given side in the folded cube. It takes in three inputs:

`folded_cube`: a dictionary containing the folded cube, where each key is an integer representing the side number, and the value is a numpy matrix representing the contents of that side.
`side`: an integer representing the side of the folded cube for which the neighboring side is to be found.
`direction`: a string representing the direction of the side for which the neighboring side is to be found. The options are: "south", "west", "east" and "north".
It first checks if the input side exists in the folded cube and if the input direction is valid. It then defines a dictionary `col_idx` which contains the indices of the columns of the matrix representing the side that correspond to the specified direction. It then iterates over all the sides of the folded cube and for each side it compares the columns of the matrix corresponding to the specified direction with the columns of the matrix of the current side corresponding to all the directions in the all_directions list. If there is a match, it adds the current side as a neighbor of the input side. If there is no match, it moves on to the next side. The function returns the neighboring side and a boolean value indicating if the elements in the neighboring side need to be reversed or not.

The function `find_all_side_neighbors` takes in the folded cube as input and calls the find_side_neighbor function for each side and each direction to find all the neighboring sides of the cube. It returns a dictionary with keys as sides and values as another dictionary where keys are the direction and values are the neighboring side in that direction.

The function `check_all_neighbors` takes in two input dictionaries, `d1` and `d2`, containing the neighboring sides of a folded cube and compares the values of the two dictionaries. If the values of the two dictionaries are the same, it returns `true`, else it returns `false`.


`map_coords_to_simple_flat_cube_idx(i, j, side_length, sfc)`: This function maps the coordinates `(i, j)` of a point on a cube to its corresponding index on a 2D representation of the cube (a "simple flat cube"). The input i and j are the row and column coordinates of the point on the cube, `side_length` is the length of one side of the cube, and sfc is the 2D representation of the cube. The function returns the index of the point on the simple flat cube by dividing the row and column coordinates by the side length and returning the corresponding element of sfc.


`reverse_direction(direction)`: Given a string direction that represents a cardinal direction, this function returns the opposite direction. This function uses a list of directions and a mapping of each direction to the next direction in the list.

`build_graph(padded_lines, part=1, all_neighbors=None, simple_flat_cube=None, side_length=None)`: This function takes in a 2D array padded_lines which represents a cube, and creates a graph data structure of the cube, where each element in the cube is a node in the graph, and the nodes are connected to their neighbors. The function has a parameter part (default 1) that can be used to specify whether this is for part 1 or part 2 of the problem. When part is 2, the function also takes in a dict `all_neighbors`, a 2D array `simple_flat_cube`, and an int `side_length` as inputs.

The function starts by creating a 2D array `G` with the same shape as `padded_lines`, and for each element in `padded_lines` that is not a space, it creates a Node object and assigns it to the corresponding element in `G`. Next, for each Node object in `G`, the function connects the node to its neighbors (nodes in the north, south, east and west direction) by adding the neighbors to the neighbors attribute of the node. If a neighbor is not found due to the cube being on an edge case, the function will find the adjacent node that is on the opposite side of the edge.

For part 2, the function also maps each node to its corresponding index on the 2D representation of the cube (simple flat cube) using the `map_coords_to_simple_flat_cube_idx` function. Then the function uses the mapping of the side and the direction provided by all_neighbors to make adjustments to the row and column indexes of the node when moving from one side of the cube to another.


`walk_graph` function takes a starting node `n`, a list of instructions and an initial direction. The instructions consist of a combination of integers and strings. Integers represent the number of steps to take in the current direction, and strings represent a change of direction ("L" for left, "R" for right). The function uses a helper function `step()` to move from one node to the next one based on the current direction. The helper function `get_change_direction_map()` returns a dictionary that maps the current direction to the new direction after a left or right turn. `walk_graph` returns the row and column of the final node, as well as the final direction.

`input_to_simple_flat_cube` is used to transform the input, which is a list of strings, into a simplified version of the cube, where each side of the cube is represented by a single integer. The function takes in the padded lines of input and the side length of each side of the cube. It creates an empty array called `S` that will be used to store the simplified cube. Then it iterates through the input array and for each non-empty side of the cube, assigns it a unique number and stores it in the `S` array.

