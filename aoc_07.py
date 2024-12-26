import requests


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第七天 可能是+ or * 判斷一下每種可能 如果能正確得到等式 那就加入ans 求總和
    try:
        url = "https://adventofcode.com/2024/day/7/input"
        input_data = fetch_data_from_url(url)
        targets = []
        arr = []
        for line in input_data.strip().split("\n"):
            key, values = line.split(":")
            targets.append(int(key.strip()))
            arr.append(list(map(int, values.strip().split())))

        def day_seven_part1(targets, arr):
            res = 0
            for idx in range(len(arr)):
                cur_set = set()
                cur_set.add(arr[idx][0])
                n = len(arr[idx])
                target = targets[idx]
                for i in range(1,n):
                    new_set = set()
                    cur = arr[idx][i]
                    for s in cur_set:
                        ns1 = s*cur
                        ns2 = s+cur
                        if ns1 <= target:
                            new_set.add(ns1)
                        if ns2 <= target:
                            new_set.add(ns2)    
                    cur_set = new_set
                if target in cur_set:
                    res += target
            return res
        # print(day_seven_part1(targets, arr))

        # part2 新增一個 || 可以變成12 || 34 = 1234
        def day_seven_part2(targets, arr):
            res = 0
            for idx in range(len(arr)):
                cur_set = set()
                cur_set.add(arr[idx][0])
                n = len(arr[idx])
                target = targets[idx]
                target_str = str(target)
                for i in range(1,n):
                    new_set = set()
                    cur = arr[idx][i]
                    s2 = str(cur)
                    for s in cur_set:
                        ns1 = s*cur
                        ns2 = s+cur
                        s1 = str(s)
                        s3 = s1 + s2
                        if ns1 <= target:
                            new_set.add(ns1)
                        if ns2 <= target:
                            new_set.add(ns2) 
                        if len(s3) <= len(target_str):
                            new_num = int(s3)
                            if new_num <= target:
                                new_set.add(new_num)
                    cur_set = new_set
                if target in cur_set:
                    res += target
            return res
        
        # print(day_seven_part2(targets, arr))
    except Exception as e:
        print(e)