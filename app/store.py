import os
from shared import utils

class KeyStore:
    def __init__(self):
        self.store = {}
        self.dataFolder = os.getcwd()

    def load(self, folder):
        self.dataFolder = folder
        fp = os.path.join(folder, 'store.yml')
        if os.path.exists(fp):
            self.store = utils.loadYaml(fp)
            print(f"Store loaded {len(self.store)} keys")
            for key in self.store.keys():
                print(key)
        else:
            print(f"Store file not found: {fp}")
    
    def getString(self, key):
        if key in self.store:
            return self.store[key]
        else:
            print(f"key [{key}] not found in store")
            for k in self.store.keys():
                print(f"{k} <> {key} {k == key}")
        return None
        
    def deleteAll(self):
        keys = len(self.store)
        self.store.clear()
        self.save()
        return { 'deleted_count': keys }

    def setString(self, key, value):
        self.store[key] = value
        self.save()
        return { key: value }

    def save(self):
        fp = os.path.join(self.dataFolder, 'store.yml')
        utils.writeYaml(self.store, fp)

    def getAll(self):
        return self.store
    