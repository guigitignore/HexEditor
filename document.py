
class TextDocument:
    def __init__(self) -> None:
        self.bytes=[]

    def getBytes(self)->bytes:
        return bytes(self.bytes)
    
    def openFile(self,filename):
        with open(filename, "rb") as file:
            self.bytes = list(file.read())

    def insertByte(self,position:int,value:int):
        self.bytes.insert(position,value)

    def setByte(self,position:int,value:int):
        self.bytes[position]=value

    def deleteByte(self,position:int):
        self.bytes.pop(position)