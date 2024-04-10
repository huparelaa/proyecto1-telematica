from DirectoryTree import DirectoryTree
# from schemas.handshake import HandShakeRequest
# from schemas.heartbeat import HeartbeatRequest
from schemas import *
import json
import time
import threading

class NameNode: 
    def __init__(self):
        self.directoryTree = DirectoryTree()
        self.blockMap = {}
        self.activesDataNodes = {}

        self.replayEditLog()
    
    def replayEditLog(self):
        with open("editlog.txt", "r") as file:
            for line in file:
                action, route = line.strip().split(":")
                if action == "write":
                    self.directoryTree.add_files(RouteRequest(route=route))
                elif action == "mkdir":
                    self.directoryTree.add_directory(route)

    def createDataNode(self, dataNodeInfo: HandShakeRequest):
        if dataNodeInfo.ip_address not in self.activesDataNodes:
            keyDataNode = dataNodeInfo.ip_address + ":" + dataNodeInfo.port
            self.activesDataNodes[keyDataNode] = { 
                'ip': dataNodeInfo.ip_address, 
                'port': dataNodeInfo.port, 
                'online': True,
                'last_heartbeat': 0
            }
            print("Datanodes", json.dumps(self.activesDataNodes, indent=4))
            return True
        else:
            print("Datanode has been already created!")
            return False
    
    def updateBlockMap(self, ip_address, port, data):
        keyDataNode = ip_address + ":" + port
        all_blocks = set()

        # Primero, actualizar el blockMap con los bloques actuales.
        for block in data:
            routeName, part = block.split("-_-")
            if routeName not in self.blockMap:
                self.blockMap[routeName] = { part: [keyDataNode] }
            else:
                if part not in self.blockMap[routeName]:
                    self.blockMap[routeName][part] = [keyDataNode]
                else:
                    if keyDataNode not in self.blockMap[routeName][part]:
                        self.blockMap[routeName][part].append(keyDataNode)

            all_blocks.add((routeName, part))

        # Ahora, revisar y eliminar cualquier bloque obsoleto para este DataNode.
        for routeName in list(self.blockMap.keys()):
            for part in list(self.blockMap[routeName].keys()):
                if (routeName, part) not in all_blocks and keyDataNode in self.blockMap[routeName][part]:
                    self.blockMap[routeName][part].remove(keyDataNode)
                    if not self.blockMap[routeName][part]:  # Si no hay más DataNodes para este bloque, eliminar la entrada.
                        del self.blockMap[routeName][part]

                if not self.blockMap[routeName]:  # Si no hay más partes para esta ruta, eliminar la entrada.
                    del self.blockMap[routeName]

        print("BlockMap actualizado:", json.dumps(self.blockMap, indent=4))

    def analyzeBlockMap(self, keyDataNode):
        command = ""
        blocks_to_replicate = []
        for route in self.blockMap:
            for part in self.blockMap[route]:
                if len(self.blockMap[route][part]) < 3:
                    command = "replicate"
                    data = {
                        "data_node_address": self.chooseDataNodeToReplicate(route, part, keyDataNode),
                        "file_path": route + "-_-" + part,
                    }
                    blocks_to_replicate.append(data)
        return command, blocks_to_replicate

    def chooseDataNodeToReplicate(self, route, part, keyDataNode):
        data_nodes = self.blockMap[route][part]
        for data_node in self.activesDataNodes:
            print(data_node)
            if data_node not in data_nodes and data_node != keyDataNode:
                return data_node
        return None

    def heartBeat(self, heartbeatRequest: HeartbeatRequest):
        current_time = time.time()
        command = ""
        block_to_replicate = []
        keyDataNode = heartbeatRequest.ip_address + ":" + heartbeatRequest.port
        if keyDataNode in self.activesDataNodes:
            self.activesDataNodes[keyDataNode]['online'] = True
            self.activesDataNodes[keyDataNode]['last_heartbeat'] = current_time
            self.updateBlockMap(heartbeatRequest.ip_address, heartbeatRequest.port, heartbeatRequest.block_list)
            if heartbeatRequest.status != "busy":
                command, block_to_replicate = self.analyzeBlockMap(keyDataNode)
            return True, command, block_to_replicate
        return False, "", []
    
    def check_data_node_status(self):
        if len(self.activesDataNodes) == 0:
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


    def getAvailableDataNodes(self):
        availableDataNodes = []
        for dataNode in self.activesDataNodes:
            if self.activesDataNodes[dataNode]['online']:
                availableDataNodes.append(dataNode)
        return availableDataNodes

    def getWriteDataNodes(self, request: FileWriteRequest): 
        #Falta comprobar que el archivo no exista en el sistema
        # Comprabar con el path 
        availableDataNodes = self.getAvailableDataNodes()
        block_assignment = {}
        num_data_nodes = len(availableDataNodes)
        if num_data_nodes == 0:
            return block_assignment
        for i in range(request.block_num):
            block_id = f"{request.file_name}-_-part{i+1:04d}"
            data_nodes_assigned = []
            data_node_index = (i) % num_data_nodes
            data_node = availableDataNodes[data_node_index]
            if data_node not in data_nodes_assigned:
                data_nodes_assigned.append(data_node)
            block_assignment[block_id] = data_nodes_assigned
        return block_assignment