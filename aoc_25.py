import requests

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def distinguish_data(matrix : list[list[str]]) -> tuple[list[str], list[str]]:
    locks = []
    keys = []
    for i,m in enumerate(matrix):
        lock = True
        for ch in m[0]:
            if ch != '#':
                lock = False
                break
        if lock:
            locks.append(m)
        else:
            keys.append(m)
    
    return locks, keys

# part1 問說 將lock 跟 key 按照特性分類後 判斷一下lock的剩餘空間. 是否能讓key的長度 # 插入 並且每列都要判斷 問說有多少個這樣的組合
# part2 需要收集前面我尚未收集到的 5 star
def day_twentyFive_part1(lock: list[str], keys:list[str]):
    def locks_handle(lock: list[str]) -> list:
        lock_arr = []
        m = len(lock)
        n = len(lock[0])
        for j in range(n):
            cnt = 0
            for i in range(m):
                if lock[i][j] == '#':
                    cnt += 1
                else:
                    break
            lock_arr.append(m - cnt) # 計算剩餘空間
        return lock_arr

    def keys_handle(key: list[str]) -> list:
        key_arr = []
        m = len(key)
        n = len(key[0])

        for j in range(n):
            cnt = 0
            for i in range(m-1, -1, -1):
                if key[i][j] == '#':
                    cnt += 1
                else:
                    break
            key_arr.append(cnt)
        return key_arr
    locks_arr = [locks_handle(lock) for lock in locks]
    keys_arr = [keys_handle(key) for key in keys]
    ret = 0
    
    for key in keys_arr:
        for lock in locks_arr:
            flag = True
            for i in range(len(lock)):
                print(lock[i], key[i])
                if lock[i] - key[i] < 0:
                    flag = False
                    break
            if flag:
                ret += 1
    print(ret)


if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/25/input'
    input_data = fetch_data_from_url(url)
    data = input_data.split('\n\n')
    matrix = [[] for _ in range(len(data))]
    for i,d in enumerate(data):
        matrix[i] = d.split('\n')
    
    del matrix[-1][-1]
    # print(matrix)
    locks, keys = distinguish_data(matrix)
   
    day_twentyFive_part1(locks, keys)
    
