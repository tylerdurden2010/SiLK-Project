import math
import struct,socket

def read_in_chunks(file_object, chunk_size=1055):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def readfile(filepath, delim):
    with open(filepath, 'r') as f:
        for line in f:
            yield tuple(line.split(delim))

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def splitBar(strContent):

    tempList = strContent.split('|')
    for index,content in enumerate(tempList):
        tempList[index] = str(content.strip())
    return tempList

def formatLine(strContent):
    result = ""
    tempList = strContent.split('|')

    result = str(tempList[0].strip()) + ":" + str(tempList[2].strip()) + "|" + str(tempList[1].strip()) + ":" + \
             str(tempList[3].strip()) + '\n'

    return result
def cos_dist(a, b):
    if len(a) != len(b):
        return None
    part_up = 0.0
    a_sq = 0.0
    b_sq = 0.0
    for a1, b1 in zip(a, b):
        part_up += a1 * b1
        a_sq += a1 ** 2
        b_sq += b1 ** 2
    part_down = math.sqrt(a_sq * b_sq)
    if part_down == 0.0:
        return None
    else:
        return part_up / part_down
#todo
def diffAB(a,b):
    aSerial = list()
    bSerial = list()
    for i in range(len(a)):
        if a[i] == b[i]:
            aSerial.append(1)
            bSerial.append(1)
        else:
            #The order is fucking important
            aSerial.append(1)
            aSerial.append(0)
            bSerial.append(0)
            bSerial.append(1)

    return cos_dist(aSerial,bSerial)


resultfile = open("./resultTest.txt",'a')
filehandle = open("./gen.txt")

line = filehandle.readline()
anoline = filehandle.readline()


while (anoline):
    anoLineList = splitBar(anoline)
    lineList = splitBar(line)

#    if (diffAB(anoLineList,lineList) <= 0.5 ):
    if (diffAB(anoLineList,lineList) < 0.75 ):

        resultfile.write( formatLine(line))

        line = anoline
        anoline = filehandle.readline()
    else:

        line = anoline
        anoline = filehandle.readline()

resultfile.write( formatLine(line))
