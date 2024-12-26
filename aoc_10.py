import requests


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

#不能用set 去裝走過但失敗的路線
def dfs_ten_part1(x, y, visited, error_path) -> bool:
    if matrix[x][y] == '0' and (x,y) not in visited:
        visited.add((x,y))
        return 1
    elif matrix[x][y] == '0' and (x,y) in visited:
        return 0
    count = 0
    for dirx, diry in dirs:
        nx, ny = x + dirx, y + diry
        if 0 <= nx < m and 0 <= ny < n:
            if (int(matrix[x][y]) - int(matrix[nx][ny]) == 1):
                nxt = dfs_ten_part1(nx,ny, visited,error_path)
                count += nxt
                if nxt == 0:
                    error_path.add((nx,ny))
                
    return count

def day_ten_part1():
    cnt = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '9':
                visited = set()
                error_path = set()
                cnt += dfs_ten_part1(i,j, visited, error_path)
    return cnt

def dfs_ten_part2(x, y,error_path) -> bool:
    if matrix[x][y] == '9':
        return 1
    count = 0
    for dirx, diry in dirs:
        nx, ny = x + dirx, y + diry
        if 0 <= nx < m and 0 <= ny < n:
            if (int(matrix[nx][ny]) - int(matrix[x][y]) == 1):
                nxt = dfs_ten_part2(nx,ny,error_path)
                count += nxt
                if nxt == 0:
                    error_path.add((nx,ny))
                
    return count
# part2 主要是多個0可以走到多個9
def day_ten_part2():
    cnt = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '0':
                error_path = set()
                cnt += dfs_ten_part2(i,j,error_path)
    return cnt
if __name__ == "__main__":
    # 第十天 要從0走到9 所以針對每遇到一個0 就去走看看 然後針對無法的點去紀錄他不能走到9
    # part1 主要是每個9只能走到一個0，不能走到多個0 所以枚舉9
    url = 'https://adventofcode.com/2024/day/10/input'
    input_data = fetch_data_from_url(url)
    matrix = []
    for line in input_data.strip().split("\n"):
        row = list(line)
        matrix.append(row)
    m = len(matrix)
    n = len(matrix[0])
    dirs = {(0,1),(1,0), (-1,0), (0,-1)}
    
    print(day_ten_part1())
    print(day_ten_part2())
