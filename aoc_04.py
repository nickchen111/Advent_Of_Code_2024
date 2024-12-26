import requests
from functools import cache
import time
from datetime import datetime

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第四天 明顯的word search 最好搭配記憶化 XMAS 可以上下左右甚至斜角走但不能換方向 問說有多少個XMAS vector<vector<vector<int>>> memo(m, vector<vector<int>>(n, vector<int>(4,0)));
    url = "https://adventofcode.com/2024/day/4/input"
    def day_four(url):
        try:
            input_data = fetch_data_from_url(url)
            matrix = []
            for line in input_data.strip().split("\n"):
                row = list(line)
                matrix.append(row)
            m = len(matrix)
            n = len(matrix[0])
            dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]
            target = "XMAS"
            cnt = 0
            
            # @cache
            def dfs(i, j, idx, dx, dy):
                if idx == len(target):
                    return True
                nx, ny = i + dx, j + dy
                if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] == target[idx]:
                    return dfs(nx, ny, idx + 1, dx, dy)
                return False
            start = time.perf_counter()
            for i in range(m):
                for j in range(n):
                    if matrix[i][j] == target[0]:
                        for dx, dy in dirs:
                            if dfs(i, j, 1, dx, dy):
                                cnt += 1
            print(cnt)
            end = time.perf_counter()
            print(f"精確時間間隔: {end - start} 秒")

            # part2 題目 問你要是中間是A 左上與右下 右上與左下去形成MAS 並且這樣一組會長的像X 的組合數量
            valid_chars = {'M', 'S'}
            dirs2 = [[(-1,-1),(1,1)], [(1,-1), (-1,1)]]
            cnt2 = 0
            def dfs2(i: int, j: int) -> bool:
                for arr in dirs2:
                    nx1 = i + arr[0][0]
                    ny1 = j + arr[0][1]
                    nx2 = i + arr[1][0]
                    ny2 = j + arr[1][1]
                    if not (0 <= nx1 < m and 0 <= ny1 < n and 0 <= nx2 < m and 0 <= ny2 < n and matrix[nx1][ny1] != matrix[nx2][ny2] and matrix[nx1][ny1] in valid_chars and matrix[nx2][ny2] in valid_chars):
                        return False
                return True
            for i in range(m):
                for j in range(n):
                    if matrix[i][j] == 'A':
                        if dfs2(i, j):
                            cnt2 += 1
            print(cnt2)
            
        except Exception as e:
            print(e)
    