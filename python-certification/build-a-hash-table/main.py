class HashTable:
    def __init__(self):
        self.collection = {}
    
    def hash(self, key):
        total = 0
        for char in key:
            total += ord(char)
        return total
    
    def add(self, key, value):
        hashed_key = self.hash(key)
        
        if hashed_key not in self.collection:
            self.collection[hashed_key] = {}
        
        self.collection[hashed_key][key] = value
    
    def remove(self, key):
        hashed_key = self.hash(key)
        
        if hashed_key in self.collection:
            if key in self.collection[hashed_key]:
                del self.collection[hashed_key][key]
                
                # If the nested dictionary becomes empty, remove it
                if not self.collection[hashed_key]:
                    del self.collection[hashed_key]
    
    def lookup(self, key):
        hashed_key = self.hash(key)
        
        if hashed_key in self.collection:
            if key in self.collection[hashed_key]:
                return self.collection[hashed_key][key]
        
        return None


# Test the implementation
if __name__ == "__main__":
    # Create a hash table instance
    ht = HashTable()
    
    # Test hash method
    print(f"Hash of 'golf': {ht.hash('golf')}") 
    
    # Test add method
    ht.add('golf', 'sport')
    print(f"Collection after adding 'golf': {ht.collection}")
    
    # Test collision handling
    ht.add('rose', 'flower')
    ht.add('dear', 'friend')
    ht.add('read', 'book')
    print(f"Collection after multiple adds: {ht.collection}")
    
    # Test lookup method
    print(f"Lookup 'golf': {ht.lookup('golf')}")  
    print(f"Lookup 'nonexistent': {ht.lookup('nonexistent')}")  
    
    # Test collision where different keys produce same hash
    ht.add('fcc', 'coding')
    ht.add('cfc', 'chemical')
    print(f"Collection with colliding keys: {ht.collection}")
    
    # Test remove method
    ht.remove('golf')
    print(f"Collection after removing 'golf': {ht.collection}")
    
    # Test removing a key that doesn't exist (should not raise error)
    ht.remove('nonexistent')
    print(f"Collection after removing nonexistent key: {ht.collection}")
    
    # Add multiple keys that hash to the same value
    test_ht = HashTable()
    test_ht.add('rose', 'flower')
    print(f"Single entry: {test_ht.collection}")
    
    test_ht.add('fcc', 'coding')
    test_ht.add('cfc', 'chemical')
    print(f"Collision example: {test_ht.collection}")
