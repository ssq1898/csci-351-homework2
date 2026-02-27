# Helper functions for creating ICMP packets and calculating checksums for both my_ping and my_traceroute.

import struct
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
