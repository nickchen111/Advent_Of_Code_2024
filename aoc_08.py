import requests


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    #第八天
    url = 'https://adventofcode.com/2024/day/8/input'
    input_data = fetch_data_from_url(url)
    matrix = []
    for line in input_data.strip().split("\n"):
        row = list(line)
        matrix.append(row)
    m = len(matrix)
    n = len(matrix[0])
    def day_eight():
        # 要把所有相同元素的先組合起來 然後n^2去看每個人可以產生的點 根據相差就可以判斷兩者該往哪邊產點 所以還需要產點的位置訊息
        pos = set()
        char_map = {}

        # 將字符的位置存入 char_map
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != '.':
                    char_map.setdefault(matrix[i][j], []).append((i, j))

        # 對於每個字符的所有位置，檢查可能的條件
        for char, positions in char_map.items():
            num_positions = len(positions)
            for i in range(num_positions):
                for j in range(i + 1, num_positions):
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]

                    # 第一種情況：從 (x1, y1) 延伸
                    xdiff, ydiff = x1 - x2, y1 - y2
                    cx, cy = x1 + xdiff, y1 + ydiff
                    while 0 <= cx < m and 0 <= cy < n:
                        pos.add((cx, cy))
                        cx += xdiff
                        cy += ydiff

                    # 第二種情況：從 (x2, y2) 延伸
                    xdiff, ydiff = x2 - x1, y2 - y1
                    cx, cy = x2 + xdiff, y2 + ydiff
                    while 0 <= cx < m and 0 <= cy < n:
                        pos.add((cx, cy))
                        cx += xdiff
                        cy += ydiff
                    while x1 != x2 and y1 != y2:
                        pos.add((x1,y1))
                        x1 += xdiff
                        y1 += ydiff
                    pos.add((x2,y2))
        # 返回集合的大小
        return len(pos)
    print(day_eight())