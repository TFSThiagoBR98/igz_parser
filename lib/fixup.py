from io import BufferedReader
from typing import Literal

from lib.chunks import ChunkInfo
from lib.fixups.base import FixUp
from lib.fixups.exid import EXID, processFixUpEXID
from lib.fixups.exnm import EXNM, processFixUpEXNM
from lib.fixups.mtsz import MTSZ, processFixUpMTSZ
from lib.fixups.onam import ONAM, processFixUpONAM
from lib.fixups.rhnd import RHND, processFixUpRHND
from lib.fixups.rnex import RNEX, processFixUpRNEX
from lib.fixups.rofs import ROFS, processFixUpROFS
from lib.fixups.root import ROOT, processFixUpROOT
from lib.fixups.rpid import RPID, processFixUpRPID
from lib.fixups.rstt import RSTT, processFixUpRSTT
from lib.fixups.rvtb import RVTB, processFixUpRVTB
from lib.fixups.tdep import TDEP, processFixUpTDEP
from lib.fixups.tmet import TMET, processFixUpTMET
from lib.fixups.tstr import TSTR, processFixUpTSTR

def processFixUp(igzFile: BufferedReader, chunk: ChunkInfo, byteorder: Literal["little", "big"] = "big"):
    currentPos: int = 0
    fixups = {}
    tstr: TSTR
    while currentPos < chunk.size:
        igzFile.seek(chunk.offset + currentPos)
        
        offset = igzFile.tell()
        magicNumber = igzFile.read(4).decode('utf-8')
        count = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        lenght = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        startOfData = int.from_bytes(igzFile.read(4), byteorder=byteorder)

        print(f"Fixup {magicNumber}: O: {offset}, C: {count}, L: {lenght}, P: {startOfData}")

        if magicNumber == "TDEP":
            igzFile.seek(offset + startOfData)
            dependencies = processFixUpTDEP(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = TDEP(magicNumber, offset, count, lenght, startOfData, dependencies)
            pass
        elif magicNumber == "TSTR":
            igzFile.seek(offset + startOfData)
            strings = processFixUpTSTR(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            tstr = TSTR(magicNumber, offset, count, lenght, startOfData, strings)
            fixups[magicNumber] = tstr
            pass
        elif magicNumber == "TMET":
            igzFile.seek(offset + startOfData)
            strings = processFixUpTMET(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = TMET(magicNumber, offset, count, lenght, startOfData, strings)
            pass
        elif magicNumber == "MTSZ":
            igzFile.seek(offset + startOfData)
            ints = processFixUpMTSZ(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = MTSZ(magicNumber, offset, count, lenght, startOfData, ints)
            pass
        elif magicNumber == "EXNM":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpEXNM(igzFile, count, tstr.strings, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = EXNM(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "EXID":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpEXID(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = EXID(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "RVTB":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpRVTB(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = RVTB(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "ROFS":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpROFS(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = ROFS(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "RSTT":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpRSTT(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = RSTT(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "RPID":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpRPID(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = RPID(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "RHND":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpRHND(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = RHND(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "RNEX":
            igzFile.seek(offset + startOfData)
            mapper = processFixUpRNEX(igzFile, count, lenght - 16, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = RNEX(magicNumber, offset, count, lenght, startOfData, mapper)
            pass
        elif magicNumber == "ONAM":
            igzFile.seek(offset + startOfData)
            offsetOnam = processFixUpONAM(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = ONAM(magicNumber, offset, count, lenght, startOfData, offsetOnam)
            pass
        elif magicNumber == "ROOT":
            igzFile.seek(offset + startOfData)
            values = processFixUpROOT(igzFile, count, byteorder)
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = ROOT(magicNumber, offset, count, lenght, startOfData, values)
            pass
        else:
            igzFile.seek(offset + startOfData)
            data = igzFile.read(lenght - startOfData).hex()
            igzFile.seek(offset + startOfData)
            fixups[magicNumber] = FixUp(magicNumber, offset, count, lenght, startOfData, data)

        currentPos += lenght
    return fixups
