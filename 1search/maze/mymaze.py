import sys

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Stack:
    def __init__(self):
        self.nodes = []
    
    def push(self, node):
        self.nodes.append(node)

    def empty(self):
        return len(self.nodes) == 0

    def pop(self):
        if not self.empty():
            return self.nodes.pop()
        else:
            raise IndexError("Empty stack")

    def has(self, state):
        return any(node.state == state for node in self.nodes)

class Queue(Stack):
    def pop(self):
        if not self.empty():
            return self.nodes.pop(0)
        else:
            raise IndexError("Empty queue")

class Maze:
    def __init__(self, filename):
        with open(filename) as file:
            self.grid = file.read()
        
        # Making sure that the input has valid starting and end point
        if self.grid.count("A") != 1:
            raise ValueError("Invalid count of start (expected a single A)")
        if self.grid.count("B") != 1:
            raise ValueError("Invalid count of goal (expected a single B)")

        self.grid = self.grid.replace("#", "█")
        self.lines = self.grid.splitlines()

        for x, line in enumerate(self.lines):
            if "A" in line:
                self.start = (x, line.index("A"))
            if "B" in line:
                self.goal = (x, line.index("B"))
        
        self.height = len(self.lines)
        self.width = len(max(self.lines, key=len))

        self.solution = None    # Beacuse while the maze hasn't been solved we don't want to look for solution
    
    def is_wall(self, i, j):
        return self.lines[i][j] == "█"

    def connected(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.is_wall(r,c):
                result.append((action, (r, c)))
        return result

    def set_structure(self, using):
        if using == "DFS":
            return Stack()
        elif using == "BFS":
            return Queue()
        else:
            raise ValueError("Unexpected algorithm")
        
# • Start with a frontier that contains the initial state.
# • Start with an empty explored set.
# • Repeat:
#   • If the frontier is empty, then no solution.
#   • Remove a node from the frontier.
#   • If node contains goal state, return the solution.
#   • Add the node to the explored set.
#   • Expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set.
    def solve(self, using):
        frontier = self.set_structure(using)
        self.explored = set()
        self.explored_count = 0

        frontier.push(Node(self.start, None, None))

        while True:
            if frontier.empty():
                raise AssertionError("No solution")
            
            self.explored_count += 1
            current = frontier.pop()

            if current.state == self.goal:
                cells = []
                actions = []    # not necessary to keep a track, but we can see  the path followed
                while current.parent != None:
                    cells.append(current.state)
                    actions.append(current.action)
                    current = current.parent
                actions.reverse()   # Bactracking was used
                cells.reverse()
                self.solution = (action, cells)
                return

            self.explored.add(current.state)
            
            for action, state in self.connected(current.state):
                if state not in self.explored and not frontier.has(state):
                    frontier.push(Node(state, current, action))
    
    def display(self):
        is_solved = False
        if self.solution is not None:
            solution = self.solution[1]
            is_solved = True
        else:
            solution = None
        for i in range(self.height):
            for j in range(self.width):
                if self.is_wall(i, j):
                    print("█", end="")
                else:
                    if self.lines[i][j] == "A":
                        print("\033[31mA\033[0m", end="")
                    elif self.lines[i][j] == "B":
                        print("\033[32mB\033[0m" ,end="")
                    elif is_solved and (i, j) in solution:
                        print("\033[33m█\033[0m",end="")
                    elif is_solved and (i, j) in self.explored:
                        print("\033[31m█\033[0m", end="")
                    else:
                        print(" ", end="")
            print()


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None

        for i in range(self.height):
            for j in range(self.width):

                # Walls
                if self.is_wall(i, j):
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python3 maze.py maze.txt")

maze = Maze(sys.argv[1])
print("Maze:")
maze.display()
print("Solving...")
maze.solve(using="BFS")
print("States Explored:", maze.explored_count)
print("Solution:")
maze.display()
maze.output_image("maze.png", show_explored=True)
