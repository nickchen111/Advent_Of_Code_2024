import requests
from collections import defaultdict
from datetime import datetime
from queue import Queue
from collections import defaultdict,deque


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第十二天 面積就是所有數字的出現頻率
    url = 'https://adventofcode.com/2024/day/12/input'
    input_data = fetch_data_from_url(url)
    matrix = []
    for line in input_data.strip().split("\n"):
        row = list(line)
        matrix.append(row)
    m = len(matrix)
    n = len(matrix[0])

    def day_twenlve_part1():
        def count_ans(i, j, visited):
            # 往右下去找找 並且每走一步就確認此點上下左右是否有不滿足的邊界 以及紀錄多少個點
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            para = 0
            area = 0
            curCh = matrix[i][j]
            q = Queue()
            q.put((i,j))
            while not q.empty():
                x, y = q.get()
                if visited[x][y]:
                    continue
                visited[x][y] = 1
                area += 1
                for dirx, diry in dirs:
                    nx = x + dirx
                    ny = y + diry

                    if nx < 0 or ny < 0 or nx >= m or ny >= n or matrix[nx][ny] != curCh:
                        para += 1
                    elif not visited[nx][ny]:
                        q.put((nx, ny))
            return area * para
        res = 0
        visited = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if visited[i][j]:
                    continue
                res += count_ans(i,j, visited)
        return res
    print(day_twenlve_part1())
    def day_twenlve_part2(url):
        time_start = datetime.now()
        def tuple_sum(a,b):
            return tuple([x + y for x, y in zip(a,b)])

        def create_grid(lines):
            grid = defaultdict(list)
            for r, line in enumerate(lines):
                for c, char in enumerate(line):
                    grid[char].append((r,c))
            return grid, len(lines), len(lines[0])

        def find_region_size_and_perimeter(coords):
            directions = [(-1, 0), (1,0), (0,-1), (0,1)] #UDlR
            queue = deque([coords[0]])
            visited = [coords[0]]
            while queue:
                current = queue.popleft()
                neighbours = [tuple_sum(direction, current) for direction in directions]
                for neighbour in neighbours:
                    if neighbour in coords and neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
            perimeter = 0
            # for coord in visited:
            #     neighbours = [tuple_sum(direction, coord) for direction in directions]
            #     neighbours = [neighbour for neighbour in neighbours if neighbour in visited]
            #     perimeter += 4 - len(neighbours)
            return visited, perimeter

        def scan_rows(start, finish, step, region):
            sides = 0
            used_cols = []
            for i in range(start, finish, step): #check cols from top to bottom ev. bottom to top
                row = list(filter(lambda coord: coord[0]==i, region)) #get all coords on i-th row
                _, cols = zip(*row) #get all column coords in i-th row
                groups = []
                for num in sorted(cols):
                    if not groups or num - groups[-1][-1] > 1: #if group is empty or differs by more than one
                        if num not in used_cols:
                            used_cols.append(num)
                            groups.append([num])
                    else:
                        if num not in used_cols:
                            used_cols.append(num)
                            groups[-1].append(num)
                used_cols = [col for col in cols]
                sides += len(groups)
            return sides

        def scan_cols(start, finish, step, region):
            sides = 0
            used_rows = []
            for i in range(start, finish, step): #check cols from left to right ev. right to left
                col = list(filter(lambda coord: coord[1]==i, region)) #get all coords on i-th col
                rows, _ = zip(*col) #get all row coords in i-th row
                groups = []
                for num in sorted(rows):
                    if not groups or num - groups[-1][-1] > 1: #if group is empty or differs by more than one
                        if num not in used_rows:
                            used_rows.append(num)
                            groups.append([num])
                    else:
                        if num not in used_rows:
                            used_rows.append(num)
                            groups[-1].append(num)
                used_rows = [col for col in rows]
                sides += len(groups)
            return sides

        def count_sides(region):
            r_s, c_s = zip(*region)
            min_r, max_r = min(r_s), max(r_s) #define borders of region
            min_c, max_c = min(c_s), max(c_s)
            sides = 0
            sides += scan_rows(min_r, max_r+1, 1, region) #scan from top to bottom
            sides += scan_rows(max_r, min_r-1, -1, region) #scan from bottom to top
            sides += scan_cols(min_c, max_c+1, 1, region) #scan from left to right
            sides += scan_cols(max_c, min_c-1, -1, region) #scan from  right to left
            return sides

        lines = fetch_data_from_url(url)
        lines = lines.splitlines()
        grid, max_r, max_c = create_grid(lines)

        price_part1 = 0
        price_part2 = 0
        for region in grid.keys():
            while len(grid[region]) > 0:
                visited, perimeter = find_region_size_and_perimeter(grid[region])
                grid[region] = [item for item in grid[region] if item not in visited]
                price_part1 += len(visited) * perimeter
                price_part2 += count_sides(visited) * len(visited)
        print("Part 1:", price_part1)
        print("Part 2:", price_part2)
        print("Total runtime:", datetime.now() - time_start)
    day_twenlve_part2(url)
    