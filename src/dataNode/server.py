from filetransfer.servicer import grpcServer
from services.auth import login

def main():
    grpcServer()

if __name__ == "__main__":
    main()
