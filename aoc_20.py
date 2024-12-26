import requests
from queue import Queue
from collections import deque
from typing import Generator

import copy

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# part1 可以選擇最多一次機會作弊撞牆 但是只能最多維持兩秒 問說作弊的方法可以節省至少100的方法數有多少種 也就是跟原本方法差100ms x,y,0 or1 走到x,y 使用過0 or 1次作弊方法需花的時間
'''
1. 是否用過撞牆機制 -> 是 就乖乖走 看要走多久，否看能否在上下左右使用
2. 用了之後 判斷是往上下左右使用，對應不同的其餘三個方向 三個方向需有一個是free space 才能用
3. 走到某點如果是已經走過的狀態 可以直接記憶化他需要的步數，並且需判斷是0 or 1 狀態，這塊我覺得可以先跑一個不能作弊的算法 得知他最短路徑會怎麼走
'''

# 以下function是尚未重構的版本
def day_twenty_part1(matrix):
    m = len(matrix)
    n = len(matrix[0])
    startx, starty, endx, endy = 0, 0, 0, 0
    for i, row in enumerate(matrix):
        for j, ch in enumerate(row):
            if ch == 'S':
                startx, starty = i, j
            if ch == 'E':
                endx, endy = i, j

    # 找出 no_cheet 每個位置的最短到終點距離
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 右邊 左邊 下面 上面
    
    def no_cheet_bfs(x, y):
        q = Queue()
        q.put((x,y,0))
        pure_visited = [[False] * n for _ in range(m)]
        while not q.empty():
            curx, cury, dist = q.get()
            if pure_visited[curx][cury]:
                continue
            pure_visited[curx][cury] = True
            if curx == endx and cury == endy:
                return dist
            for dirx, diry in dirs:
                nx, ny = curx + dirx, cury + diry
                if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] != '#' and not pure_visited[nx][ny]:
                    q.put((nx,ny, dist+1))
        return -1
    x, y = startx, starty
    # no_cheet_shortest_path = no_cheet_bfs(x, y)
    no_cheet_path = [[float('inf')] * n for _ in range(m)]
    for i, row in enumerate(matrix):
        for j, ch in enumerate(row):
            if ch != '#':
                no_cheet_path[i][j] = no_cheet_bfs(i,j)
    no_cheet_shortest_path = 9484
   
    def bfs(x,y):
        ret = 0
        q = Queue()
        q.put((x,y,0,0)) # x,y, dist, 是否用過，用過了多少條路
        visited = [[False] * n for _ in range(m)] # 走到i,j 並且狀態是0 or 1 是否已經有過
        cheat_visited = set()
        while not q.empty():
            curx, cury, dist, used = q.get()
            if curx == endx and cury == endy:
                break
            if visited[curx][cury] and used == 0:
                continue
            elif not visited[curx][cury] and used == 0:
                visited[curx][cury] = True

            for i,(dirx, diry) in enumerate(dirs):
                nx, ny = curx + dirx, cury + diry
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and matrix[nx][ny] != '#':
                    q.put((nx,ny, dist+1, used))
                elif 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] == '#' and used <= 20:
                    if i == 0:
                        if ny + 1 < n and matrix[nx][ny+1] != '#' and (nx, ny, nx, ny+1) not in cheat_visited and not visited[nx][ny+1] and dist + 2 + no_cheet_path[nx][ny+1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny+1))
                            ret += 1
                            # q.put((nx, ny+1, dist+2, 1))
                        if nx + 1 < m and matrix[nx+1][ny] != '#' and (nx, ny, nx+1, ny) not in cheat_visited and not visited[nx+1][ny] and dist + 2 + no_cheet_path[nx+1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx+1, ny))
                            ret += 1
                            # q.put((nx+1, ny, dist+2, 1))
                        if nx - 1 >= 0 and matrix[nx-1][ny] != '#' and (nx, ny, nx-1, ny) not in cheat_visited and not visited[nx-1][ny] and dist + 2 + no_cheet_path[nx-1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx-1, ny))
                            ret += 1
                            # q.put((nx-1, ny, dist+2, 1))
                    elif i == 1:
                        if ny - 1 >= 0 and matrix[nx][ny-1] != '#' and (nx, ny, nx, ny-1) not in cheat_visited and not visited[nx][ny-1] and dist + 2 + no_cheet_path[nx][ny-1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny-1))
                            ret += 1
                            # q.put((nx, ny-1, dist+2, 1))
                        if nx + 1 < m and matrix[nx+1][ny] != '#' and (nx, ny, nx+1, ny) not in cheat_visited and not visited[nx+1][ny] and dist + 2 + no_cheet_path[nx+1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx+1, ny))
                            ret += 1
                            # q.put((nx+1, ny, dist+2, 1))
                        if nx - 1 >= 0 and matrix[nx-1][ny] != '#' and (nx, ny, nx-1, ny) not in cheat_visited and not visited[nx-1][ny] and dist + 2 + no_cheet_path[nx-1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx-1, ny))
                            ret += 1
                            # q.put((nx-1, ny, dist+2, 1))
                    elif i == 2:
                        if ny - 1 >= 0 and matrix[nx][ny-1] != '#' and (nx, ny, nx, ny-1) not in cheat_visited and not visited[nx][ny-1] and dist + 2 + no_cheet_path[nx][ny-1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny-1))
                            ret += 1
                            # q.put((nx, ny-1, dist+2, 1))
                        if ny + 1 < n and matrix[nx][ny+1] != '#' and (nx, ny, nx, ny+1) not in cheat_visited and not visited[nx][ny+1] and dist + 2 + no_cheet_path[nx][ny+1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny+1))
                            ret += 1
                            # q.put((nx, ny+1, dist+2, 1))
                        if nx + 1 < m and matrix[nx+1][ny] != '#' and (nx, ny, nx+1, ny) not in cheat_visited and not visited[nx+1][ny] and dist + 2 + no_cheet_path[nx+1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx+1, ny))
                            ret += 1
                            # q.put((nx+1, ny, dist+2, 1))
                    else:
                        if ny - 1 >= 0 and matrix[nx][ny-1] != '#' and (nx, ny, nx, ny-1) not in cheat_visited and not visited[nx][ny-1] and dist + 2 + no_cheet_path[nx][ny-1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny-1))
                            ret += 1
                            # q.put((nx, ny-1, dist+2, 1))
                        if ny + 1 < n and matrix[nx][ny+1] != '#' and (nx, ny, nx, ny+1) not in cheat_visited and not visited[nx][ny+1] and dist + 2 + no_cheet_path[nx][ny+1] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx, ny+1))
                            ret += 1
                            # q.put((nx, ny+1, dist+2, 1))
                        if nx - 1 >= 0 and matrix[nx-1][ny] != '#' and (nx, ny, nx-1, ny) not in cheat_visited and not visited[nx-1][ny] and dist + 2 + no_cheet_path[nx-1][ny] <= no_cheet_shortest_path - 100: 
                            cheat_visited.add((nx, ny, nx-1, ny))
                            ret += 1
                            # q.put((nx-1, ny, dist+2, 1))
        print(ret)
    bfs(startx, starty)

Grid = list[list[str]]
Position = tuple[int, int]
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def find_point(grid: Grid, type: str) -> Position:
    return next(find_points(grid, type))


def find_points(grid: Grid, type: str) -> Generator[Position, None, None]:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                yield row, col


def calculate_distances(
    grid: Grid,
    start_row: int,
    start_col: int,
    walls: set[Position],
) -> dict[Position, int]:
    distances: dict[Position, int] = {}
    queue = deque([(start_row, start_col, 0)])
    seen = set() | walls

    while queue:
        r, c, dist = queue.popleft()

        distances[(r, c)] = dist

        for dr, dc in DIRECTIONS:
            new_r, new_c = r + dr, c + dc

            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and (new_r, new_c) not in seen
            ):
                seen.add((r, c))
                queue.append((new_r, new_c, dist + 1))

    return distances


def find_possible_shortcuts(
    grid: Grid,
    distances_from_start: dict[Position, int],
    distances_to_end: dict[Position, int],
    walls: set[Position],
    regular_time: int,
    max_cheat_time: int,
) -> list[int]:
    savings = []
    rows, cols = len(grid), len(grid[0])

    for start_r in range(rows):
        for start_c in range(cols):
            if (start_r, start_c) in walls:
                continue

            for end_r in range(
                max(0, start_r - max_cheat_time),
                min(rows, start_r + max_cheat_time + 1),
            ):
                for end_c in range(
                    max(0, start_c - max_cheat_time),
                    min(cols, start_c + max_cheat_time + 1),
                ):
                    if (end_r, end_c) in walls:
                        continue

                    manhattan_dist = abs(end_r - start_r) + abs(end_c - start_c)
                    if manhattan_dist > max_cheat_time:
                        continue

                    total_time = (
                        distances_from_start[(start_r, start_c)]
                        + manhattan_dist
                        + distances_to_end[(end_r, end_c)]
                    )

                    if total_time < regular_time:
                        savings.append(regular_time - total_time)

    return savings


def find_cheats(
    grid: Grid,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int,
    walls: set[Position],
    max_cheat_time: int = 2,
) -> list[int]:
    distances_from_start = calculate_distances(grid, start_row, start_col, walls)
    distances_to_end = calculate_distances(grid, end_row, end_col, walls)

    regular_time = distances_from_start[(end_row, end_col)]

    return find_possible_shortcuts(
        grid,
        distances_from_start,
        distances_to_end,
        walls,
        regular_time,
        max_cheat_time,
    )



def day_twenty_part2(grid) -> int:
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")
    walls = set(find_points(grid, "#"))

    savings = find_cheats(
        grid, start_row, start_col, end_row, end_col, walls, max_cheat_time=20
    )

    return sum(1 for saving in savings if saving >= 100)

if __name__ == "__main__":
    # 測試輸入
    url = 'https://adventofcode.com/2024/day/20/input'
    input_data = fetch_data_from_url(url)
    matrix = [list(line) for line in input_data.splitlines()]
    print(day_twenty_part2(matrix))
    


