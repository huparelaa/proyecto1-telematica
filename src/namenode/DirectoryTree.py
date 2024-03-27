class DirectoryNode:
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.subdirectory = {}

class DirectoryTree:
    def __init__(self):
        self.root = DirectoryNode("/")

    def add_files(self, route, metadata, chunks_ubication):
        parts = route.split("/")
        file_name = parts[-1]
        actual_directory = self.root
        for part in parts[1:-1]:
            if part in actual_directory.subdirectory:
                actual_directory = actual_directory.subdirectory[part]
            else: 
                return False
        actual_directory.files[file_name] = { "route": route, "numReplicas": 1, "blockId": chunks_ubication  }

    def add_directory(self, route):
        parts = route.split("/")
        actual_directory = self.root
        for part in parts[1:-1]:
            if part in actual_directory.subdirectory:
                actual_directory = actual_directory.subdirectory[part]
                new_directory = DirectoryNode(part)
            else: 
                return False
        new_directory = DirectoryNode(parts[-1])
        actual_directory.subdirectory[parts[-1]] = new_directory
        return True

    def get_directory(self, directory_route): 
        if directory_route == "/": 
            return self.root
        parts = directory_route.split("/")
        actual_directory = self.root
        for part in parts[1:]:
            if part in actual_directory.subdirectory:
                actual_directory = actual_directory.subdirectory[part]
            else:
                print("Does not exist this directory", part)
                return None
        return actual_directory

    def ls(self, route):
        actual_directory = self.get_directory(route)
        print(list(actual_directory.files.keys()) + list(actual_directory.subdirectory.keys()))
        return list(actual_directory.files.keys()) + list(actual_directory.subdirectory.keys())

    def deleteDataNodeRegister():
        pass