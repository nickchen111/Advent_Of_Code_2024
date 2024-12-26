import requests

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
     #第二天 不錯的題目 需要用到前後綴分解
    url = "https://adventofcode.com/2024/day/2/input"
    def day_two(url):
        try:
            input_data = fetch_data_from_url(url)
            count = 0
            count_2 = 0
            for line in input_data.split("\n"):
                nums = list(map(int, line.split()))
                if len(nums) < 2:
                    continue 
                elif len(nums) == 2:
                    if abs(nums[0] - nums[1]) <= 3:
                        count += 1
                        count_2 += 1
                    continue
                '''
                part1 暴力解
                def check(nums):
                    is_increasing = None  # None: 未确定, True: 遞增, False: 遞減
                    valid = True 
                    for idx in range(1, len(nums)):
                        diff = nums[idx] - nums[idx - 1]
                        if abs(diff) == 0 or abs(diff) > 3:
                            valid = False
                            break
                        if is_increasing is None:
                            is_increasing = diff > 0
                        else:
                            if is_increasing and diff < 0:
                                valid = False
                                break
                            elif not is_increasing and diff > 0:
                                valid = False
                                break
                    return valid
                硬要if else 探討可能的寫法:
                '''
                def increasing(nums):
                    violations = 0
                    prev = -1
                    chance = 0
                    for i in range(1, len(nums)):
                        if chance != 0:
                            chance += 1
                        if nums[i] <= nums[i-1] or nums[i] - nums[i-1] > 3:
                            if prev != -1 and nums[i] > prev and nums[i] - prev <= 3 and chance == 2:
                                prev = -1
                                continue
                            violations += 1
                            if violations > 1:
                                return False
                            # 跳過i-1 or 跳過i
                            if (i > 1 and (nums[i] <= nums[i - 2] or nums[i] - nums[i - 2] > 3)) and (i + 1 < len(nums) and (nums[i + 1] <= nums[i - 1] or nums[i + 1] - nums[i - 1] > 3)):
                                return False
                            if i-1 >= 0 and i + 1 < len(nums) and not(nums[i + 1] <= nums[i - 1] or nums[i + 1] - nums[i - 1] > 3):
                                prev = nums[i-1]
                                chance = 1
                    return True

                def decreasing(nums):
                    violations = 0
                    prev = -1
                    chance = 0
                    for i in range(1, len(nums)):
                        if chance != 0:
                            chance += 1
                        if nums[i] >= nums[i-1] or nums[i-1] - nums[i] > 3:
                            if prev != -1 and nums[i] < prev and prev - nums[i] <= 3 and chance == 2:
                                prev = -1
                                continue
                            violations += 1
                            if violations > 1:
                                return False
                            # 跳過i-1 or 跳過i
                            if (i > 1 and (nums[i] >= nums[i - 2] or nums[i - 2] - nums[i] > 3)) and (i + 1 < len(nums) and (nums[i + 1] >= nums[i - 1] or nums[i - 1] - nums[i + 1] > 3)):
                                return False
                            if i-1 >= 0 and i + 1 < len(nums) and not (nums[i + 1] >= nums[i - 1] or nums[i - 1] - nums[i + 1] > 3):
                                prev = nums[i-1]
                                chance = 1
                    return True
                if(increasing(nums) or decreasing(nums)):
                    count += 1
                def helper(nums):
                    n = len(nums)
                    pre_inc = [1] * n
                    pre_dec = [1] * n
                    suf_inc = [1] * n
                    suf_dec = [1] * n

                    for i in range(1, n):
                        if 0 < nums[i] - nums[i - 1] <= 3:
                            pre_inc[i] = pre_inc[i - 1] + 1
                        if 0 < nums[i - 1] - nums[i] <= 3:
                            pre_dec[i] = pre_dec[i - 1] + 1

                    for i in range(n - 2, -1, -1):
                        if 0 < nums[i] - nums[i + 1] <= 3:
                            suf_dec[i] = suf_dec[i + 1] + 1
                        if 0 < nums[i + 1] - nums[i] <= 3:
                            suf_inc[i] = suf_inc[i + 1] + 1

                    if suf_dec[1] == n - 1 or suf_inc[1] == n - 1:  # 移除第一個元素
                        return True
                    if pre_dec[-2] == n - 1 or pre_inc[-2] == n - 1:  # 移除最後一個元素
                        return True

                    for i in range(1, n - 1):
                        if (pre_dec[i - 1] + suf_dec[i + 1] == n - 1 and 
                            nums[i - 1] - nums[i + 1] <= 3 and nums[i - 1] > nums[i + 1]):
                            return True
                        if (pre_inc[i - 1] + suf_inc[i + 1] == n - 1 and 
                            nums[i + 1] - nums[i - 1] <= 3 and nums[i + 1] > nums[i - 1]):
                            return True

                    return False

                if helper(nums):
                    count_2 += 1
                

                # if check(nums):
                #     count += 1
                #     continue
                # else:
                #     for i in range(len(nums)):
                #         mod_nums = nums[:i] + nums[i+1:]
                #         if(check(mod_nums)):
                #             count += 1
                #             break         
            print(count)
            print(count_2)
        except Exception as e:
            print(e)
    