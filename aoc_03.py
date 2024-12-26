import requests

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    # 第三天 字串匹配遊戲 
    url = "https://adventofcode.com/2024/day/3/input"
    def day_three(url):
        try:
            input_data = fetch_data_from_url(url)
            n = len(input_data)
            res = 0
            str1 = "mul("
            str2 = "don't()"
            str3 = "do()"
            validation = True
            for i in range(n - 3):
                if input_data[i:i+4] == str1 and validation == True:
                    j = i + 4
                    num1 = None
                    num2 = None
                    while j < n and input_data[j] != ',' and input_data[j].isdigit():
                        if num1 == None:
                            num1 = 0
                        num1 = num1*10 + int(input_data[j])
                        j += 1
                    if j >= n or input_data[j] != ',':
                        i = j-1
                        continue
                    j += 1
                    while j < n and input_data[j] != ')' and input_data[j].isdigit():
                        if num2 == None:
                            num2 = 0
                        num2 = num2*10 + int(input_data[j])
                        j += 1
                    if j >= n or input_data[j] != ')':
                        i = j-1
                        continue
                    else:
                        res += num1*num2
                        i = j
                elif i+6 < n and input_data[i:i+7] == str2:
                    validation = False
                    i += 6
                elif input_data[i:i+4] == str3:
                    validation = True
                    i += 3
            print(res)

        except Exception as e:
            print(e)