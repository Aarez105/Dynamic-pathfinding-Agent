import heapq
import math

def heuristic(a, b, heuristic_type):
    if heuristic_type == "manhattan":
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    else:
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_neighbors(node, grid, rows, cols):
    r, c = node
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == 0:
                neighbors.append((nr, nc))

    return neighbors

def run_search(grid_obj, heuristic_type, algorithm):
    start = grid_obj.start
    goal = grid_obj.goal
    grid = grid_obj.grid
    rows = grid_obj.rows
    cols = grid_obj.cols

    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    g_cost = {start: 0}
    visited = set()

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return came_from, g_cost[goal], visited

        for neighbor in get_neighbors(current, grid, rows, cols):
            tentative_g = g_cost[current] + 1

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g

                if algorithm == "gbfs":
                    f = heuristic(neighbor, goal, heuristic_type)
                else:
                    f = tentative_g + heuristic(neighbor, goal, heuristic_type)

                heapq.heappush(open_list, (f, neighbor))

    return None, None, visited
