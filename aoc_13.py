import requests
from fractions import Fraction
import re


def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
# 問說 B操作需要花1coin Ａ操作需要3 coin 給你很多的娃娃機 算出他們需要花費的最少coin 相加總和是多少 也會有無法操作到指定位置的 那種就不理他
B_COST = 1
A_COST = 3
OFFSET = 10000000000000
def day_thirteen_part1(buttonA: list, buttonB: list, prizes: list):
    ret = 0
    for i in range(len(prizes)):
        x, y = 0, 0
        for j in range(100,-1,-1):
            x = buttonB[i][0] * j
            y = buttonB[i][1] * j
            if x > prizes[i][0] or y > prizes[i][1]:
                continue
            diffx, diffy = prizes[i][0] - x, prizes[i][1] - y
            if diffx % buttonA[i][0] == 0 and diffy % buttonA[i][1] == 0:
                steps_a_x = diffx // buttonA[i][0]
                steps_a_y = diffy // buttonA[i][1]
                if steps_a_x == steps_a_y:
                    ret += B_COST * j + A_COST * steps_a_x
                    break
    print(ret)

def day_thirteen_part2(buttonA: list, buttonB: list, prizes: list):
    """
    Solves a 2x2 system of linear equations using matrix inversion method.

    The system of equations is:
        aa_x + bb_x = px
        aa_y + bb_y = py

    e. g.
        94a + 22b = 8400
        34a + 67b = 5400

        (a, b) = (80, 40)

    Reference:
    https://en.m.wikipedia.org/wiki/System_of_linear_equations#Matrix_solution
    """
    ret = 0
    for i in range(len(prizes)):
        ax, ay = buttonA[i][0], buttonA[i][1]
        bx, by = buttonB[i][0], buttonB[i][1]
        px,py = prizes[i][0] + OFFSET, prizes[i][1] + OFFSET
        det = ax * by - ay * bx
        A_inverse = [
            [Fraction(by, det), Fraction(-bx, det)],
            [Fraction(-ay, det), Fraction(ax, det)],
        ]

        a = A_inverse[0][0] * px + A_inverse[0][1] * py
        b = A_inverse[1][0] * px + A_inverse[1][1] * py

        # check if a or b has denominator different than 1
        if a.denominator != 1 or b.denominator != 1:
            continue
        ret += 3 * int(a) + 1 * int(b)
    print(ret)


if __name__ == "__main__":
    url = 'https://adventofcode.com/2024/day/13/input'
    input_data = fetch_data_from_url(url)
    # 正則表達式提取資料
    pattern = r"Button A: X\+(-?\d+), Y\+(-?\d+)\nButton B: X\+(-?\d+), Y\+(-?\d+)\nPrize: X=(-?\d+), Y=(-?\d+)"
    matches = re.findall(pattern, input_data)

    buttonA = []
    buttonB = []
    prizes = []

    for match in matches:
        ax, ay, bx, by, px, py = map(int, match)
        buttonA.append((ax, ay))
        buttonB.append((bx, by))
        prizes.append((px, py))
    # print(buttonB)
    day_thirteen_part1(buttonA, buttonB, prizes)
    day_thirteen_part2(buttonA, buttonB, prizes)
    
    