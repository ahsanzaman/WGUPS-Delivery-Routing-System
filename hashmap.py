class HashMap:
    def __init__(self):
        self.size = 10
        self.map = []
        for i in range(self.size):
            self.map.append([])

    # generates a hash according to the size set
    def get_hash(self, key):
        key_hash = 0
        key_str = str(key)
        for char in key_str:
            key_hash += ord(char)
        return key_hash % self.size

    # codebasics video on Hash Table implementation and magic methods.
    # Using the methods below allow us to treat this class similar to a dictionary.
    # Python Creating a HASHMAP using Lists video for tutorial on how to chain hashtables.

    # setting items with key, value pairs
    # each value is set to a hash which is generated from the key
    def __setitem__(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = value
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # insert function leveraging setter for this class
    def insert_item(self, key, value):
        return self.__setitem__(key, value)

    # hash is generated with the key
    # key is compared with each hash to get the exact item
    def __getitem__(self, key):
        key_str = str(key)
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key_str:
                    return pair[1]
        return None

    # lookup function leveraging getter for this class
    def lookup_item(self, key):
        return self.__getitem__(key)

    # finds item by getting hash from key and then comparing key to each value
    # deletes the item by pop() method
    def __delitem__(self, key):
        key_hash = self.get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True


