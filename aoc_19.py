import requests


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# part1 問說 各種想做的毛巾 有哪些可以被你用現有的零件組成
# part2 問說每種毛巾根據現有的編織方法 每種毛巾編織方案加總為多少
# 想到Trie 自己目前的方法建樹 之後好search 
def day_nineteen(words, targets):
    class TrieNode:
        def __init__(self):
            self.children = [None]*27
            self.isEnd = False 

    class Trie:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word):
            node = self.root
            for ch in word:
                if node.children[ord(ch) - ord('a')] == None:
                    node.children[ord(ch) - ord('a')] = TrieNode()
                node = node.children[ord(ch) - ord('a')]
            node.isEnd = True

    # 初始化 Trie 並插入所有毛巾圖案
    trie = Trie()
    for word in words:
        trie.insert(word)

    def dfs(idx, target, memo) -> int:
        if idx == len(target): 
            return 1
        if memo[idx] != -1:
            return memo[idx]
        ret = 0
        node = trie.root
        for i in range(idx, len(target)):
            ch = target[i]
            if node.children[ord(ch) - ord('a')] == None:
                memo[idx] = ret
                return ret
            node = node.children[ord(ch) - ord('a')]
            
            if node.isEnd:
                ret += dfs(i + 1, target, memo)
        memo[idx] = ret
        return ret
    # 計算能夠完成的目標設計數量
    res = 0
    ret = 0
    for target in targets:
        memo = [-1]*len(target)
        cur_ways = dfs(0, target, memo)
        res += cur_ways
        if cur_ways:
            ret += 1
    print("可以完成的設計數量:", ret)
    print("總共的設計方案:", res)

if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/19/input'
    input_data = fetch_data_from_url(url)
    parts = input_data.split('\n', 1)  # 分成兩部分，最多只分一次
    words = parts[0]
    words = words.split(',')
    words = [word.strip() for word in words]
    targets = parts[1]
    targets = targets.splitlines()
    del targets[0]
    words = [word.strip() for word in words if word.strip()]
    targets = [target.strip() for target in targets if target.strip()]
    day_nineteen(words, targets)
    



