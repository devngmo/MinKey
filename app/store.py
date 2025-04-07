import os, shutil
from shared import utils

class KeyStore:
    def __init__(self, autoSave = True, traceEnabled = False):
        self.store = { '/': {} }
        self.autoSave =autoSave
        self.dataFolder = os.getcwd()
        self.traceEnabled = traceEnabled

    def scanAndLoad(self, relativePath: str = '', indent = ''):
        keyPrefix = relativePath.replace("\\", '/')
        
        if relativePath == '': # root
            fp = os.path.join(self.dataFolder, 'store.yml')
            keyPrefix = '/'

        fp = os.path.join(self.dataFolder, relativePath, 'store.yml')
        if not os.path.exists(fp):
            return
        
        if self.traceEnabled:
            print(f"[SCAN]{indent}{relativePath}...")

        if os.path.exists(fp):
            m = utils.loadYaml(fp)
            keySet = {}
            if keyPrefix in self.store:
                keySet = self.store[keyPrefix]
            for key in m.keys():
                keySet[key] = m[key]
                
            self.store[keyPrefix] = keySet

            if self.traceEnabled:
                print(f"  loaded {len(self.store)} keys")
                for key in keySet.keys():
                    print(f"  {key}: {keySet[key]}")
        else:
            print(f"Store file not found: {fp}")
        
        subDirs = os.listdir(os.path.join(self.dataFolder, relativePath))
        for subDir in subDirs:
            self.scanAndLoad(os.path.join(relativePath, subDir), indent + '  ')

    def load(self, storeFolder):
        self.dataFolder = storeFolder
        if self.traceEnabled:
            print(f"DataFolder: {self.dataFolder}")
        self.scanAndLoad()
        
    def parseKeyAndGetKeyset(self, key: str):
        parts = key.split('/')
        keyset = {}
        if len(parts) == 1:
            keyset = self.store['/']
            if self.traceEnabled:
                print(f"parseKeyAndGetKeyset: {key}, {parts[0]}")
                print(keyset)
            return '/', parts[0], keyset
        else:
            prefix = '/'.join( parts[:-1] )            
            if prefix in self.store:
                keyset = self.store[prefix]
            
            if self.traceEnabled:
                print(f"parseKeyAndGetKeyset: {prefix}, {parts[len(parts)-1]}")
                print(keyset)
            return prefix, parts[len(parts)-1], keyset
    
    def getString(self, key: str):
        path, keyName, keyset = self.parseKeyAndGetKeyset(key)

        if keyName in keyset:
            return keyset[keyName]
        
        if self.traceEnabled:
            print(f"key [{key}] not found in store")
        return None

    def deleteKeyFolder(self, keyPath: str):
        relativePath = keyPath.replace('/', '\\')
        print(f"DELETE: {keyPath}/*")
        shutil.rmtree(os.path.join(self.dataFolder, relativePath))
        self.store[relativePath] = {}
        keys = self.store.keys()
        for k in keys:
            if k.startswith(relativePath):
                print(f"DELETE: {k}/*")
                del self.store[k]

    def deleteAll(self):
        print("DELETE ALL")
        shutil.rmtree(self.dataFolder)
        self.store.clear()

    def setString(self, key, value):
        path, keyName, keyset = self.parseKeyAndGetKeyset(key)
        keyset[keyName] = value
        self.store[path] = keyset

        if self.autoSave:
            self.saveKeyFolder(path)
        return { key: value }

    def saveKeyFolder(self, keyPath: str):
        relativePath = keyPath.replace('/', '\\')
        folderPath = self.dataFolder +"\\" + relativePath
        if relativePath == "\\":
            folderPath = self.dataFolder

        if self.traceEnabled:
            print(f"dataFolder: {self.dataFolder}")
            print(f"folderPath: {folderPath}")

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        fp = os.path.join(folderPath, 'store.yml')
        if self.traceEnabled:
            print(f"SAVE: {fp}")
        m = self.store[keyPath]
        utils.writeYaml(m, fp)

    