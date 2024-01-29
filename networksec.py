# import socket
# import nmap
# from prettytable import PrettyTable
# import pandas as pd

# target = input("Enter the target IP address: ")
# ports = list(map(int, input("Enter the range of ports (comma-separated): ").split(',')))


# def scan_port(target, port):
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(1)
#         sock.connect((target, port))
#         return True
#     except:
#         return False

# def identify_service(target, port):
#     scanner = nmap.PortScanner()
#     results = scanner.scan(target, arguments='-sV -p '+str(port))
#     service = results['scan'][target]['tcp'][port]['name']
#     return service

# # Create a table
# table = PrettyTable(["Port", "Status", "Service"])

# for port in ports:
#     result = scan_port(target, port)
#     if result:
#         service = identify_service(target, port)
#         table.add_row([port, "Open", service])
#     else:
#         table.add_row([port, "Closed", "N/A"])

# # Print the table
# print(table)

# # Save the table to a text file
# with open('output.txt', 'w') as f:
#     f.write(str(table))


import socket

def scan_ports(target, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports

def main():
    target_host = input("Enter target host/IP: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    open_ports = scan_ports(target_host, start_port, end_port)

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(port)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
