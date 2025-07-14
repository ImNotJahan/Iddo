import sys
from vm import VM

args = sys.argv[1:]

if len(args) == 0:
    file = input("What file would you like to run? ")
else:
    file = args[0]

machine = VM()

code = []

with open(file, "rb") as file:
    while bytes := file.read(2):
        code.append(int.from_bytes(bytes, byteorder='big'))

machine.set_program(code)
machine.run()