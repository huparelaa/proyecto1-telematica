from filetransfer.servicer import grpcServer
from services.auth import login

def main():
    #print(login()) <- wait for the login function to be implemented on NameNode
    grpcServer()


if __name__ == "__main__":
    main()
