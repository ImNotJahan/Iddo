import os

print("Please select one of the following components to test:")
print("0. Half adder", "1. Full adder", "2. Byte adder", "3. 16 bit adder")
selection = input("Number: ")
with_gtk = input("Would you like to view in gtkwave? y/n: ")

dir_path = os.path.dirname(os.path.realpath(__file__))
command = "cd " + dir_path + " && cd {location} && iverilog -c requirements.txt tb/{component}.v && vvp a.out"

if with_gtk == "y": 
    command += " && gtkwave test.vcd"

location = ""

match selection:
    case "0":
        location = "bit/math"
        os.system(command.format(location=location, component="half_adder"))
    case "1":
        location = "bit/math"
        os.system(command.format(location=location, component="full_adder"))
    case "2":
        location = "octet/math"
        os.system(command.format(location=location, component="add8"))
    case "3":
        location = "doublet/math"
        os.system(command.format(location=location, component="add16"))

# delete temporary testing files
os.remove(dir_path + "/" + location + "/a.out")
os.remove(dir_path + "/" + location + "/test.vcd")