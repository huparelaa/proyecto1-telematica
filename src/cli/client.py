from commands.cli_commands import ls, cd
import os

AVAILABLE_COMMANDS = ["ls", "mkdir", "cd","clear", "exit"]


def main():
    my_route = "/" # <- Don't change this line

    print("Welcome to the Hadoop File System")

    while True:
        command = input(f"{my_route}$ ")
        command = command.split(" ")
        if command[0] == "exit":
            break

        if command[0] not in AVAILABLE_COMMANDS:
            print(f"Command not found: {command[0]}")
            continue

        if command[0] == "ls":
            print("Listing files")
            ls(my_route)
        elif command[0] == "mkdir":
            print("Creating a directory")
        elif command[0] == "cd":
            if len(command) != 2:
                print("Usage: cd <directory>")
            else:
                my_route = cd(my_route, command[1])
        elif command[0] == "clear":
            os.system("clear")
        elif command[0] == "exit":
            break

if __name__ == "__main__":
    main()
