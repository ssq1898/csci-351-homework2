import socket
import struct
import time
import select
import argparse
import os

def create_packet(seq, size):
    """
    Create an ICMP echo request packet with the given sequence number.

    @param seq: Sequence number for the ICMP packet
    @param size: Size of the ICMP payload in bytes
    @return: The complete ICMP packet ready to be sent
    """
    header = struct.pack("bbHHh", 8, 0, 0, os.getpid() & 0xFFFF, seq)
    data = bytes(size)
    checksum = calculate_checksum(header + data)
    header = struct.pack("bbHHh", 8, 0, checksum, os.getpid() & 0xFFFF, seq)
    return header + data


def calculate_checksum(source_string):
    """
    Calculate the checksum of the given source string.

    @param source_string: The string to calculate the checksum for
    @return: The checksum value
    """
    checksum = 0
    count_to = (len(source_string) // 2) * 2

    for count in range(0, count_to, 2):
        this_val = source_string[count + 1] * 256 + source_string[count]
        checksum += this_val
        checksum &= 0xFFFFFFFF

    if count_to < len(source_string):
        checksum += source_string[len(source_string) - 1]
        checksum &= 0xFFFFFFFF

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)
    return ~checksum & 0xFFFF


def traceroute(dest, numeric, queries, summary):
    """
    Perform a traceroute to the specified destination.

    @param dest: The destination host to trace
    @param numeric: If True, display numeric IP addresses instead of hostnames
    @param queries: Number of queries to send per hop
    @param summary: If True, display a summary of the traceroute results
    """
    print(f"\nTracing route to {dest} [{socket.gethostbyname(dest)}] with {queries} queries per hop:")

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    dest_ip = socket.gethostbyname(dest)

    for ttl_value in range(1, 30):
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_value)

        unanswered = 0
        reached_destination = False

        print(f"{ttl_value} ", end="")

        for probe in range(queries):
            packet = create_packet(probe, 56)
            sock.sendto(packet, (dest_ip, 0))

            ready = select.select([sock], [], [], 1)

            if ready[0] == []:
                print("* ", end="")
                unanswered += 1
                continue

            recv_packet, _ = sock.recvfrom(1024)

            ip_header = struct.unpack("!BBHHHBBH4s4s", recv_packet[:20])
            recv_ip = socket.inet_ntoa(ip_header[8])

            if numeric:
                display = recv_ip
            else:
                try:
                    display = socket.gethostbyaddr(recv_ip)[0] + f" [{recv_ip}]"
                except socket.herror:
                    display = recv_ip

            print(f"{display} ", end="")

            if recv_ip == dest_ip:
                reached_destination = True

        print()

        if summary and unanswered > 0:
            print(f"  {unanswered}/{queries} probes unanswered")

        if reached_destination:
            print("Destination reached.\n")
            break


if __name__ == "__main__":
    """
    Command-line interface for the traceroute utility. Parses arguments and calls the traceroute function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("-n", action="store_true", help="numeric output only")
    parser.add_argument("-q", type=int, default=3, help="queries per hop")
    parser.add_argument("-S", action="store_true", help="summary")

    args = parser.parse_args()
    traceroute(args.destination, args.n, args.q, args.S)
