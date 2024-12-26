import requests
import itertools
from functools import cache

# 第一個機器人用方向鍵控制數字鍵，第二個機器人用方向鍵控制第一個機器人該案的方向鍵 第三個機器人在控制第二個機器人 by 方向鍵 最後人類控制第三個機器人
'''
想法是先把數字鍵盤上會走得最短路徑都列出來 去讓第二個機器人選擇 看他怎麼走會最短
然後第二個機器人也把走的最短的cand 傳給第三個人讓他選擇 最後問說出第四個人可以走出理想的數字 人類可以製造的步數最短距離
'''

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
'''
以下註記是沒有記憶化的做法TLE
'''
# def day_twentyone_part1(data):
#     numberboard = ['789','456','123','/0A']
#     dirsboard = ['/^A','<v>']
#     #需紀錄自己走的路線用<>^v代表
#     dirs = [(0,-1),(0,1),(-1,0),(1,0)] # 上下左右
#     dirs_mapping_sign = {}
#     dirs_mapping_sign[(0,-1)] = '<'
#     dirs_mapping_sign[(0,1)] = '>'
#     dirs_mapping_sign[(-1,0)] = '^'
#     dirs_mapping_sign[(1,0)] = 'v'
#     def number_shortest_path(number):
#         q = Queue()
#         q.put((3,2,0,''))
#         m = len(numberboard)
#         n = len(numberboard[0])
#         cand = []
#         flag = 0
#         # visited = set()
#         while not q.empty():
#             x, y, idx, s = q.get()
#             # state = (x, y, idx, s)
#             # if state in visited:
#             #     continue
#             # visited.add(state)
#             if idx < len(number) and numberboard[x][y] == number[idx]:
#                 q.put((x,y, idx+1, s + 'A'))
#                 continue
#             if idx == len(number):
#                 flag = 1
#                 cand.append(s)
#                 continue
#             if not flag:
#                 for i, (dirx, diry) in enumerate(dirs):
#                     nx, ny = x + dirx, y + diry
#                     if 0 <= nx < m and 0 <= ny < n:
#                         if numberboard[nx][ny] == number[idx]:
#                             q.put((nx,ny, idx+1, s + dirs_mapping_sign[(dirx,diry)] + 'A'))
#                         else:
#                             q.put((nx,ny, idx, s + dirs_mapping_sign[(dirx,diry)]))
            
#         if number == '029A':
#             print(cand)
#         return cand
#     cand1 = [] # 第一個機器人的最佳路徑
#     for d in data:
#         cand1.append(number_shortest_path(d)) # [[3,3,3], [4,4,4],.....]
    
#     def dirs_shortest_path(dirstring):
#         q = Queue()
#         q.put((0, 2, 0, '')) 
#         m = len(dirsboard)
#         n = len(dirsboard[0])
#         visited = set()  # 記錄 (x, y, idx) 狀態
#         cand = []
#         flag = 0
#         while not q.empty():
#             x, y, idx, s = q.get()
#             state = (x, y, idx)

#             if idx < len(dirstring) and dirsboard[x][y] == dirstring[idx]:
#                 q.put((x,y, idx+1, s + 'A'))
#                 continue

#             if idx == len(dirstring):
#                 cand.append(s)
#                 flag = 1
#                 continue

#             # if state in visited:
#             #     continue
#             # visited.add(state)
          
#             if not flag:
#                 for dirx, diry in dirs:
#                     nx, ny = x + dirx, y + diry
#                     if 0 <= nx < m and 0 <= ny < n:
#                         new_s = s + dirs_mapping_sign[(dirx, diry)]
#                         if dirsboard[nx][ny] == dirstring[idx]:
#                             q.put((nx, ny, idx + 1, new_s + 'A'))
#                         else:
#                             q.put((nx, ny, idx, new_s))

#         return cand
    
    
#     # dirsboard = ['/^A','<v>']
#     # '''
#     # /^A
#     # <v>
#     # '''
#     # dist = [[float('inf')] * 3*2 for _ in range(3*2)]
#     # def calculate_min_path_foreach_dirboard(dist):
#     #     dist = [[float('inf')] * 3*2 for _ in range(3*2)]
#     #     dist[0][1] = 1
#     #     dist[1][0] = 1
#     #     dist[0][3] = 1
#     #     dist[3][0] = 1
#     #     dist[1][2] = 1
#     #     dist[2][1] = 1
#     #     dist[1][4] = 1
#     #     dist[4][1] = 1
#     #     dist[2][5] = 1
#     #     dist[5][2] = 1
#     #     dist[3][4] = 1
#     #     dist[4][3] = 1
#     #     dist[4][5] = 1
#     #     dist[5][4] = 1
#     #     for i in range(3*2):
#     #         for j in range(3*2):
#     #             if i == j:
#     #                 dist[i][j] = 0
#     #     for k in range(3*2):
#     #         for i in range(3*2):
#     #             for j in range(3*2):
#     #                 dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
#     #     return dist
#     # dist = calculate_min_path_foreach_dirboard(dist)
    
#     cand2 = [[] for _ in range(len(cand1))]
#     for idx,c in enumerate(cand1):
#         minLen = float('inf')
#         for cc in c:
#             tmp_string_array = dirs_shortest_path(cc)
#             # cand2[idx] += tmp_string_array
#             if len(tmp_string_array[0]) < minLen:
#                 minLen = len(tmp_string_array[0])
#                 cand2[idx].clear() # cand2[idx][:] or cand2[idx] = [] 也可以
#                 cand2[idx] = tmp_string_array
#             elif len(tmp_string_array[0]) == minLen:
#                 cand2[idx] += tmp_string_array

#     cand3 = [[] for _ in range(len(cand2))]
#     for idx,c in enumerate(cand2):
#         minLen = float('inf')
#         for cc in c:
#             tmp_string_array = dirs_shortest_path(cc)
#             # cand3[idx] += tmp_string_array
#             if len(tmp_string_array[0]) < minLen:
#                 minLen = len(tmp_string_array[0])
#                 cand3[idx].clear() # cand2[idx][:] or cand2[idx] = [] 也可以
#                 cand3[idx] = tmp_string_array
#             elif len(tmp_string_array[0]) == minLen:
#                 cand3[idx] += tmp_string_array
#     ret = 0
#     # input_number = [826,341,582,983,670]
#     input_number = [29,980,179,456,379]
#     mapping_str_pos = {
#         '/':0,
#         '^':1,
#         'A':2,
#         '<':3,
#         'v':4,
#         '>':5,
#     }
#     # for i, row in enumerate(cand2):
#     #     minLen = float('inf')
#     #     for j,s in enumerate(row):
#     #         start = 'A'
#     #         tmp_len = 0
#     #         for k in s:
#     #             tmp_len += dist[mapping_str_pos[start]][mapping_str_pos[k]] + 1
#     #             start = k
#     #         minLen = min(minLen, tmp_len)
#     #     ret += input_number[i] * minLen
#     for i, row in enumerate(cand3):
#         minString = min(row, key = len)
#         ret += input_number[i] * len(minString)
#     print(ret)

 
'''
加上記憶化
'''
 
dk_keys = {} # key = character, value = [row, column]
dk_keys[" "] = [0, 0]
dk_keys["^"] = [0, 1]
dk_keys["A"] = [0, 2]
dk_keys["<"] = [1, 0]
dk_keys["v"] = [1, 1]
dk_keys[">"] = [1, 2]
 
nk_keys = {}
nk_keys["7"] = [0, 0]
nk_keys["8"] = [0, 1]
nk_keys["9"] = [0, 2]
nk_keys["4"] = [1, 0]
nk_keys["5"] = [1, 1]
nk_keys["6"] = [1, 2]
nk_keys["1"] = [2, 0]
nk_keys["2"] = [2, 1]
nk_keys["3"] = [2, 2]
nk_keys[" "] = [3, 0]
nk_keys["0"] = [3, 1]
nk_keys["A"] = [3, 2]
 
# assumption: longer sequence of presses never has lower cost
 
def get_sequences(dict):
  derived_dict = {}
  for current in dict:
    if current == " ":
      continue
    for goal in dict:
      if goal == " ":
        continue
      cr, cc = dict[current][0], dict[current][1]
      gr, gc = dict[goal][0], dict[goal][1]
      keys_to_press = []
      for r in range(abs(cr - gr)):
        if cr > gr:
          keys_to_press.append("^")
        if cr < gr:
          keys_to_press.append("v")
      for c in range(abs(cc - gc)):
        if cc > gc:
          keys_to_press.append("<")
        if cc < gc:
          keys_to_press.append(">")
      options = []
      for key_permutation in list(itertools.permutations(keys_to_press)):
        # if it crosses a gap, then omit it
        r, c = cr, cc
        key_list_valid = True
        key_list = ""
        for key in key_permutation:
          if key == "^":
            r -= 1
          if key == "v":
            r += 1
          if key == "<":
            c -= 1
          if key == ">":
            c += 1
          if r == dict[" "][0] and c == dict[" "][1]:
            key_list_valid = False
            break
          key_list += key
        if key_list_valid:
          options.append(key_list)
      derived_dict[current + goal] = options
  return derived_dict
 
d2d = get_sequences(dk_keys)
n2d = get_sequences(nk_keys)
 
@cache
def get_all_sub_sequences(str, use_n2d):
  dict = d2d
  if use_n2d:
    dict = n2d
  if len(str) == 1:
    return [""]
  options = []
  for next_step in dict[str[:2]]:
    for rest_of_steps in get_all_sub_sequences(str[1:], use_n2d):
      options.append(next_step + "A" + rest_of_steps)
  return list(set(options))
 
@cache
def get_all_sequences(str, use_n2d):
  return get_all_sub_sequences("A" + str, use_n2d)
 

if __name__ == "__main__":
  url = 'https://adventofcode.com/2024/day/21/input'
  input_data = fetch_data_from_url(url)
  lines = input_data.splitlines()

  total = 0
  for line in lines:
    code = int(line.replace("A", ""))
    options = get_all_sequences(line, True)
    shortest_option = -1
    for option in options:
      for option2 in get_all_sequences(option, False):
        for option3 in get_all_sequences(option2, False):
          if shortest_option == -1 or shortest_option > len(option3):
            shortest_option = len(option3)
    total += code * shortest_option
  print (total)