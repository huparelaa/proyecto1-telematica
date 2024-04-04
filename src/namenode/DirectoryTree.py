import json

class FileNode:
    def __init__(self, name, route, numReplicas):
        self.name = name
        self.route = route
        self.numReplicas = numReplicas
        self.blockId = []
        
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
        actual_directory.files[file_name] = { "route": route, "numReplicas": 1, "block_list": []  }

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
        if actual_directory is None:
            return None
        print(list(actual_directory.files.keys()) + list(actual_directory.subdirectory.keys()))
        return list(actual_directory.files.keys()) + list(actual_directory.subdirectory.keys())
    
    def to_json(self, filename):
        data = self._serialize_node(self.root)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def _serialize_node(node):
        serialized = {
            "name": node.name,
            "files": node.files,
            "subdirectory": {}
        }
        for name, subdirectory_node in node.subdirectory.items():
            serialized["subdirectory"][name] = DirectoryTree._serialize_node(subdirectory_node)
        return serialized

    @staticmethod
    def from_json(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        tree = DirectoryTree()
        tree.root = DirectoryTree._deserialize_node(data)
        return tree

    @staticmethod
    def _deserialize_node(data):
        node = DirectoryNode(data["name"])
        node.files = data["files"]
        for name, subdirectory_data in data["subdirectory"].items():
            node.subdirectory[name] = DirectoryTree._deserialize_node(subdirectory_data)
        return node

if __name__ == "__main__":
    tree = DirectoryTree()
    print("Adding files")
    tree.add_files("/txt/hola/cl.mp3", "", "")
    tree.add_directory("/txt1")
    tree.add_directory("/txt2")
    tree.add_directory("/txt1/lucia")
    tree.add_files("/txt1/lucia/la.mp3", "", "")
    tree.add_directory("/txt2/hola")
    tree.add_directory("/txt2/hola2")
    tree.ls("/")
    print("Writing files")
    tree.to_json("directory_tree.json")
    print("Reading files")
    tree2 = DirectoryTree.from_json("directory_tree.json")
    tree2.ls("/")
    tree.ls("/txt")
    tree2.ls("/txt1")
    tree2.ls("/txt2/hola")