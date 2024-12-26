import requests
import heapq

# 抓取數據
def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# 第十八天 給你一堆障礙物 問你從左上走到右下最短距離 保證定可以走到 Dijkstra
def day_eighteen_part1(matrix, lines):
        cnt = 0
        for line in lines:
            if cnt < 1024:
                print(line)
                x, y = line.split(",")
                matrix[int(x)][int(y)] = "#"
                cnt += 1
        # 看地圖狀況
        # for row in matrix:
        #     print("".join(row))
        priority_queue = []
        
        minDist = [[1000000] * 71 for _ in range(71)]
        heapq.heappush(priority_queue, (0, 0, 0))  # (dist, x, y)
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        while priority_queue:
            dist, x, y = heapq.heappop(priority_queue)
            if minDist[x][y] <= dist:
                continue
            minDist[x][y] = dist
            if x == 70 and y == 70:
                return dist

            for dirx, diry in dirs:
                nx, ny = x + dirx, y + diry
                nxtDist = dist + 1
                if nx < 0 or ny < 0 or nx >= 71 or ny >= 71 or matrix[nx][ny] == "#" or minDist[nx][ny] <= nxtDist:
                    continue
                heapq.heappush(priority_queue, (nxtDist, nx, ny))
        return -1


# part2 想問說一堆障礙物 加到哪個確定無法從左上走到右下
def dijkstra(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    minDist = [[float('inf')] * cols for _ in range(rows)]
    prev = [[None] * cols for _ in range(rows)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    priority_queue = [(0, start[0], start[1])]  # (dist, x, y)
    minDist[start[0]][start[1]] = 0

    while priority_queue:
        dist, x, y = heapq.heappop(priority_queue)
        if minDist[x][y] < dist:
            continue
        for dirx, diry in dirs:
            nx, ny = x + dirx, y + diry
            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] != "#":
                nxtDist = dist + 1
                if nxtDist < minDist[nx][ny]:
                    minDist[nx][ny] = nxtDist
                    prev[nx][ny] = (x, y)
                    heapq.heappush(priority_queue, (nxtDist, nx, ny))
    return minDist[end[0]][end[1]], prev


def reconstruct_path(prev, start, end):
    path = []
    current = end
    while current and current != start:
        path.append(current)
        current = prev[current[0]][current[1]]
    if current == start:
        path.append(start)
        return path[::-1] #反轉reverse 但其實也不用轉 用set包就好
    return None


def day_eighteen_part2(matrix, obstacles):
    for i in range(1024):
        x, y = map(int, obstacles[i].split(","))
        matrix[x][y] = "#"

    dist, prev = dijkstra(matrix, (0, 0), (70, 70))
    if dist == float('inf'):
        return "Initial 1024 obstacles already block the path!"

    # 從右下角回溯最短路徑
    path = set(reconstruct_path(prev, (0, 0), (70, 70)))

    # 添加剩餘障礙物並檢查是否阻斷路徑
    for i in range(1024, len(obstacles)):
        x, y = map(int, obstacles[i].split(","))
        if (x, y) in path:
            # 如果障礙物在最短路徑上，重新計算路徑
            matrix[x][y] = "#"
            dist, prev = dijkstra(matrix, (0, 0), (70, 70))
            if dist == float('inf'):
                return f"First blocking obstacle: {x},{y}"
            path = set(reconstruct_path(prev, (0, 0), (70, 70)))
        else:
            # 如果障礙物不影響最短路徑，直接加入矩陣
            matrix[x][y] = "#"

    return "All obstacles added without blocking the path!"



if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/18/input'
    input_data = fetch_data_from_url(url)
    lines = input_data.splitlines()
    print(lines)
    matrix = [['.']*71 for _ in range(71)]
    print(day_eighteen_part1(matrix, lines))
    matrix = [['.'] * 71 for _ in range(71)]
    result = day_eighteen_part2(matrix, lines)
    print(result)

