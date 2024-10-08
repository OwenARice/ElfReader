from byteParse import byteparser


class elfpheader:

    def __init__(self, byteArr, offset):
        
        self.bytes = byteArr[offset:offset + 0x38]

        self.thispheaderoffset = offset  # where in the file is this pheader located?

        self.ptype = byteparser.parseBytes(byteArr, offset + 0x0, 4)
        self.flags = byteparser.parseBytes(byteArr, offset + 0x4, 4)
        self.poffset = byteparser.parseBytes(byteArr, offset + 0x8, 8) #where in the file are the bytes associated with this pheader?
        self.vaddr = byteparser.parseBytes(byteArr, offset + 0x10, 8)
        self.paddr = byteparser.parseBytes(byteArr, offset + 0x18, 8)
        self.filesz = byteparser.parseBytes(byteArr, offset + 0x20, 8)
        self.memsz = byteparser.parseBytes(byteArr, offset + 0x28, 8)
        self.align = byteparser.parseBytes(byteArr, offset + 0x30, 8)

        self.sectionBytes = byteArr[self.poffset:self.poffset + self.memsz]

    def setOffset(self, newOffset):
        self.poffset = newOffset
        self.bytes[0x8: 0x10] = byteparser.toBytes(newOffset, 8)

    def size():
        return 0x38

    def isPhdr(self):
        return (self.ptype == 6)
    

    def __str__(self):
        types = ["null", "Load", "dynamic", "interp", "note", "shlib", "phdr", "tls"]
        type = "other"
        if self.ptype < 8:
            type = types[self.ptype]
        
        output = "type: " + type
        output += "\nflags: " + hex(self.flags)
        output += "\noffset: " + hex(self.poffset)
        output += f"\nsection covers bytes : {self.poffset} to {self.poffset + self.memsz}"
        output += "\nvirtual address: " + hex(self.vaddr)
        output += "\nphysical address: " + hex(self.paddr)
        output += "\nsegment size in on disk: " + hex(self.filesz)
        output += "\nsegment size in memory: " + hex(self.memsz)
        output += "\nallign: " + hex(self.align)

        return output
