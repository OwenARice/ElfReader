class byteparser:

    #given a bytearray of a little endian number, convert and return a single number
    def parseBytes(byteArr, start, len):
        num = 0
        for i in range(0,len):
            num *= 256
            num += byteArr[start - i + len - 1]
        return num
    
    #given a number and a number of bytes to fill, convert that number to a little endian byte array
    def toBytes(number, numbytes):
        bytearr = []
        num = number
        for i in range(0, numbytes):
            bytearr.insert(0,num % 256)
            num = int(num/256)
        
        return bytearray(bytearr)