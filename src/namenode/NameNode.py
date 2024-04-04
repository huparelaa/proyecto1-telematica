from DirectoryTree import DirectoryTree
from schemas.handshake import HandShakeRequest

class NameNode: 
    def __init__(self):
        self.directoryTree = DirectoryTree()
        self.blockMap = {}
        self.activesDataNodes = {}
    
    def createDataNode(self, dataNodeInfo: HandShakeRequest):
        success = False
        if dataNodeInfo.ip_address not in self.activesDataNodes:
            keyDataNode = dataNodeInfo.ip_address + ":" + dataNodeInfo.port
            self.activesDataNodes[keyDataNode] = { 
                'ip': dataNodeInfo.ip_address, 
                'port': dataNodeInfo.port, 
                'process': dataNodeInfo.process, 
                'space': dataNodeInfo.space 
            }
            print("Datanodes", self.activesDataNodes)
            print("Datanode has been created!")
            success = True
            return success 
        else:
            print("Datanode has been already created!")
            return success
    
    def handShakeBlockMap(self, ip, data):
        for block in data:
            routeName, part = block.split("-")
            if routeName not in self.blockMap:
                self.blockMap[routeName] = { 
                    part: [ip]
                }
            else: 
                if part not in self.blockMap[routeName]:
                    self.blockMap[routeName][part] = [ip]
                else: 
                    self.blockMap[routeName][part].append(ip)
            print("BlockMap", self.blockMap)

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
