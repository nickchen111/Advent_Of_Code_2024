import requests
from collections import defaultdict
from queue import Queue

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第五天 part1 給你一堆兩兩數字誰必須放前誰必須後的規則 問你每一個合法的array 中間數的加總是多少
    url = "https://adventofcode.com/2024/day/5/input"
    def day_five(url):
        try:
            url = "https://adventofcode.com/2024/day/5/input"
            input_data = fetch_data_from_url(url)

            sections = input_data.strip().split("\n\n")
            rules_section = sections[0].strip().split("\n")
            updates_section = sections[1].strip().split("\n")
            pairs = []
            updates = []
            for line in rules_section:
                if "|" in line:
                    pairs.append(tuple(map(int, line.split("|"))))
            for line in updates_section:
                updates.append(list(map(int, line.split(","))))

            invalid_rule_map = defaultdict(set) # or list 但是較慢
            for item in pairs:
                invalid_rule_map[item[1]].add(item[0])

            middle_sum = 0
            for line in updates:
                n = len(line)
                validation = True
                for i in range(n):
                    for j in range(i + 1, n):
                        if line[i] in invalid_rule_map and line[j] in invalid_rule_map[line[i]]:
                            validation = False
                            break
                    if not validation:
                        break

                if validation:
                    cnt += 1
                    middle_sum += line[n // 2]

            # 計算結果
            print(f"中間頁碼總和: {middle_sum}")
            # part2 可以對調位置 藉由topological sort 可以知道位置之間的關係 但是需要針對每update 都設定一個自己的indegree 略嫌麻煩 並且也要看原本的鄰接表有沒有這個點
            # 75,97,47,61,53 
            def build_graph(pairs):
                graph = defaultdict(list)
                for a, b in pairs:
                    graph[a].append(b)
                return graph
            
            def topological_sort(graph, update):
                indegree = {node: 0 for node in update}
                for node in update:
                    for neighbor in graph[node]:
                        if neighbor in update:
                            indegree[neighbor] += 1
                        
                sorted_order = []
                queue = Queue()
                for node in indegree:
                    if indegree[node] == 0:
                        queue.put(node)
                while not queue.empty():
                    sz = queue.qsize()
                    while sz:
                        sz -= 1
                        node = queue.get()
                        sorted_order.append(node)
                        for neighbor in graph[node]:
                            if neighbor in indegree:
                                indegree[neighbor] -= 1
                                if indegree[neighbor] == 0:
                                    queue.put(neighbor)
                return sorted_order
            
            graph = build_graph(pairs)
            sum = 0
            for update in updates:
                sorted_order = topological_sort(graph, update)
                if sorted_order != update:
                    n = len(sorted_order)//2
                    sum += sorted_order[n]
            print(sum)
            
        except Exception as e:
            print(e)
