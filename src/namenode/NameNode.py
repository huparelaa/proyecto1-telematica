from DirectoryTree import DirectoryTree
from schemas.handshake import HandShakeRequest
from schemas.heartbeat import HeartbeatRequest
import json
import time
import threading

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
    
    def updateBlockMap(self, ip_address, port, data):
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
                    if ip_address + ":" + port not in self.blockMap[routeName][part]:
                        self.blockMap[routeName][part].append(ip_address + ":" + port)
        print("BlockMap", json.dumps(self.blockMap, indent=4))

    def heartBeat(self, heartbeatRequest: HeartbeatRequest):
        current_time = time.time()
        keyDataNode = heartbeatRequest.ip_address + ":" + heartbeatRequest.port
        if keyDataNode in self.activesDataNodes:
            self.activesDataNodes[keyDataNode]['online'] = True
            self.activesDataNodes[keyDataNode]['available_space'] = heartbeatRequest.available_space
            self.activesDataNodes[keyDataNode]['last_heartbeat'] = current_time
            self.updateBlockMap(heartbeatRequest.ip_address, heartbeatRequest.port, heartbeatRequest.block_list)
            print("Datanodes", json.dumps(self.activesDataNodes, indent=4))
            print("Heartbeat has been received!")
            return True
        else:
            print("Heartbeat has been failed!")
            return False
    
    def check_data_node_status(self):
        if len(self.activesDataNodes) == 0:
            print("No Data Nodes available")
            return
        current_time = time.time()
        for data_node_id, data_node_info in self.activesDataNodes.items():
            if not data_node_info['online']:
                continue
            last_heartbeat = data_node_info.get('last_heartbeat', 0)
            elapsed_time = current_time - last_heartbeat
            print(f"Elapsed time for Data Node {data_node_id}: {elapsed_time}")
            if elapsed_time > 30:
                data_node_info['online'] = False
                print(f"Data Node {data_node_id} is offline")
                self.deleteDataNodeFromBlockMap(data_node_info['ip'], data_node_info['port'])
            else:
                print(f"Data Node {data_node_id} is online")

    def start_heartbeat_checker(self):
        heartbeat_check_thread = threading.Thread(target=self._hearbeat_check_loop)
        heartbeat_check_thread.daemon = True
        heartbeat_check_thread.start()

    def _hearbeat_check_loop(self):
        while True:
            self.check_data_node_status()
            time.sleep(5)

    def deleteDataNodeFromBlockMap(self, ip_address, port):
        keyDataNode = ip_address + ":" + port
        for route in self.blockMap:
            for part in self.blockMap[route]:
                if keyDataNode in self.blockMap[route][part]:
                    self.blockMap[route][part].remove(keyDataNode)

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
