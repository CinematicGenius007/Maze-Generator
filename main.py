import random
import sys


class Maze:
    def __init__(self):
        self.maze = None
        self.rows = 0
        self.cols = 0
        self.num_of_nodes_in_graph = 0

    @staticmethod
    def minKey(key, mst_set, vertices):
        min_index = -1
        _min = sys.maxsize

        for v in range(vertices):
            if key[v] < _min and not mst_set[v]:
                _min = key[v]
                min_index = v

        return min_index

    @staticmethod
    def primMST(vertices, graph):
        # Key values used to pick minimum weight edge in cut
        key = [sys.maxsize] * vertices
        parent = [-1] * vertices  # Array to store constructed MST
        # Make key 0 so that this vertex is picked as first vertex
        key[0] = 0
        mst_set = [False] * vertices

        for _ in range(vertices):
            u = Maze.minKey(key, mst_set, vertices)
            mst_set[u] = True
            for v in range(vertices):
                if 0 < graph[u][v] < key[v] and not mst_set[v]:
                    key[v] = graph[u][v]
                    parent[v] = u
        
        return parent

    def generate_maze(self):
        x = (self.rows - 1) // 2
        y = (self.cols - 1) // 2

        self.num_of_nodes_in_graph = x * y

        adjacencyMatrix = [[0 for _ in range(self.num_of_nodes_in_graph)] for _ in range(self.num_of_nodes_in_graph)]

        for i in range(x):
            for j in range(y):
                if i + 1 < x:
                    adjacencyMatrix[y * i + j][y * (i + 1) + j] = random.randint(1, self.num_of_nodes_in_graph * 10)
                if i - 1 >= 0:
                    adjacencyMatrix[y * i + j][y * (i - 1) + j] = random.randint(1, self.num_of_nodes_in_graph * 10)
                if j - 1 >= 0:
                    adjacencyMatrix[y * i + j][y * i + j - 1] = random.randint(1, self.num_of_nodes_in_graph * 10)
                if j + 1 < y:
                    adjacencyMatrix[y * i + j][y * i + j + 1] = random.randint(1, self.num_of_nodes_in_graph * 10)

        path = Maze.primMST(self.num_of_nodes_in_graph, adjacencyMatrix)

        self.maze = [[0] * self.cols]

        start = random.randint(0, x - 1)
        end = random.randint(0, x - 1)

        for i in range(x * 2 - 1):
            row = []
            for j in range(y * 2 - 1):
                if j == 0:
                    if i // 2 == start and i % 2 == 0:
                        row.append(1)
                    else:
                        row.append(0)
                if i % 2 == 0 and j % 2 == 0:
                    row.append(1)
                elif i % 2 == 0:
                    if path[(i // 2) * y + ((j + 1) // 2)] == (i // 2) * y + ((j - 1) // 2) \
                            or path[(i // 2) * y + ((j - 1) // 2)] == (i // 2) * y + ((j + 1) // 2):
                        row.append(1)
                    else:
                        row.append(0)
                else:
                    if j % 2 == 0 \
                            and (
                            path[((i - 1) // 2) * y + (j // 2)] == ((i + 1) // 2) * y + (j // 2)
                            or path[((i + 1) // 2) * y + (j // 2)] == ((i - 1) // 2) * y + (j // 2)):
                        row.append(1)
                    else:
                        row.append(0)
                if j == y * 2 - 2:
                    if i // 2 == end and i % 2 == 0:
                        row.append(1)
                    else:
                        row.append(0)
            self.maze.append(row)

        if self.rows % 2 != 0:
            self.maze.append([0] * self.cols)
        else:
            self.maze.append([0] * self.cols)
            self.maze.append([0] * self.cols)

        if self.cols % 2 == 0:
            for i in range(self.rows - 1):
                if len(maze[i]) != self.cols:
                    self.maze[i].append(self.maze[i][-1])

    def take_input_for_maze(self):
        try:
            user_input = list(map(int, input("Enter the size of the maze: ").split(" ")))
            if len(user_input) == 2:
                self.rows = max(user_input[0], 5)
                self.cols = max(user_input[1], 5)
            else:
                self.rows = max(user_input[0], 5)
                self.cols = max(user_input[0], 5)
        except ValueError:
            print("Invalid input. Please enter only numbers.\n")
            self.take_input_for_maze()

    def traverse_maze_dfs(self, _x, _y, vertical=0, horizontal=0):
        if _y == len(self.maze[_x]) - 1:
            self.maze[_x][_y] = -1
            return True

        if _x == 0 or _x == len(self.maze) - 1:
            return False

        if _x > 0 and self.maze[_x - 1][_y] == 1 and vertical != -1 and self.traverse_maze_dfs(_x - 1, _y, vertical=1):
            self.maze[_x][_y] = -1
            return True

        if _x < len(self.maze) - 1 and self.maze[_x + 1][_y] == 1 and vertical != 1 and self.traverse_maze_dfs(_x + 1, _y, vertical=-1):
            self.maze[_x][_y] = -1
            return True

        if _y < len(self.maze[_x]) - 1 and self.maze[_x][_y + 1] == 1 and horizontal != -1 and self.traverse_maze_dfs(_x, _y + 1, horizontal=1):
            self.maze[_x][_y] = -1
            return True

        if _y - 1 > 0 and self.maze[_x][_y - 1] == 1 and horizontal != 1 and self.traverse_maze_dfs(_x, _y - 1, horizontal=-1):
            self.maze[_x][_y] = -1
            return True

        return False


    def traverse_maze(self):
        print("\nTraversing...")
        start_index = 1
        for i in range(len(self.maze)):
            if self.maze[i][0] == 1:
                start_index = i
                break

        if not self.traverse_maze_dfs(start_index, 0):
            print("Didn't find any path")
        else:
            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    if self.maze[i][j] == 1:
                        print("  ", end="")
                    elif self.maze[i][j] == -1:
                        print("//", end="")
                        self.maze[i][j] = 1
                    else:
                        print("\u2588\u2588", end="")
                print()
            print()


    def print_maze(self):
        for i in self.maze:
            for j in i:
                if j == 1:
                    print("  ", end="")
                else:
                    print("\u2588\u2588", end="")
            print()
        print()


    def write_maz_to_file(self, file):
        try:
            with open(file, 'w', encoding='utf-8') as file:
                for i in self.maze:
                    for j in range(len(i)):
                        if j != len(i) - 1:
                            file.write(f"{i[j]},")
                        else:
                            file.write(f"{i[j]}")
                    file.write("\n")
        except OSError as e:
            print(e)


    def read_maze(self, file):
        self.maze = []
        try:
            with open(file, 'r') as file:
                for line in file.readlines():
                    self.maze.append(list(map(int, line.replace("\n", "").split(","))))
        except OSError as e:
            print("The file ... does not exist\n")
        if len(self.maze) == 0:
            self.maze = None
            print("The file ... does not exist\n")


    def print_menu(self):
        print("=== Menu ===")
        print("1. Generate a new maze")
        print("2. Load a maze")
        if self.maze:
            print("3. Save the maze")
            print("4. Display the maze")
            print("5. Find the escape")
        print("0. Exit")


if __name__ == '__main__':
    maze = Maze()
    while True:
        maze.print_menu()
        option = int(input("Option: "))

        if option == 0:
            print("Bye!")
            break
        elif option == 1:
            maze.take_input_for_maze()
            maze.generate_maze()
            maze.print_maze()
        elif option == 2:
            file_name = input("File name: ").strip()
            maze.read_maze(file_name)
            maze.print_maze()
        elif maze.maze:
            if option == 3:
                file_name = input("File name: ").strip()
                maze.write_maz_to_file(file_name)
            elif option == 4:
                maze.print_maze()
            elif option == 5:
                maze.traverse_maze()
        else:
            print("Incorrect option. Please try again")
        print()


