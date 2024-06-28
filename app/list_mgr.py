import os
from shared import utils


class ListManager:
    def __init__(self):
        self.listMap = {}
        self.dataFolder = os.path.join(os.getcwd(), 'lists')

    def getAt(self, listId: str, index: int):
        if (listId in self.listMap) == False:
            return None
        items = self.listMap[listId]
        if index >= len(items):
            return None
        return items[index]
    
    def append(self, listId: str, item: any):
        if listId in self.listMap:
            self.listMap[listId].append(item)
        else:
            self.listMap[listId] = [item]
        self.saveList(listId)
        return len(self.listMap[listId])
    
    def removeAt(self, listId: str, index: int):
        if listId in self.listMap:
            del self.listMap[listId][index]
            self.saveList(listId)
            return len(self.listMap[listId])
        return 0
    
        
    def saveList(self, listId: str):
        print(f"Save list: {listId}...")
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)

        fp = os.path.join(self.dataFolder, f'{listId}.yaml')
        utils.writeYaml(self.listMap[listId], fp)

    def loadList(self, listId: str):
        print(f"Load list: {listId}...")
        fp = os.path.join(self.dataFolder, f'{listId}.yaml')
        self.listMap[listId] = utils.loadYaml(fp)


    def load(self):
        if os.path.exists(self.dataFolder):
            files = os.listdir(self.dataFolder)
            for f in files:
                fName, ext = f.split('.')
                self.loadList(fName)