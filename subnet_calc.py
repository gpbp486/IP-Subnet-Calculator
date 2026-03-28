

#a.c.d/x where x is # of bits in subnet
#example; 200.23.16.0/23
#a = format(a, '08b')

def calculate_subnet(addr, cidr, print_=False):

    #changing ip string to binary octect
    integers = [int(part) for part in addr.split('.')]
    for num in integers:
        num = format(int(num), '08b')
        
    
    if print_:
        print(f"IP addr: {addr}\n")


    #calculating subnet mask
    cidr_cal = pow(2, (32 - int(cidr)))
    
    if print_:
        print("Calculating CIDR...")
        print(f"32 - {int(cidr)} = {32-int(cidr)}")
        print(f"2^{32-int(cidr)} = {cidr_cal}")
    
    #checking if there is an overflow
    cidr_num = cidr_cal
    cidr_diff = 0
    if cidr_cal>255:
        cidr_diff = cidr_cal-255
        cidr_num = cidr_num - cidr_diff
        
    if print_:
        print(f"{cidr_cal} host addresses in subnet")


    #creating subnet mask
    mask = (0xffffffff >> (32 - int(cidr))) << (32 - int(cidr))
    subnet_Mask = [
    (mask >> 24) & 255,
    (mask >> 16) & 255,
    (mask >> 8) & 255,
    mask & 255]

    if print_:
        subnet_address = ".".join(format(o, '08b') for o in subnet_Mask)
        print(f"Subnet Mask Octet: {subnet_address}")

    #calculating network address
    if print_:
        print("\nCalculating Network Addr...")
        ip_addr = ".".join([format(o, '08b') for o in integers])
        print(f"IP addr (octet): {ip_addr}")
        print("\t\t--Bitwise AND--")
        print(f"Subnet Mask (octet): {subnet_address}")
        print("------------------------------------------------------")

    # ip AND subnet mask to get network address
    network_octets = []
    for i in range(4):
        result = integers[i] & subnet_Mask[i]
        network_octets.append(result)
    

    network_addr_octet = ".".join(format(o, '08b') for o in network_octets)
    network_addr = ".".join(str(o) for o in network_octets)
    
    if print_:
        print(f"Network addr (octet): {network_addr_octet}")
        print(f"Network addr: {network_addr}")

        print("\nCalculating Broadcast Address...")


    host_bits = 32 - int(cidr)
    
    if print_:
        print(f"Number of host bits 32 - CIDR = {host_bits}")

    host_mask = (1 << host_bits) - 1 # sets n bits to 1
    
    #turn network addr into a big 32 bit num
    network_int = (
        (network_octets[0] << 24) |
        (network_octets[1] << 16) |
        (network_octets[2] << 8) |
        network_octets[3]
    ) 
    # OR network int and our host_mask to get Broadcase 32 bit in
    broadcast_int = network_int | host_mask

    #turn back into octets
    broadcast_octets = [
        (broadcast_int >> 24) & 255,
        (broadcast_int >> 16) & 255,
        (broadcast_int >> 8) & 255,
        broadcast_int & 255
    ]


    broadcast_addr = ".".join([str(o) for o in broadcast_octets])
    if print_:
        print("Calculated by taking network address and replace all host bits with 1s")
        print(f"Broadcast addr: {broadcast_addr}")

        
    if int(cidr)!=32:
        if int(cidr)!=31:
            first_usable = network_octets[0:3]
            first_usable.append(network_octets[3]+1)
            first_usable_addr = ".".join(str(o) for o in first_usable)

            #calc last usable
            last_usable = broadcast_octets[0:3]
            last_usable.append(broadcast_octets[3]-1)
            last_usable_addr = ".".join(str(o) for o in last_usable)

        else:
            #cidr=31 so we just use network and broadcast
            first_usable = network_octets
            first_usable_addr = ".".join(str(o) for o in first_usable)
            last_usable = broadcast_octets
            last_usable_addr = ".".join(str(o) for o in last_usable)
       
        if print_:
            print("\nCalculating Range of Host Addresses...")
            print("Calculate the First Usable Address: This is typically the network address plus one")
    
            print(f"First Usable addr: {first_usable_addr}")

            print("Calculate the Last Usable Address: This is typically the broadcast address minus one")
            print(f"Last Usable addr: {last_usable_addr}")


    print("\nSummary:")
    print(f"Network addr: {network_addr}")
    print(f"Broadcast addr: {broadcast_addr}")
    if int(cidr)!=32:
        print(f"First Usable addr: {first_usable_addr}")
        print(f"Last Usable addr: {last_usable_addr}")
    else:
        print("CIDR = 32, SINGLE HOST, First/Last N/A")




if __name__ == "__main__":
    #calculate_subnet('192.168.1.0', '24')
    q = True
    print("Do you want to print calulation specifications?")
    p = input("Y/N: ").strip()
    print_ = True if p.lower() == 'y' else False
    while q:
        print("\n\nEnter 'q' at anytime to QUIT.")
        ip = input("Enter IP Address: ")
        if ip=='q':
            q = False
            break
        cidr = input("Enter CIDR: ")
        if cidr=='q':
            q = False
            break
        calculate_subnet(ip, cidr, print_=print_)



