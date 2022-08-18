from sys import argv, exit, stderr

if len(argv) != 3:
	print("USAGES: python3 overflow_signed_8bits.py <number1> <number2>", file=stderr)
	exit(1)
	
_, number1, number2 = argv

get_digits = lambda x: x[1:] if x.startswith("-") else x
is_8bit_signed = lambda x: 127 >= x >= -128
get_signed = lambda x, b: "1" + binary_add("0" + b[3:][-7:].rjust(7, "0").replace("0", "2").replace("1", "0").replace("2", "1"), "10000001")[0][1:] if x < 0 else "0" + b[2:].rjust(7, "0")

def binary_add(n1, n2):
	p = 0
	r = ""
	l = len(n1)
	
	if l != len(n2):
		raise ValueError(f"n1 ({n1}) and n2 ({n2}) don't have the same length.")
	
	n2 = n2[::-1]
	for i, value in enumerate(n1[::-1]):
		n = int(value) + int(n2[i]) + p
		if n > 1:
			r += "1" if n % 2 else "0"
			p = 1
		elif n:
			r += "1"
			p = 0
		else:
			p = 0
			r += "0"
			
	return r[::-1], p
	
def get_binary_result(result):
	if result[0] == "1":
		return "-" + str(128 - int(result[1:], 2))
	else:
		return "+" + str(int(result[1:], 2))

n1_d = get_digits(number1)
n2_d = get_digits(number1)

if not n1_d.isdigit() or not n2_d.isdigit():
	print("<number1> and <nulber2> must be digits.", file=stderr)
	exit(2)

number1 = int(number1)
number2 = int(number2)

if not is_8bit_signed(number1) or not is_8bit_signed(number2):
	print("<number1> and <number2> must be a 8 bit signed number (an integer between -128 and 127)", file=stderr)
	exit(3)

n1_b = bin(number1)
n2_b = bin(number2)

n1_b = get_signed(number1, n1_b)
n2_b = get_signed(number2, n2_b)

result, carry = binary_add(n1_b, n2_b)

print(" ", n1_b)
print("+", n2_b)
print("_" * 10)
print(" ", result)

sign_n1_b = n1_b[0]
sign_n2_b = n2_b[0]
sign_r = result[0]

if carry:
	print("\n[*] There is a carry.")

if sign_n1_b != sign_n2_b:
	print(("" if carry else "\n") + "[*] There is no overflow possible because numbers are signed differently.")
elif sign_n2_b == sign_r:
	print(("" if carry else "\n") + "[+] There is no overflow in this addition.")
else:
	print(("" if carry else "\n") + "[!] There is an overflow in this addition !")

print(f"\nBase 10 result:", number1, "+", number2, "=", get_binary_result(result))
