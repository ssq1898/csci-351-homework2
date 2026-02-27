import socket
import struct
import time
import select
import argparse

from helpers import create_packet


def ping(dest, count, interval, size, timeout):
    """
    Send ICMP echo requests to the specified destination and print the results.

    @param dest: The destination host to ping
    @param count: Number of packets to send
    @param interval: Time interval between packets in seconds
    @param size: Size of the ICMP payload in bytes
    @param timeout: Timeout for each packet in seconds
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    dest_ip = socket.gethostbyname(dest)
    print(f"\nPinging {dest} [{dest_ip}] with {size} bytes of data:")

    current = 1
    initial_time = time.time()

    while count is None or current <= count:
        send_time = time.time()
        packet = create_packet(current, size)
        sock.sendto(packet, (dest_ip, 0))

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0] == []:
                print("Request timed out.\n")
                return

            if timeout is not None and (time.time() - initial_time) >= timeout:
                print(f"Ping session timed out after {timeout} seconds.\n")
                return

            recv_time = time.time()
            recv_packet, _ = sock.recvfrom(1024)
            icmp_header = recv_packet[20:28]
            type, _, _, _, recv_seq = struct.unpack("bbHHh", icmp_header)

            if type == 0 and recv_seq == current:
                rtt = (recv_time - send_time) * 1000
                print(f"Reply from {dest_ip}: bytes={len(recv_packet)} time={rtt:.0f} ms TTL={recv_packet[8]}")
                break

        time.sleep(interval)

        current += 1

    print("")


if __name__ == "__main__":
    """
    Command-line interface for the ping utility. Parses arguments and calls the ping function.
    """
    parser = argparse.ArgumentParser(prog="my_ping")
    parser.add_argument("destination", help="destination host")
    parser.add_argument("-c", type=int, help="packet count")
    parser.add_argument("-i", type=float, default=1, help="interval seconds")
    parser.add_argument("-s", type=int, default=56, help="packet size")
    parser.add_argument("-t", type=int, help="timeout seconds")

    args = parser.parse_args()
    ping(args.destination, args.c, args.i, args.s, args.t)
