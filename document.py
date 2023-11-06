import requests
import os
import json

class TextDocument:
    def __init__(self) -> None:
        self.bytes=[]
        self.metadata={}

    def getBytes(self)->bytes:
        return bytes(self.bytes)
    
    def openFile(self,filename):
        try:
            with open(filename, "rb") as file:
                self.bytes = list(file.read())

            self.metadata={
                "File Size": os.path.getsize(filename),
                "Last Modified Time": os.path.getmtime(filename),
                "Creation Time": os.path.getctime(filename),
                "Last Access Time": os.path.getatime(filename),
            }

            return True
        except:
            return False
        
    def getMetadata(self):
        return self.metadata

    def openURL(self,url):

        try:
            result=requests.get(url)
            self.metadata=dict(result.headers)
            self.bytes=result.content
            
            return True
        except:
            return False

    def insertByte(self,position:int,value:int):
        self.bytes.insert(position,value)

    def setByte(self,position:int,value:int):
        self.bytes[position]=value

    def deleteByte(self,position:int):
        self.bytes.pop(position)

    def writeFile(self,path):
        try:
            with open(path,"wb") as file:
                file.write(bytes(self.bytes))
            return True
        except:
            return False
        
    def writeMetadata(self,path):
        try:
            with open(path,"w") as file:
                file.write(json.dumps(self.metadata))
            return True
        except:
            return False