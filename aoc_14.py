import requests
import re

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def find_robot_cycle(x: int, y: int, dirx: int, diry: int) -> tuple[dict, int]:
    """
    記錄機器人位置的週期性行為。
    返回步數對應位置的字典與週期長度。
    """
    MODX, MODY = 101, 103
    visited = {}  # 位置對應步數
    step_to_pos = {}  # 步數對應位置
    visited[(x, y)] = 0
    step_to_pos[0] = (x, y)

    for step in range(1, MODX * MODY + 1):  # 最多走完所有可能位置的組合
        x, y = (x + dirx) % MODX, (y + diry) % MODY
        if (x, y) in visited:
            cycle_length = step - visited[(x, y)]
            return step_to_pos, cycle_length
        visited[(x, y)] = step
        step_to_pos[step] = (x, y)

    return step_to_pos, -1  # 無週期

def get_robot_position_at_step(step_to_pos: dict, cycle_length: int, steps: int) -> tuple[int, int]:
    """
    根據記錄的步數對應位置與週期長度，計算指定步數的位置。
    """
    if cycle_length == -1 or steps < len(step_to_pos):
        return step_to_pos[steps]
    remaining_steps = (steps - len(step_to_pos)) % cycle_length
    last_cycle_start = max(step for step in step_to_pos if step < len(step_to_pos))
    return step_to_pos[last_cycle_start + remaining_steps]

def four_part(matrix) -> int:
    """
    計算指定象限內的機器人數量。
    """
    mid_x = 101 // 2
    mid_y = 103 // 2
    count1 = count2 = count3 = count4 = 0
    for x in range(101):
        for y in range(103):
            if x > mid_x and y < mid_y:
                count1 += matrix[x][y]
            elif x < mid_x and y < mid_y:
                count2 += matrix[x][y]
            elif x < mid_x and y > mid_y:
                count3 += matrix[x][y]
            elif x > mid_x and y > mid_y:
                count4 += matrix[x][y]
    return count1 * count2 * count3 * count4

def check(matrix) -> bool:
    """
    檢查是否存在連續5個機器人的水平或垂直圖案。
    """
    for row in matrix:
        cnt = 0
        for cell in row:
            if cell > 0:
                cnt += 1
                if cnt >= 5:
                    return True
            else:
                cnt = 0
    return False

if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/14/input'
    input_data = fetch_data_from_url(url)

    # 使用正則表達式解析 p 和 v 的數值
    pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    matches = re.findall(pattern, input_data)
    parsed_data = [((int(px), int(py)), (int(vx), int(vy))) for px, py, vx, vy in matches]

    # 記錄所有機器人的移動週期
    robot_cycles = []
    for p in parsed_data:
        step_to_pos, cycle_length = find_robot_cycle(p[0][0], p[0][1], p[1][0], p[1][1])
        robot_cycles.append((step_to_pos, cycle_length))

    # 模擬指定秒數並檢查圖案
    for time in range(1, 8000):
        matrix = [[0] * 103 for _ in range(101)]
        for step_to_pos, cycle_length in robot_cycles:
            x, y = get_robot_position_at_step(step_to_pos, cycle_length, time)
            matrix[x][y] += 1
        if check(matrix):
            print(f"現在時間 {time}")
            for row in matrix:
                print("".join("#" if cell > 0 else "." for cell in row))
   
    
    
    


