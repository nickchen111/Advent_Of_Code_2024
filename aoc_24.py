import requests
import re
import copy
from collections import defaultdict

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# part1 問說 XOR or OR or AND 去解出未知數 保證可以解 問說Zxx 的 數字 去組合二進制數字 會是多少 -> 單純不斷嘗試然後依照AND OR XOR 狀況判斷是否可解即可
# part2 問說 x01 AND y01 = z01 有些會被改成 x01 AND y01 = z03 這種就要去做交換把它換回來 問說有多少種這種狀況輸出出現這種狀況的電線 似乎需要邏輯電路 計算機架構 等知識 先pass 
def day_twentyfour_part1(value_map, gate_map):
    z_map = {}
    keys_to_delete = set()  # 用於儲存待刪除的鍵
    
    while len(gate_map):
        progress_made = False  # 記錄當前迴圈是否有進展

        for key, value in gate_map.items():
            if key[0] in value_map and key[1] in value_map:
                # 計算新的值
                if key[2] == 'AND':
                    new_num = value_map[key[0]] & value_map[key[1]]
                elif key[2] == 'OR':
                    new_num = value_map[key[0]] | value_map[key[1]]
                elif key[2] == 'XOR':
                    new_num = value_map[key[0]] ^ value_map[key[1]]
                else:
                    raise ValueError(f"Unknown gate operation: {key[2]}")
                # 更新 value_map
                if value == 'vcd':
                    print("找到",new_num)
                value_map[value] = new_num

                # 如果鍵以 'z' 開頭，記錄到 z_map
                if value.startswith('z'):
                    z_map[value] = new_num

                # 標記該鍵待刪除
                keys_to_delete.add(key)
                progress_made = True  # 記錄進展
            elif (key[0] in value_map or key[1] in value_map) and value in value_map:
                # 處理部分初始化的情況
                if key[0] in value_map:
                    num1 = value_map[key[0]]
                    need_to_check = key[1]
                else:
                    num1 = value_map[key[1]]
                    need_to_check = key[0]
                num2 = value_map[value]

                if key[2] == 'AND' and num1 == 1:
                    value_map[need_to_check] = num2
                    if need_to_check.startswith('z'):
                        z_map[need_to_check] = num2
                    keys_to_delete.add(key)
                    progress_made = True
                elif key[2] == 'OR' and ((num1 == 0 and num2 == 1) or (num1 == 0 and num2 == 0)):
                    value_map[need_to_check] = num2
                    if need_to_check.startswith('z'):
                        z_map[need_to_check] = num2
                    keys_to_delete.add(key)
                    progress_made = True
                elif key[2] == 'XOR':
                    value_map[need_to_check] = 1 - num1 if num2 == 1 else num1
                    if need_to_check.startswith('z'):
                        z_map[need_to_check] = 1 - num1 if num2 == 1 else num1
                    keys_to_delete.add(key)
                    progress_made = True

        # 批量刪除已處理的鍵
        for key in keys_to_delete:
            del gate_map[key]
        keys_to_delete.clear()

        # 如果本次迴圈沒有進展，退出避免死循環
        if not progress_made:
            # print(f"Remaining gates cannot be resolved:",gate_map, "have", value_map)
            break

    # 對 z_map 排序並計算結果
    sorted_by_key = dict(sorted(z_map.items()))
    ret = 0
    for key, value in sorted_by_key.items():
        if value:
            try:
                num = int(key[1:])  # 確保鍵結構固定為 'zXX'
                ret |= (1 << num)
            except ValueError:
                print(f"Invalid key format: {key}")

    print(ret)


# 輔助函式：解析資料
def gates_wires(file_name):
    wires, g = open(file_name).read().split("\n\n")
    wires = {w.split(":")[0]: int(w.split(":")[1]) for w in wires.strip().split("\n")}
    gates = {}
    for gate in [wire for wire in g.strip().split("\n")]:
        left, operation, right, _, output_wire = gate.split(" ")
        gates[(left,right, operation)] = output_wire

    return wires, gates


if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/24/input'
    input_data = fetch_data_from_url(url)
    wires, gates = gates_wires("input.txt")
    # value_map, gate_map = parse_data(input_data)
    # print(gate_map)
    # print(gates)
    day_twentyfour_part1(wires, gates)


