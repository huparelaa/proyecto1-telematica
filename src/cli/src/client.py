from commands.cli_commands import ls, cd, mkdir, write, read
import os

AVAILABLE_COMMANDS = ["ls", "mkdir", "cd","clear", "exit", "help", "write", "read"]

def main():
    os.system("clear")
    username = login()
    my_route = f"/{username}/"
    print("Welcome to the Hajoop File System")
    print("Type 'help' to see the available commands")
    while True:
        command = input(f"\033[92m{my_route}$ \033[0m")
        command = command.split(" ")
        #remove empty strings
        command = list(filter(lambda x: x != "", command))
        if command[0] == "exit":
            break

        if command[0] not in AVAILABLE_COMMANDS:
            print(f"Command not found: {command[0]}")
            continue

        if command[0] == "ls":
            ls(my_route)
        elif command[0] == "mkdir":
            if len(command) != 2:
                print("Usage: mkdir <directory>")
            else:
                mkdir(my_route, command[1])
        elif command[0] == "cd":
            if len(command) != 2:
                print("Usage: cd <directory>")
            else:
                try:
                    my_route = cd(my_route, command[1], username)
                except Exception as e:
                    print("No such file or directory")
        elif command[0] == "clear":
            os.system("clear")
        elif command[0] == "exit":
            break
        elif command[0] == "help":
            print("Available commands:")
            for command in AVAILABLE_COMMANDS:
                print(f"\t{command}")
        elif command[0] == "write":
            if len(command) != 2:
                print("Usage: write <file_name>")
            else:
                write(my_route, command[1])
        elif command[0] == "read":
            if len(command) != 2:
                print("Usage: read <file_name>")
            else:
                read(my_route, command[1])
        else:
            print(f"Command not found {command[0]}")

def login():
    username = input("Username: ")
    try:
        cd("/", username, username)
    except Exception as e:
        mkdir("/", username)
        cd("/", username, username)

    return username

if __name__ == "__main__":
    main()
    