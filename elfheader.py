from byteParse import byteparser
from elfpheader import elfpheader
from elfsectionheader import sectionheader

class elfheader:


    def __init__(self, byteArr):

        self.bytes = byteArr[0:0x40]

        self.magnum = byteparser.parseBytes(byteArr, 0,4)       #magic number, declares that this is an elf file
        self.byteness = byteparser.parseBytes(byteArr, 4, 1)    #is this a 32 or 64 bit file
        self.endianness = byteparser.parseBytes(byteArr, 5, 1)  #little or big endian
        self.version = byteparser.parseBytes(byteArr, 6, 1)     #What version elf file is this
        self.osabi = byteparser.parseBytes(byteArr, 7, 1)       #What OS ABI is this file targeting
        self.abiversion = byteparser.parseBytes(byteArr, 8, 1)  #Further specify ABI version
        self.pad = byteparser.parseBytes(byteArr, 9, 7)         #reserved padding bytes
        self.objtype = byteparser.parseBytes(byteArr, 0x10, 2)  #object file type (executable, library, etc)
        self.machine = byteparser.parseBytes(byteArr, 0x12, 2)
        self.eversion = byteparser.parseBytes(byteArr, 0x14, 4)
        self.entry = byteparser.parseBytes(byteArr, 0x18, 8)
        self.phoff = byteparser.parseBytes(byteArr, 0x20, 8)
        self.shoff = byteparser.parseBytes(byteArr, 0x28, 8)
        self.flags = byteparser.parseBytes(byteArr, 0x30, 4)
        self.ehsize = byteparser.parseBytes(byteArr, 0x34, 2)
        self.phentsize = byteparser.parseBytes(byteArr, 0x36,2)
        self.phnum = byteparser.parseBytes(byteArr, 0x38,2)
        self.shentsize = byteparser.parseBytes(byteArr, 0x3a, 2)
        self.shnum = byteparser.parseBytes(byteArr, 0x3c, 2)
        self.shstrndx = byteparser.parseBytes(byteArr, 0x3e,2)
    
        self.fileLength = len(byteArr)

        self.pheaders = []
        self.secheaders = []

        #read program headers
        for i in range(0,self.phnum):
            self.pheaders.append(elfpheader(byteArr, self.phoff + i * self.phentsize))

        #initialize section headers
        for i in range(0, self.shnum):
            self.secheaders.append(sectionheader(byteArr, self.shoff + i * self.shentsize))

        #once we've loaded them all, that means we've loaded the header for the 
        #section name table. grab that offset
        nameoffset =  self.secheaders[self.shstrndx].offset

        #get section names from section name table
        for i in range(0, self.shnum):
            self.secheaders[i].initName(byteArr, nameoffset)

    def setphoff(self, newoffset):
        self.phoff = newoffset
        self.bytes[0x20:0x28] = byteparser.toBytes(newoffset, 8)
    
    def setshoff(self,newoffset):
        self.shoff = newoffset
        self.bytes[0x28:0x30] = byteparser.toBytes(newOffset, 8)
    
    def setshstrindex(self,newindex):
        self.shstrndx = newindex
        self.bytes[0x3e:0x40] = byteparser.toBytes(newindex,2)

    def __str__(self):
        output = ""
        output += "byteness: " + "64" if self.byteness == 2 else "32"
        output += "\nendianness: " + ("little" if self.endianness == 1 else "big")
        output += "\nfile type: " + ("exe" if self.objtype == 2 else "else")
        output += "\nprogram header offset: " + hex(self.phoff)
        output += "\nsize of a program header entry: " + hex(self.phentsize)
        output += "\nnumber of pheader entries: " + str(self.phnum)
        output += "\nnumber of section header entries: " + str(self.shnum)
        output += "\nsection header offset: " + str(self.shoff)
        output += "\nsection header entry size: " + hex(self.shentsize)
        output += "\nindex of section header table entry: " + str(self.shstrndx)
        output += "\nentry point: " + hex(self.entry)

        for phdrentry in self.pheaders:
            output += "\n\n"
            output += str(phdrentry)
        
        for sechentry in self.secheaders:
            output += "\n\n"
            output += str(sechentry)

        return output
    
    def fixupHeaders(self):
        return 0
        #take the newly ordered headers and resolve their references to one another

    def randomize(self):
        #shuffle the headers then fix them up
        #I think if I just shuffle the pheaders, I should still end up with a valid elf
        self.pheaders.shuffle()
    

    def serialize(self):
       with open("a-changed.out", "wb") as outfile:
            
            #idk, let's give it a shot
            self.randomize()

            output = bytearray([0] * (self.fileLength + 4))
            self.setphoff(self.phoff + 4)
            output[0:0x40] = self.bytes
            index = 0x40
                        
            for phdr in self.pheaders:
                output[index:(index + self.phentsize)] = phdr.bytes
            
            for phdr in self.pheaders:
                output[phdr.poffset: (phdr.poffset + phdr.memsz)] = phdr.sectionBytes

            for i in range(0, len(self.secheaders)):
                curroff = self.shoff + i * 0x40
                output[curroff:curroff + 0x40] = self.secheaders[i].bytes
            
            outfile.write(output)

            

        