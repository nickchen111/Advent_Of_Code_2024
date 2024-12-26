import requests
from collections import defaultdict, Counter,deque
from functools import cache
from queue import Queue

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
# part1 很多電腦會彼此連接 找出每三個三個一組的集合 有哪些集合至少有一台電腦包含t開頭
'''
從某個點開始當頭 先看他是否有t 如果有底下就是cn取2 -> n*(n-1)/2 如果沒有 底下就要看是否有t 有t的數量m *  n - m 
以此往下推
'''

def build(data, graph):
    for d in data:
        s1 = d[0] + d[1]
        s2 = d[3] + d[4]
        graph[s1].add(s2)
        graph[s2].add(s1)

# def dfs(lan : str, pa : str):
#     ret = 0
#     flag = False
#     if lan[0] == 't':
#         flag = True
#     if flag:
#         cnt = 0
#         for nxt in graph[lan]:
#             if nxt == pa:
#                 continue
#             cnt += 1
#             ret += dfs(nxt, lan)
#         ret += (cnt)(cnt-1)/2
#         return ret
#     else:
#         startWitht = 0
#         cnt = 0
#         for nxt in graph[lan]:
#             if nxt == pa:
#                 continue
#             cnt += 1
#             if nxt[0] == 't':
#                 startWitht += 1
#             ret += dfs(nxt, lan)
#         ret += startWitht * (cnt - startWitht)
#         return ret

def build(data, graph):
    for line in data:
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

def bfs(data, graph):
    triangles = set()
    
    for node in graph:
        neighbors = list(graph[node])
        
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in graph[neighbors[i]]:
                    # 檢查是否有節點以 't' 開頭
                    if node[0] == 't' or neighbors[i][0] == 't' or neighbors[j][0] == 't':
                        # 三元組排序並添加到集合中
                        triangles.add(tuple(sorted([node, neighbors[i], neighbors[j]])))

    return len(triangles)

# part2 要找互相連接點最多的點有哪些

if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/23/input'
    input_data = fetch_data_from_url(url)
    data = input_data.splitlines()
    graph = defaultdict(set)
    build(data, graph)
    print(len(graph))
    print(bfs(data, graph))
    


