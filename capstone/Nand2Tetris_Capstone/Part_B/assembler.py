
import sys

comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

dest_table = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_table = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def clean_code(filename):
    instructions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.split("//")[0].strip()

            if line:
                instructions.append(line)

    return instructions


def build_symbol_table(instructions):
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2,
        "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }

    for i in range(16):
        symbols[f"R{i}"] = i

    rom_address = 0
    for instruction in instructions:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]
            symbols[label] = rom_address
        else:
            rom_address += 1

    return symbols


def assemble(instructions):
    for instruction in instructions:
        if instruction.startswith("@"):
            value = int(instruction[1:])
            print(format(value, "016b"))
        else:
            dest = ""
            jump = ""

            if "=" in instruction:
                dest, instruction = instruction.split("=")

            if ";" in instruction:
                instruction, jump = instruction.split(";")

            comp = instruction

            binary = (
                "111"
                + comp_table[comp]
                + dest_table[dest]
                + jump_table[jump]
            )

            print(binary)



if __name__ == "__main__":
    filename = sys.argv[1]
    instructions = clean_code(filename)

    output_file = filename.replace(".asm", ".hack")

    with open(output_file, "w") as file:
        original_stdout = sys.stdout
        try:
            sys.stdout = file
            assemble(instructions)
        finally:
            sys.stdout = original_stdout

    print("Assembly completed:", output_file)
