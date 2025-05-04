from io import BufferedReader
import struct

def split_into_hex_groups(data):
    return [data[i:i+4].hex().upper() for i in range(0, len(data), 4)]

def concat_hex_groups(hex_list):
    return b''.join(bytes.fromhex(hex_str) for hex_str in hex_list)

def checkByteOrder(igzFile: BufferedReader):
    igzMagicBigEndian = 0x49475A01
    igzMagicLittleEndian = 0x015A4749

    igzFile.seek(0)
    magic = igzFile.read(4)

    isIgzB = compareMagicByte(magic, igzMagicBigEndian)
    if isIgzB:
        return "big"
    else:
        return "little"

def compareMagicByte(byte, base):
    mgc = int.from_bytes(byte)
    return mgc == base

def readString(igzFile: BufferedReader):
    chars = bytearray()
    while True:
        byt = igzFile.read(1)
        if byt == b'\x00':
            ## The TSTR Fixup have duplicate 0x00 to split strings
            byt = igzFile.read(1)
            if byt == b'\x00':
                break
            else:
                igzFile.seek(igzFile.tell() - 1)
                break
        chars.extend(byt)
    return chars.decode()

def decode_raw(payload, count, big_endian):
    """Decode raw 32-bit integers"""
    if len(payload) != count * 4:
        raise ValueError("Raw data size mismatch")
    
    fmt = '>I' if big_endian else '<I'
    return [struct.unpack_from(fmt, payload, i*4)[0] 
            for i in range(count)]

def encode_delta(input_data: list):
    # Temporary buffer and state
    temp_buffer = bytearray()
    nibble_state = 0  # 0 = fresh nibble, 4 = partially filled

    # Validate sorted & delta encoding
    prev = 0
    deltas = []
    for num in input_data:
        if num < prev:
            raise ValueError("Input data not sorted")
        deltas.append(num - prev)
        prev = num

    # Bit-pack deltas
    for delta in deltas:
        current = delta
        while True:
            # Take 3 bits + continuation flag
            chunk = current & 0x07
            current >>= 3
            if current > 0:
                chunk |= 0x08  # Set continuation flag

            # Pack into nibbles
            if nibble_state == 0:
                temp_buffer.append(chunk << 4)
                nibble_state = 4
            else:
                temp_buffer[-1] |= chunk
                nibble_state = 0

            if current == 0:
                break

    # Align to 4 bytes
    while len(temp_buffer) % 4 != 0:
        temp_buffer.append(0)

def decode_delta(payload, count, big_endian):
    """Decode delta-encoded data"""
    current = 0
    result = []
    bit_buffer = 0
    bits_stored = 0
    byte_idx = 0
    nibble_idx = 0

    while len(result) < count:
        if byte_idx >= len(payload):
            break

        # Get next nibble (4 bits)
        byte = payload[byte_idx]
        nibble = (byte >> (4 * (1 - nibble_idx))) & 0x0F
        nibble_idx = (nibble_idx + 1) % 2
        if nibble_idx == 0:
            byte_idx += 1

        # Process nibble
        continuation = (nibble & 0x08) != 0
        value = nibble & 0x07
        
        # Add to bit buffer
        bit_buffer |= value << bits_stored
        bits_stored += 3
        
        if not continuation:
            # Finalize delta
            delta = bit_buffer
            bit_buffer = 0
            bits_stored = 0
            
            # Apply delta
            current += delta
            result.append(current)
    
    # Handle remaining bits
    if bits_stored > 0:
        delta = bit_buffer
        current += delta
        result.append(current)

    # Validate count
    if len(result) != count:
        raise ValueError("Delta decoding count mismatch")

    return result