"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):
        return (0, False)

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(program) as f:
            for line in f:
                comment_split = line.split('#')
                number = comment_split[0].strip()

                try:
                    self.ram_write(int(number, 2), address)
                    address += 1
                except ValueError:
                    pass

        for instruction in program:
            self.ram[address] = instruction
            address += 1

      

    def alu(self, operation, int_a, int_b):
        

        if operation == "ADD":
            self.reg[int_a] += self.reg[int_b]
        elif operation == "MUL":
            self.reg[int_a] = (self.reg[int_a] * self.reg[int_b])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                operation_output = self.commands[ir](operand_a, operand_b)
                running = operation_output[1]
                self.pc += operation_output[0]

            except:
                print(f"Unknown command: {ir}")
                sys.exit()