import os
from dotenv import load_dotenv

load_dotenv()
token = "-_-part"
def split_file(file_path):
    block_size = int(os.getenv("BLOCK_SIZE"))
    base_file_name = os.path.splitext(os.path.basename(file_path))[0] + os.path.splitext(os.path.basename(file_path))[1]
    destination_directory = "splits/uploads"
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    block_num = 1
    with open(file_path, 'rb') as file:
        block = file.read(block_size)
        while block:
            block_file_name = f"{destination_directory}/{base_file_name}{token}{block_num:04d}"
            with open(block_file_name, 'wb') as block_file:
                block_file.write(block)
            block_num += 1
            block = file.read(block_size)

def join_files(file_name):
    destination_directory = "../downloads"
    partitions_directory = "splits/downloads"
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    if not os.path.exists(partitions_directory):
        print("No partitions to join")
        return
    if check_partition_exists(file_name) == False:
        print("File not found")
        return

    delete_splits("downloads")

    partitions = sorted(os.listdir(partitions_directory))
    with open(f"{destination_directory}/{file_name}", 'wb') as file:
        for partition in partitions:
            partition_path = os.path.join(partitions_directory, partition)
            with open(partition_path, 'rb') as partition_file:
                file.write(partition_file.read())
    
def delete_splits(folder_type):
    if folder_type == "uploads":
        destination_directory = "splits/uploads"
    elif folder_type == "downloads":
        destination_directory = "splits/downloads"
    else:
        print("Invalid folder type")
        return
    if os.path.exists(destination_directory):
        for file in os.listdir(destination_directory):
            file_path = os.path.join(destination_directory, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        os.rmdir(destination_directory)
    else:
        print("No splits to delete")

def check_partition_exists(file_name):
    partitions_directory = "splits/downloads"
    if not os.path.exists(partitions_directory):
        return False
    partitions = sorted(os.listdir(partitions_directory))
    # Partition name format: <file_name>-_-part<block_num>
    for partition in partitions:
        if partition.split("-_-")[0] == file_name:
            return True
    return False

