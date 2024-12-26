import requests
import heapq


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# part1要從S走到E 問你最少cost是多少
# part2 要問走的路徑可以是哪些點 可以用一個array去紀錄走的過程 然後用set去重
def day_sixteen_part1(matrix, startx, starty, endx, endy):
    # 紀錄每個點 他的走向與是否走過該點 (x,y,dir) 
    '''
        0
    3       1
        2
    '''
    m, n = len(matrix), len(matrix[0])
    minDist = [[[float('inf')]*4 for _ in range(n)] for _ in range(m)]
    dirs = [(-1,0), (0,1),(1,0), (0,-1)] # URDL
    priority_queue = []
    heapq.heappush(priority_queue, (0,startx, starty, 1))

    while priority_queue:
        dist, x, y, dir = heapq.heappop(priority_queue)
        if minDist[x][y][dir] <= dist:
            continue
        minDist[x][y][dir] = dist
        if x == endx and y == endy:
            print("part1",dist)
            return dist

        for i,(dirx, diry) in enumerate(dirs):
            if i == dir:
                nx = x + dirx
                ny = y + diry
                nxt_dist = dist + 1
            else:
                nx = x
                ny = y
                nxt_dist = dist + 1000 * min(abs(i - dir), 4 - abs(i - dir))
            if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] != "#":
                if minDist[nx][ny][i] <= nxt_dist:
                    continue
                heapq.heappush(priority_queue, (nxt_dist, nx, ny, i))
    return -1
def day_sixteen_part2(matrix, startx, starty, endx, endy):
    # 紀錄每個點 他的走向與是否走過該點 (x,y,dir, path) 
    '''
        0
    3       1
        2
    '''
    m, n = len(matrix), len(matrix[0])
    minDist = [[[float('inf')] * 4 for _ in range(n)] for _ in range(m)]
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # URDL
    priority_queue = []
    heapq.heappush(priority_queue, (0, startx, starty, 1, [(startx, starty)]))
    paths = []
    while priority_queue:
        dist, x, y, dir, path = heapq.heappop(priority_queue)

        if minDist[x][y][dir] < dist:
            continue
        minDist[x][y][dir] = dist
        if x == endx and y == endy and minDist[x][y][dir] == dist:
            paths.append(path)
            continue
        
        for i, (dirx, diry) in enumerate(dirs):
            if i == dir:  
                nx, ny = x + dirx, y + diry
                nxt_dist = dist + 1
            else:
                nx, ny = x, y
                nxt_dist = dist + 1000 * min(abs(i - dir), 4 - abs(i - dir))

            if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] != "#":
                if minDist[nx][ny][i] < nxt_dist:
                    continue
                heapq.heappush(priority_queue, (nxt_dist, nx, ny, i, path + [(nx, ny)]))

    # print("走過的點:", paths)
    visited_set = set()
    for i in range(len(paths)):
        for x,y in paths[i]:
            visited_set.add((x,y))
    print("part2", len(visited_set))

if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/16/input'
    input_data = fetch_data_from_url(url)
    matrix = input_data.splitlines()
    startx = 0
    starty = 0
    endx = 0
    endy = 0
    for i,row in enumerate(matrix):
        for j, ch in enumerate(row):
            if ch == 'S':
                startx, starty = i, j
            if ch == 'E':
                endx, endy = i, j
    day_sixteen_part1(matrix, startx, starty, endx, endy)
    day_sixteen_part2(matrix, startx, starty, endx, endy)

    