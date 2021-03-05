PACKET_SIZE_HEADER_LENGTH: int = 4


def pack_size(data: bytes) -> bytes:
    return len(data).to_bytes(PACKET_SIZE_HEADER_LENGTH,
                              byteorder='big')


def unpack_size(header: bytes) -> int:
    if len(header) == PACKET_SIZE_HEADER_LENGTH:
        return int.from_bytes(header,
                              byteorder="big")
    else:
        raise Exception(
            f"Invalid header size: {len(header)}, \
                expected {PACKET_SIZE_HEADER_LENGTH}")
