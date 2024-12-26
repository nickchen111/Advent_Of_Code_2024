import requests

def fetch_data_from_url(url):
    response = requests.get(url, cookies={"session": "53616c7465645f5f4954a0b4a72309ac4accc8385d62ab6d3009090e3ed32b7409d587cc36e90de3acb9636c5852563f485c522b25189618be728ce56b21be09"})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def execute_program(program, registers):
    # 解析程序與寄存器初始化
    instruction_pointer = 0
    output = []
    n = len(program)
    
    while instruction_pointer < n:
        # 獲取操作碼與操作數
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        
        # 定義組合操作數解析
        def resolve_operand(op):
            if op == 4:  # Register A
                return registers['A']
            elif op == 5:  # Register B
                return registers['B']
            elif op == 6:  # Register C
                return registers['C']
            elif op < 4:  # Literal values 0-3
                return op
            else:
                raise ValueError(f"Invalid operand: {op}")

        # 按操作碼執行對應指令
        if opcode == 0:  # adv: A = A // (2^operand)
            denominator = 2 ** resolve_operand(operand)
            registers['A'] //= denominator
        
        elif opcode == 1:  # bxl: B = B ^ operand
            registers['B'] ^= operand
        
        elif opcode == 2:  # bst: B = operand % 8
            registers['B'] = resolve_operand(operand) % 8
        
        elif opcode == 3:  # jnz: Jump if A != 0
            if registers['A'] != 0:
                instruction_pointer = operand
                continue  # 跳過指針更新
        
        elif opcode == 4:  # bxc: B = B ^ C
            registers['B'] ^= registers['C']
        
        elif opcode == 5:  # out: Output operand % 8
            output.append(resolve_operand(operand) % 8)
        
        elif opcode == 6:  # bdv: B = A // (2^operand)
            denominator = 2 ** resolve_operand(operand)
            registers['B'] = registers['A'] // denominator
        
        elif opcode == 7:  # cdv: C = A // (2^operand)
            denominator = 2 ** resolve_operand(operand)
            registers['C'] = registers['A'] // denominator
        
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        # 更新指令指針
        instruction_pointer += 2

    return ",".join(map(str, output))

program = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]
registers = {'A': 28066687, 'B': 0, 'C': 0}

result = execute_program(program, registers)
print("Output:", result)
