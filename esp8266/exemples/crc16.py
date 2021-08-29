
def calculate_crc(b, l):
    crc = 0xFFFF
    crcH = 0
    crcL = 0

    for i in range(0,l,1):
        crc ^= b[i]
        for j in range(8,0,-1):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    #bytes are wrong way round so doing a swap here..
    crcH = (crc & 0x00FF) << 8
    crcL = (crc & 0xFF00) >> 8
    crcH |= crcL
    crc = crcH
    return crc

#End
