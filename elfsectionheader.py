from byteParse import byteparser

class sectionheader:
    
    def getName(self, byteArr, shstrndx):

        strEndIndex = self.name + shstrndx

        while(byteArr[strEndIndex] != 0):
            strEndIndex += 1

        nameBytes = byteArr[self.name + shstrndx:strEndIndex]
        name = nameBytes.decode("utf-8")
        return name

    def __init__(self, byteArr, offset):

        self.thissecheaderoffset = offset #where in the file is this sectionheader?
        self.thissecheaderindex = 0         #what section header index is this sectionheader?

        self.bytes = byteArr[offset:offset + 0x40]
        self.name = byteparser.parseBytes(byteArr, offset + 0x0, 4)
        self.shtype = byteparser.parseBytes(byteArr, offset + 0x4, 4)
        self.flags = byteparser.parseBytes(byteArr, offset + 0x8, 8)
        self.addr = byteparser.parseBytes(byteArr, offset + 0x10, 8)
        self.offset = byteparser.parseBytes(byteArr, offset + 0x18, 8)
        self.size = byteparser.parseBytes(byteArr, offset + 0x20, 4)
        self.link = byteparser.parseBytes(byteArr, offset + 0x28, 4)
        self.info = byteparser.parseBytes(byteArr, offset + 0x2c, 4)
        self.align = byteparser.parseBytes(byteArr, offset + 0x30,8)
        self.entsize = byteparser.parseBytes(byteArr, offset + 0x38, 8)
        self.namestr = None

        self.isshoff = False #is this the section header related to the section name strings?

    def setOffset(self, newOffset):
        self.offset = newOffset
        self.bytes[0x18: 0x20] = byteparser.toBytes(newOffset, 8)
    
    def setIndex(self, newIndex):
        this.thissecheaderindex = newIndex

    def setLink(self, newLink):
        self.bytes[0x28: 0x2c] = byteParse.toBytes(newLink, 4)

    def setName(self, newname):
        self.offname = newname
        self.bytes[0x0: 0x4] = byteparser.toBytes(newname, 4)

    def size():
        return 0x40
    
    #offset here should be an offset to the strtable that holds all the names
    def initName(self, byteArr, offset):
        self.namestr = self.getName(byteArr, offset)

    def __str__(self):
        output = "name: " + self.namestr
        output += "\ntype: " + str(self.shtype)
        output += "\nvaddr: " + hex(self.addr)
        output += "\noffset: " + hex(self.offset)
        output += "\nsize: " + hex(self.size)
        output += "\nlink: " + hex(self.link)
        output += "\nalign: " + hex(self.align)
        return output
        