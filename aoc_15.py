import requests
from typing import Generator

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def find_next_space(direction, x, y, matrix):
    """找出下一個空格的位置，並檢查是否能將 O 推過去"""
    if direction == '^':  # 上
        # 找 x 上方的下一個空格
        next_space = None
        next_obs = None
        for i,row in enumerate(matrix):
            for j, si in enumerate(row):
                if j == y and i < x:
                    if si == '.':
                        next_space = i
                    elif si == '#':
                        next_obs = i
        return next_space, next_obs
    elif direction == 'v':  # 下
        # 找 x 下方的下一個空格
        next_space = None
        next_obs = None
        for i,row in enumerate(matrix):
            for j, si in enumerate(row):
                if j == y and i > x:
                    if si == '.' and next_space == None:
                        next_space = i
                    elif si == '#' and next_obs == None:
                        next_obs = i
        return next_space, next_obs
    elif direction == '>':  # 右
        # 找 y 右方的下一個空格
        next_space = None
        next_obs = None
        for i,row in enumerate(matrix):
            for j, si in enumerate(row):
                if i == x and j > y:
                    if si == '.' and next_space == None:
                        next_space = j
                    elif si == '#' and next_obs == None:
                        next_obs = j
        return next_space, next_obs
    elif direction == '<':  # 左
        # 找 y 左方的下一個空格
        next_space = None
        next_obs = None
        for i,row in enumerate(matrix):
            for j, si in enumerate(row):
                if i == x and j < y:
                    if si == '.':
                        next_space = j
                    elif si == '#':
                        next_obs = j
        return next_space, next_obs
    return None, None

def day_fifteen_part1(matrix, instructions):
    # 找出機器人位置，並初始化障礙物和空格的記錄
    startx, starty = 0, 0
    m, n = len(matrix), len(matrix[0])
    
    for i, row in enumerate(matrix):
        for j, ch in enumerate(row):
            if ch == "@":
                startx, starty = i, j
                break
    print(startx, starty)
    x, y = startx, starty
    for ins in instructions:
        if ins in '^v><':
            dx, dy = 0, 0
            if ins == '^':
                dx, dy = -1, 0
            elif ins == 'v':
                dx, dy = 1, 0
            elif ins == '>':
                dx, dy = 0, 1
            elif ins == '<':
                dx, dy = 0, -1

            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] == '.':
                # 直接移動到空格
                matrix[x][y] = '.'
                x, y = nx, ny
                matrix[nx][ny] = '@'
            elif 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] == 'O':
                # 推動箱子
                next_space, next_obs = find_next_space(ins, nx, ny, matrix)
                if next_space is not None and (next_obs is None or next_obs > next_space if ins in 'v>' else next_obs < next_space):
                    # 更新地圖
                    print("update")
                    if ins in '^v':
                        matrix[next_space][ny] = 'O'
                    else:
                        matrix[nx][next_space] = 'O'
                    matrix[x][y] = '.'
                    matrix[nx][ny] = '@'
                    x, y = nx, ny  # 更新機器人位置

    # 計算 GPS 座標和
    ret = 0
    for i, row in enumerate(matrix):
        for j, sp in enumerate(row):
            if sp == 'O':
                ret += 100 * i + j
    print(ret)

DIRECTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}

# part2 開始 上述的是比較混亂的part1 code
Position = list[list[str]]
def find_box(matrix: Position) -> Generator[tuple[int, int], None, None]: # Generator[YieldType, SendType, ReturnType]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == '[':
                yield i,j

def find_robot(matrix) -> Generator[Position, None, None]:
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == "@":
                return row, col

    raise ValueError("No robot found")

def check_moveable(matrix, row: int, col: int, dr: int, dc: int, seen: set) -> bool:
    if (row, col) in seen:
        return True
    seen.add((row, col))
    
    nr, nc = row + dr, col + dc
    
    match matrix[nr][nc]:
        case '#':
            return False
        case '[':
            return check_moveable(matrix, nr, nc, dr, dc, seen) and check_moveable(matrix, nr, nc+1, dr, dc, seen)
        case ']':
            return check_moveable(matrix, nr, nc, dr, dc, seen) and check_moveable(matrix, nr, nc-1, dr, dc, seen)
        # 可補part1 的 'O'
        case 'O':
            return check_moveable(matrix, nr, nc, dr, dc, seen)
    return True

def is_valid(x: int, y:int, matrix : Position) -> bool:
    m = len(matrix)
    n = len(matrix[0])
    return 0 <= x < m and 0 <= y < n and matrix[x][y] != '#'

def process_instruction(matrix : Position, instruction: str, row: int, col: int) -> tuple[int,int]:
    dr, dc = DIRECTIONS[instruction]

    nr, nc = row + dr, col + dc

    if not is_valid(nr, nc, matrix):
        return row, col

    if matrix[nr][nc] in ["[", "]", "O"]:
        seen = set()

        if not check_moveable(matrix, row, col, dr, dc, seen):
            return row, col

        while len(seen) > 0:
            for r, c in seen.copy():
                nr2, nc2 = r + dr, c + dc
                if (nr2, nc2) not in seen:
                    if matrix[nr2][nc2] != "@" and matrix[r][c] != "@":
                        matrix[nr2][nc2] = matrix[r][c]
                        matrix[r][c] = "."

                    seen.remove((r, c))

        matrix[row][col], matrix[nr][nc] = matrix[nr][nc], matrix[row][col]
        return nr, nc

    matrix[row][col], matrix[nr][nc] = matrix[nr][nc], matrix[row][col]
    return nr, nc

            

def gps(matrix: Position) -> int:
    return sum(100 * box[0] + box[1] for box in find_box(matrix))

def process_input(data):
    lines = data.strip().split('\n')

    separator_index = 0
    for i, line in enumerate(lines):
        if line.startswith('^') or line.startswith('<') or line.startswith('v') or line.startswith('>'):
            separator_index = i
            break
    
    matrix = [list(row) for row in lines[:separator_index-1]]
    
    # 指令部分去掉換行，存為一維字串陣列
    instructions = ''.join(lines[separator_index:]).strip()
    
    return matrix, instructions


if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/15/input'
    input_data = fetch_data_from_url(url)
    initial_matrix, instructions = process_input(input_data)
    # . 是空格 O 是 箱子, @ 是機器人 # 是牆壁
    # day_fifteen_part1(matrix, instructions)
    # 放大地圖
    matrix = []
    for row in range(len(initial_matrix)):
        if len(matrix) <= row or row not in matrix:
            matrix.append([])

        for col in range(len(initial_matrix[0])):
            match initial_matrix[row][col]:
                case "#":
                    matrix[row].extend(["#", "#"])
                case "O":
                    matrix[row].extend(["[", "]"])
                case ".":
                    matrix[row].extend([".", "."])
                case "@":
                    matrix[row].extend(["@", "."])

    row, col = find_robot(matrix)
    for instruction in instructions:
        row, col = process_instruction(matrix,  instruction, row, col)
    print(gps(matrix))