import requests
from collections import Counter

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def process_input_data(input_data):
    column1 = []
    column2 = []
    for line in input_data.strip().split("\n"):
        nums = list(map(int, line.split()))
        if len(nums) == 2:  # 假設每行有兩個數字
            column1.append(nums[0])
            column2.append(nums[1])
    return column1, column2


if __name__ == "__main__":

    #第一天
    #排序後計算差加總
    url = "https://adventofcode.com/2024/day/1/input"
    def day_one(url):
        try:
            
            input_data = fetch_data_from_url(url)
            column1, column2 = process_input_data(input_data)
            column1.sort()
            column2.sort()
            res = 0
            for i in range(len(column2)):
                res += abs(column2[i] - column1[i])

            print(res)

        except Exception as e:
            print(e)

        # 計算column1 有多少數字出現在column2 出現次數*column的數字
        try:
            input_data = fetch_data_from_url(url)
            column1, column2 = process_input_data(input_data)
            mp = Counter(column2)
            # map = defaultdict(int) #可以都設置為0
            # for num in column2:
            #     map[num] += 1

            # 或者可以 map = {} 然後用 map.get(num, 0) 來判斷是否有這個值存在
            res = 0
            for num in column1:
                res += num * mp[num]
            
            print(res)
        except Exception as e:
            print(e)
    