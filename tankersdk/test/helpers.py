def corrupt_buffer(buffer):
    """ Make sure one part of the buffer gets changed """
    array = bytearray(buffer)
    array[0] = (array[0] + 1) % 255
    return bytes(array)
