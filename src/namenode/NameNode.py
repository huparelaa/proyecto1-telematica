from DirectoryTree import DirectoryTree

class NameNode: 
    def __init__(self):
        self.directoryTree = DirectoryTree()
        self.activesDataNodes = { 
            "127.0.0.1": { 
                "ip": "127.0.0.1",
                "port": "8080",
                "state": "active"
            },
            "127.0.0.2": { 
                "ip": "127.0.0.2",
                "port": "8080",
                "state": "active"
            },
            "127.0.0.3": { 
                "ip": "127.0.0.3",
                "port": "8080",
                "state": "active"
            },
            "127.0.0.4": { 
                "ip": "127.0.0.4",
                "port": "8080",
                "state": "active"
            },
            "127.0.0.5": { 
                "ip": "127.0.0.5",
                "port": "8080",
                "state": "active"
            },
        }
    
    def createDataNode(self, ip, port, state):
        success = False
        if ip not in self.activesDataNodes:
            self.activesDataNodes[ip] = { 'ip': ip, 'port': port, 'state': state }
            print("Datanode has been created!")
            success = True
            return success 
        else:
            print("Datanode has been already created!")
            return success
    
    def getWriteDataNodes(self, file_name, block_size, block_num, num_replicas): 
        dataNodesToWrite = []
        dataNodesAvailable = list(self.activesDataNodes.keys())
        for i in range(0, block_num):
            dataNodesToWrite.append(dataNodesAvailable[i])
        return dataNodesToWrite
    
    def getReadDataNodes(self, file_name):
        pass