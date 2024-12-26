import requests
from collections import defaultdict

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def day_six＿part1(matrix):
    try:
        #part1 只需要模擬他走的路程
        cur_dir = 0
        cnt = 1
        x = startx
        y = starty
        while True:
            nx = x + dir_map[cur_dir % MOD][0]
            ny = y + dir_map[cur_dir % MOD][1]
            if nx >= m or ny >= n or nx < 0 or ny < 0:
                break
            if matrix[nx][ny] == '#':
                cur_dir += 1
                continue
            elif matrix[nx][ny] == '.':
                matrix[nx][ny] = 'X'
                cnt += 1
            x = nx
            y = ny 
        return cnt
    except Exception as e:
        print(e)
def day_six_part2(matrix):
    try:
        '''錯誤的想法，想說只要碰撞到障礙物的同一個角落一次就會是循環，我想說用二分快速找出 並且每走到.處就判斷一下他的上下左右是否有已經碰撞過的障礙物，但他繞的圈可能不止四個角所以fail
        obs_map = defaultdict(lambda: [0] * 4)  # 用來記錄障礙物位置和碰撞次數 lamda 匿名函數
        obs_row = SortedSet()  # 記錄每行有哪些障礙物
        obs_col = SortedSet()  # 記錄每列有哪些障礙物
        cnt = 0
        x = 0
        y = 0
        cur_dir = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '#':
                    obs_map[i * n + j]  # 初始化障礙物位置
                    obs_row.add(i)
                    obs_col.add(j)
                if matrix[i][j] == '^':
                    x = i
                    y = j
        while True:
            nx = x + dir_map[cur_dir % MOD][0]
            ny = y + dir_map[cur_dir % MOD][1]
            # 確認是否超出邊界
            if nx >= m or ny >= n or nx < 0 or ny < 0:
                break

            if matrix[nx][ny] == '#':
                # 紀錄撞擊
                obs_map[nx * n + ny][cur_dir % MOD] += 1
                cur_dir += 1
                continue
            elif matrix[nx][ny] != 'X':
                # 計算下一個方向
                new_dir = (cur_dir + 1) % MOD
                
                if new_dir == 0:  # 向下方向
                    # row_list = sorted(obs_row)
                    idx = bisect.bisect_right(obs_row, nx)
                    if idx > 0:
                        prev_row = obs_row[idx - 1]
                        if obs_map[prev_row * n + ny][new_dir] >= 1:
                            cnt += 1
                            matrix[nx][ny] = 'X'

                elif new_dir == 1:  # 向右方向
                    # col_list = sorted(obs_col)
                    idx = bisect.bisect_right(obs_col, ny)
                    if idx < len(obs_col):
                        next_col = obs_col[idx]
                        if obs_map[nx * n + next_col][new_dir] >= 1:
                            cnt += 1
                            matrix[nx][ny] = 'X'

                elif new_dir == 2:  # 向上方向
                    # row_list = sorted(obs_row)
                    idx = bisect.bisect_right(obs_row, nx)
                    if idx < len(obs_row):
                        next_row = obs_row[idx]
                        if obs_map[next_row * n + ny][new_dir] >= 1:
                            cnt += 1
                            matrix[nx][ny] = 'X'

                else:  # 向左方向
                    # col_list = sorted(obs_col)
                    idx = bisect.bisect_right(obs_col, ny)
                    if idx > 0:
                        prev_col = obs_col[idx - 1]
                        if obs_map[nx * n + prev_col][new_dir] >= 1:
                            cnt += 1
                            matrix[nx][ny] = 'X'
            x = nx
            y = ny
        print(cnt)
        '''
        # part2 可以任意設置一個障礙物讓他無限迴圈 問有多少種位置可以設置
        
        def simulate_guard(matrix, start_x, start_y, start_dir, m, n):
            visited = set()
            x, y = start_x, start_y
            cur_dir = start_dir
            while True:
                if (x, y, cur_dir) in visited:
                    return True  # 進入循環
                visited.add((x, y, cur_dir))
                
                nx, ny = x + dir_map[cur_dir][0], y + dir_map[cur_dir][1]
                if nx < 0 or nx >= m or ny < 0 or ny >= n:
                    return False
                    # 撞牆，改變方向
                if matrix[nx][ny] == '#':
                    cur_dir = (cur_dir + 1) % MOD
                else:
                    x, y = nx, ny  # 正常移動

        def count_obstruction_positions(matrix):
            m, n = len(matrix), len(matrix[0])
            x, y, cur_dir = startx, starty, 0
            # 找到守衛的起始位置
            for i in range(m):
                for j in range(n):
                    if matrix[i][j] == '^':
                        x = i
                        y = j
                        break
                if x and y:
                    break
            valid_positions = 0

            # 嘗試每個空位新增障礙物
            for i in range(m):
                for j in range(n):
                    if matrix[i][j] == 'X' and (i, j) != (x, y):
                        # 模擬新增障礙物
                        matrix[i][j] = '#'
                        if simulate_guard(matrix, x, y, cur_dir, m, n):
                            valid_positions += 1
                        # 恢復原狀
                        matrix[i][j] = '.'
            return valid_positions
        # count_obstruction_positions(matrix)
        return count_obstruction_positions(matrix)
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
     # 第六天 走格子 讓警衛可以走出map 撞到障礙物就要turn right 90 
    url = " https://adventofcode.com/2024/day/6/input"
    input_data = fetch_data_from_url(url)
    matrix = []
    for line in input_data.strip().split("\n"):
        row = list(line)
        matrix.append(row)
    m = len(matrix)
    n = len(matrix[0])
    # 先找出位置在哪 然後判斷一下他現在是往哪個方向 up:0 -> right:1 -> down:2 -> left:3 循環
    dir_map = defaultdict(tuple)
    dir_map[0] = (-1,0)
    dir_map[1] = (0,1)
    dir_map[2] = (1,0)
    dir_map[3] = (0,-1)
    MOD = 4
    startx = 0
    starty = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '^':
                startx = i
                starty = j
                break
        if startx and starty:
            matrix[startx][starty] = 'X'
            break
    print("第六天part1", day_six_part1(matrix))
    print("第六天part2", day_six_part2(matrix))