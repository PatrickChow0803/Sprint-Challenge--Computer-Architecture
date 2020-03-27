"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.pc = 0                 #program counter
        self.ram = [0] * 256        # memory

        self.registers = [0] * 8    # registers
        self.flags = [0] * 3

        self.filename = filename    # data file

    def load(self):
        """Load a program into memory."""
        address = 0
        try:
            with open(self.filename) as file:
                for line in file:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                        self.ram[address] = val
                        address += 1
                    except ValueError:
                        # print("warning: value cannot be translated as int")
                        continue

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file not found")
            sys.exit(1)

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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:

            LDI = 0b10000010 # 130 - Set the value of a register to an integer.
            PRN = 0b01000111 # 71  - Print numeric value stored in the given register.
            CMP = 0b10100111 # 167 - Compare the values in two registers.

            # FL bits: 00000LGE
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.

            JMP = 0b01010100 # 84 - Jump to the address stored in the given register.
            JEQ = 0b01010101 # 85 - If E flag is set (true), jump to the address stored in the given register.
            JNE = 0b01010110 # 86 - If E flag is clear (false, 0), jump to the address stored in the given register.

            # IR = Instruction Register
            IR = self.ram[self.pc]
            op1 = self.ram[self.pc+1]
            op2 = self.ram[self.pc+2]

            # Set the value of a register to an integer.
            if IR == LDI:

                self.registers[op1] = op2
                self.pc += 3

            # Print numeric value stored in the given register.
            elif IR == PRN:
                print(self.registers[op1])
                self.pc += 2

            # Compare two different registers and change the value of the flags accordingly.
            # FL bits: LGE
            elif IR == CMP:
                # If registers are equal, set E flag to true, else false.
                if self.registers[op1] == self.registers[op2]:
                    self.flags[2] = 1
                else:
                    self.flags[2] = 0

                # If first register is less than second register, set L flag to true, else false
                if self.registers[op1] < self.registers[op2]:
                    self.flags[0] = 1
                else:
                    self.flags[0] = 0

                # If first register is greater than second register, set G flag to true, else false
                if self.registers[op1] > self.registers[op2]:
                    self.flags[1] = 1
                else:
                    self.flags[1] = 0

                self.pc += 3

            # Jump to the address stored in the given register.
            elif IR == JMP:
                self.pc = self.registers[op1]

            # If E flag is set (true/equal), jump to the address stored in the given register.
            elif IR == JEQ:
                if self.flags[2] == 1:
                    self.pc = self.registers[op1]
                else:
                    self.pc += 2

            # If E flag is clear (false/unequal, 0), jump to the address stored in the given register.
            elif IR == JNE:
                if self.flags[2] == 0:
                    self.pc = self.registers[op1]
                else:
                    self.pc += 2
            else:
                running = False
