from assembler import assemble
from sys import argv

if len(argv) == 1:
    machine_code = assemble(open(input("File to assemble: ")))
    output_location = input("Where to save (leave empty to put in console): ")
    print("How to represent machine code:")
    print("1. Bytes", "2. Base 10", "3. Base 2")
    representation = input()

    output = ""

    if(representation == "1"):
        output = bytearray()
        for n in machine_code:
            output.extend(n.to_bytes(2, byteorder="big"))

    elif(representation == "2"):
        output = " ".join(map(str, machine_code))
    elif(representation == "3"):
        output = " ".join(map(lambda x: format(x, '016b'), machine_code))
    
    if output_location == "":
        print(output)
    else:
        if type(output) is str:
            with open(output_location) as file:
                file.write(output)
        elif type(output) is bytearray:
            with open(output_location, "wb") as file:
                file.write(bytes(output))