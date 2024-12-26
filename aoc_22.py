import requests
from collections import defaultdict,deque

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
def day_twenytwo_part1(data):
    MOD = 16777216

    # @cache
    def dfs(num: int):
        cur_num = num
        cand = []
        s = "".join(set(str(cur_num)))
        cand.append(s)
        for cnt in range(2000):
            for step in range(3): 
                if step == 0:
                    cur_num = ((cur_num*64) ^ cur_num) % MOD
                elif step == 1:
                    cur_num = ((cur_num//32) ^ cur_num) % MOD
                else:
                    cur_num = ((cur_num*2048) ^ cur_num) % MOD
            # 這裡可以預處理一下cur_num的元素有哪些數字
            new_num = cur_num % 10
            s = str(new_num)
            cand.append(s)
        return cur_num, cand
    ret = 0
    cands = []
    for d in data:
        c,cand = dfs(d)
        cands.append(cand)
        ret += c
    print(ret)
    return cands

def day_twentytwo_part2(cands):
    # create all possible output
    m = len(cands)
    # vector<unordered_map<string, int>> map; 在某index上 字串diff為? 會是多少的數字
    arr = [defaultdict(int) for _ in range(m)] # 每個index 代表不同的祕密數字可以湊出的四個差值的最大值是多少
    allPossible = set() # 每個差值的可能組合
    
    # def backtrack(idx:int, cand, path, prev:int, j):
    #     if idx == len(cand):
    #         return
    #     if idx == 0:
    #         for i in cand[idx]:
    #             backtrack(idx+1, cand, path, int(i), j)
    #     else:
    #         for i in cand[idx]:
    #             cur = int(i) - prev
    #             path.append(str(cur))
    #             if idx >= 3:
    #                 if len(path) > 4:
    #                     path.popleft()
    #                 s = "".join(path)
    #                 arr[j][s] = max(arr[j][s], int(cand[idx]))
    #                 allPossible.add(tuple(path))
    #             backtrack(idx+1, cand, path, int(i), j)
    #             path.popleft()

    delta = {}
    def slide_windoew(cand):
        # x x x x x 
        dq = deque(maxlen=4) # 這樣寫就會自己彈出 讚讚
        seen = set()
        for i in range(1,len(cand)):
            dq.append(int(cand[i]) - int(cand[i-1]))
            if len(dq) == 4:
                pattern = tuple(dq)
                if pattern not in seen:
                    seen.add(pattern)
                    delta[pattern] = delta.get(pattern, 0) + int(cand[i])
                
    for i in range(m):
        slide_windoew(cands[i])
   
    print(max(delta.values()))
            


if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/22/input'
    input_data = fetch_data_from_url(url)
    data = input_data.splitlines()
    data = [int(s) for s in data] # or list(map[int, data])
    # len = 1842 每個都要按照規則跑2000次 用def + memo 根據 目前要跑的數字與還需要跑的次數去做memo
    # 第一次 將num * 64 在做XOR 之後 % MOD  第二次: //32 下取整 XOR 後MOD 第三次就是*2048
    cands = day_twenytwo_part1(data)
    day_twentytwo_part2(cands)
