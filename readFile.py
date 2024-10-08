import sys
from elfheader import elfheader
if(len(sys.argv) < 2):
	print("usage: readFile.py <file>")
	exit(0)

targetFile = open(sys.argv[1], "rb")

ba = bytearray(targetFile.read())
header = elfheader(ba)
print("trying to print header, fingers crossed!\n")
print(header)

header.serialize()
exit(0)

for pheader in header.pheaders:
	if(pheader.ptype == 1):
		print("\n\nprinting section: " + str(pheader.ptype))
		print("\ntheoretically starting at vaddr: " + hex(0x4e8 + pheader.vaddr) + "\n")
		i = pheader.poffset + 0x4e8
		while(i < pheader.memsz + pheader.poffset):
			output = ""
			for ln in range(0,10):
				output += hex(ba[i + ln]) + " "
			print(output)
			i += 10
		
		
