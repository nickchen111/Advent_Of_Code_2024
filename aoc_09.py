import requests
import time
from sortedcontainers import SortedDict

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def day_nine_part1():
    global cnt
    new_str = []
    n = len(input_str)

    for i in range(n):
        if i % 2:
            new_str.extend(['.'] * int(input_str[i]))
        else:
            new_str.extend([str(cnt)] * int(input_str[i]))
            cnt += 1

    left, right = 0, len(new_str) - 1
    res = 0
    print(new_str)
    while left < len(new_str) and new_str[left] != '.':
        res += left * int(new_str[left])
        left += 1

    while right >= 0 and new_str[right] == '.':
        right -= 1

    while left <= right:
        if new_str[right].isdigit():
            new_str[left] = new_str[right]
            res += left * int(new_str[left])
        new_str[right] = '.'
        left += 1
        right -= 1

        while left <= right and new_str[left] != '.':
            res += left * int(new_str[left])
            left += 1

        while right >= left and new_str[right] == '.':
            right -= 1

    return res

'''
題目變成要你先把ID大的先塞 塞到最左邊可以放置的連續空間 一路放下去 不能放就不動 可以想到的是 index, 空間大小這兩個是key 雙向隊列去放 index小不錯 遇到空間小的加入隊尾 但如果遇到index大 空間大的!?
1. 該如何設計資料結構 支持index越小且空間越大的去做使用，
2. 需要支持當我某個數字的index 小於free space起點位置時 free space就不能使用了
感覺只能用線段樹...
'''

def day_nine_part2():
    cnt = 0
    new_str = []
    n = len(input_str)
    free_space = SortedDict()  # 記錄空閒空間
    file_id = SortedDict()  # 記錄文件的長度
    file_map_id = {}  # 文件ID到起始位置的映射

    # 初始化文件和空間映射
    for i in range(n):
        if i % 2:
            new_str.extend(['.'] * int(input_str[i]))
            free_space[len(new_str) - int(input_str[i])] = int(input_str[i])
        else:
            new_str.extend([str(cnt)] * int(input_str[i]))
            file_id[len(new_str) - int(input_str[i])] = int(input_str[i]) 
            file_map_id[len(new_str) - int(input_str[i])] = cnt
            cnt += 1

    checkSum = 0

    for i, file_len in reversed(file_id.items()):
        moved = False

        for j, free_len in free_space.items():
            if j > i:
                break
            if free_len >= file_len and j < i:
                new_free_len = free_len - file_len
                checkSum += (file_len * (j + j + file_len - 1) // 2) * file_map_id[i]

                del free_space[j] 
                if new_free_len > 0:
                    free_space[j + file_len] = new_free_len
                moved = True
                break

        if not moved:
            checkSum += (file_len * (i + i + file_len - 1) // 2) * file_map_id[i]

    return checkSum
if __name__ == "__main__":
    # 第九天 將字串先轉成000....1111...2222...這樣的格式 然後把越後面的字開始往回填，直到所有字串數字的部分都合併在一起 雙指針
    url = 'https://adventofcode.com/2024/day/9/input'
    input_data = fetch_data_from_url(url)
    cnt = 0
    input_str = ''.join(filter(str.isdigit, input_data))
    print(day_nine_part1())
    start = time.perf_counter()
    print(day_nine_part2())
    end = time.perf_counter()
    print(f"精確時間間隔: {end - start} 秒")