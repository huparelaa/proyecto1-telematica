from DirectoryTree import DirectoryTree
from schemas.handshake import HandShakeRequest
import json

class NameNode: 
    def __init__(self):
        self.directoryTree = DirectoryTree()
        self.blockMap = {}
        self.activesDataNodes = {}
    
    def createDataNode(self, dataNodeInfo: HandShakeRequest):
        if dataNodeInfo.ip_address not in self.activesDataNodes:
            keyDataNode = dataNodeInfo.ip_address + ":" + dataNodeInfo.port
            self.activesDataNodes[keyDataNode] = { 
                'ip': dataNodeInfo.ip_address, 
                'port': dataNodeInfo.port, 
                'available_space': dataNodeInfo.available_space, 
                'online': True
            }
            print("Datanodes", json.dumps(self.activesDataNodes, indent=4))
            print("Datanode has been created!")
            return True
        else:
            print("Datanode has been already created!")
            return False
    
    def handShakeBlockMap(self, ip_address, port, data):
        for block in data:
            routeName, part = block.split("-_-")
            if routeName not in self.blockMap:
                self.blockMap[routeName] = { 
                    part: [ip_address + ":" + port]
                }
            else: 
                if part not in self.blockMap[routeName]:
                    self.blockMap[routeName][part] = [ip_address + ":" + port]
                else: 
                    self.blockMap[routeName][part].append(ip_address + ":" + port)
        print("BlockMap", json.dumps(self.blockMap, indent=4))

    def getReadDataNodes(self, route):
        return self.blockMap[route]

    def getWriteDataNodes(self, file_name, block_size, block_num, num_replicas): 
        dataNodesToWrite = []
        dataNodesAvailable = list(self.activesDataNodes.keys())
        for i in range(0, block_num):
            dataNodesToWrite.append(dataNodesAvailable[i])
        return dataNodesToWrite
    

    
    def searchFileInBlockMap(self, filename):
        pass
