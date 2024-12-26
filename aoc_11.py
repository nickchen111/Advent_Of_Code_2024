import requests
from collections import defaultdict


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第十一天 
    # part1 石頭改變規則是 0變1，even個數字 變成兩個 左半邊 跟右半邊拆分 並且不會有前導0，其餘的就是當下數字*2024，改變25次會變啥?
    input_data = "890 0 1 935698 68001 3441397 7221 27"
    input_data = input_data.split() # input_data = list(map(int, input_data.split()))
    input_data = map(int, [i for i in input_data])
    memo = defaultdict(lambda: defaultdict(int))
    #我覺得時間複雜度大概會是 stone狀態個數 * step遞迴深度
    def process_stone(stone, step):
        # if stone == 0:
        #     return [1]
        # stone_str = str(stone)
        # if len(stone_str) % 2 == 0:
        #     mid = len(stone_str)//2
        #     left = int(stone_str[:mid])
        #     right = int(stone_str[mid:])
        #     return [left, right]
        # return [stone*2024]
        if stone == 0:
            stone = 1
            step -= 1

        if step <= 0:
            return 1
        if stone in memo and step in memo[stone]:
            return memo[stone][step]
        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            mid = len(stone_str)//2
            left = int(stone_str[:mid])
            right = int(stone_str[mid:])
            memo[stone][step] = process_stone(left, step-1) + process_stone(right, step-1)
        else:
            memo[stone][step] = process_stone(stone*2024, step-1)
        return memo[stone][step]
    def day_eleven(blink):
        stones = input_data
        res = 0
        for stone in stones:
            res += process_stone(stone,blink)
        return res
    print(day_eleven(75))