import pygame
import random
from collections import deque

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS
DELAY_MS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver (Press B=🟦 BFS, D=🔴 DFS, K=🟢 Kruskal, R=Reset)")

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.walls = [True, True, True, True]
        self.visited = False

    def draw(self, win, color=WHITE):
        pygame.draw.rect(win, color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        if self.walls[0]: pygame.draw.line(win, BLACK, (self.x, self.y), (self.x + CELL_SIZE, self.y), 2)
        if self.walls[1]: pygame.draw.line(win, BLACK, (self.x + CELL_SIZE, self.y), (self.x + CELL_SIZE, self.y + CELL_SIZE), 2)
        if self.walls[2]: pygame.draw.line(win, BLACK, (self.x, self.y + CELL_SIZE), (self.x + CELL_SIZE, self.y + CELL_SIZE), 2)
        if self.walls[3]: pygame.draw.line(win, BLACK, (self.x, self.y), (self.x, self.y + CELL_SIZE), 2)

grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

def draw_maze():
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    pygame.display.update()

def draw_start_end(start, end):
    start.draw(win, ORANGE)
    end.draw(win, PURPLE)

def reset_maze_colors():
    draw_maze()
    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]
    draw_start_end(start, end)
    pygame.display.update()

def get_neighbors(cell):
    neighbors = []
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for i, (dr, dc) in enumerate(directions):
        r, c = cell.row + dr, cell.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            neighbors.append((grid[r][c], i))
    return neighbors

def generate_maze_backtracker():
    for row in grid:
        for cell in row:
            cell.visited = False
            cell.walls = [True, True, True, True]

    stack = []
    current = grid[0][0]
    current.visited = True
    while True:
        neighbors = [(n, d) for n, d in get_neighbors(current) if not n.visited]
        if neighbors:
            next_cell, direction = random.choice(neighbors)
            next_cell.visited = True
            stack.append(current)
            current.walls[direction] = False
            next_cell.walls[(direction + 2) % 4] = False
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break

def generate_maze_kruskal():
    for row in grid:
        for cell in row:
            cell.walls = [True, True, True, True]
    parent = {(r, c): (r, c) for r in range(ROWS) for c in range(COLS)}

    def find(pos):
        while parent[pos] != pos:
            parent[pos] = parent[parent[pos]]
            pos = parent[pos]
        return pos

    def union(a, b):
        parent[find(a)] = find(b)

    edges = []
    for r in range(ROWS):
        for c in range(COLS):
            if r + 1 < ROWS: edges.append(((r, c), (r + 1, c), 2))  
            if c + 1 < COLS: edges.append(((r, c), (r, c + 1), 1))  
    random.shuffle(edges)

    for (r1, c1), (r2, c2), dir in edges:
        if find((r1, c1)) != find((r2, c2)):
            union((r1, c1), (r2, c2))
            grid[r1][c1].walls[dir] = False
            grid[r2][c2].walls[(dir + 2) % 4] = False


def solve_bfs(start, end):
    queue = deque()
    queue.append(start)
    visited = {(start.row, start.col)}
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); 
                return
            #Handler tombol r
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_maze_colors()
                return

        if not done and queue:
            current = queue.popleft()

            if current == end:
                done = True
                print("BFS: Path found!")
            else:
                current.draw(win, GREEN)
                draw_start_end(start, end)
                pygame.display.update()
                pygame.time.delay(DELAY_MS)

                for i, (dr, dc) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                    if not current.walls[i]:
                        r, c = current.row + dr, current.col + dc
                        if 0 <= r < ROWS and 0 <= c < COLS:
                            if (r, c) not in visited:
                                visited.add((r, c))
                                queue.append(grid[r][c])
        elif done:
            #tunggu input untuk reset atau keluar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_maze_colors()
                    return

def solve_dfs(start, end):
    stack = [start]
    visited = {(start.row, start.col)}
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); 
                return
            #Handle tombol r
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_maze_colors()
                return

        if not done and stack:
            current = stack.pop()

            if current == end:
                done = True
                print("DFS: Path found!")
            else:
                current.draw(win, GREEN)
                draw_start_end(start, end)
                pygame.display.update()
                pygame.time.delay(DELAY_MS)

                for i, (dr, dc) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                    if not current.walls[i]:
                        r, c = current.row + dr, current.col + dc
                        if 0 <= r < ROWS and 0 <= c < COLS:
                            if (r, c) not in visited:
                                visited.add((r, c))
                                stack.append(grid[r][c])
        elif done:
            #tunggu input untuk reset atau keluar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_maze_colors()
                    return

def main():
    generate_maze_backtracker()
    draw_maze()
    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]
    draw_start_end(start, end)
    pygame.display.update()

    print("Controls:")
    print("B = BFS Algorithm")
    print("D = DFS Algorithm") 
    print("K = Generate new maze (Kruskal)")
    print("R = Reset maze colors")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print("Running BFS...")
                    solve_bfs(start, end)
                elif event.key == pygame.K_d:
                    print("Running DFS...")
                    solve_dfs(start, end)
                elif event.key == pygame.K_k:
                    print("Generating new maze...")
                    generate_maze_kruskal()
                    draw_maze()
                    draw_start_end(start, end)
                    pygame.display.update()
                elif event.key == pygame.K_r:
                    print("Resetting maze colors...")
                    reset_maze_colors()

if __name__ == "__main__":
    main()
