import amiibo
import os
import sys

with open(os.path.join(os.path.abspath("."), "key_retail.bin"), "rb") as fp_j:
    key = amiibo.AmiiboMasterKey.from_combined_bin(fp_j.read())

def open_bin(bin_location):
    """
    Opens a bin and makes it 540 bytes if it wasn't

    :param str bin_location: file location of bin you want to open
    :return: opened bin
    """
    bin_fp = open(bin_location, 'rb')

    bin_dump = bytes()
    for line in bin_fp:
        bin_dump += line
    bin_fp.close()

    if len(bin_dump) == 540:
        with open(bin_location, 'rb') as fp:
            dump = amiibo.AmiiboDump(key, fp.read())
            return dump
    # if bin isn't 540 bytes, set it to that
    elif 532 <= len(bin_dump) <= 572:
        while len(bin_dump) < 540:
            bin_dump += b'\x00'
        if len(bin_dump) > 540:
            bin_dump = bin_dump[:-(len(bin_dump) - 540)]
        b = open(bin_location, 'wb')
        b.write(bin_dump)
        b.close()

        with open(bin_location, 'rb') as fp:
            dump = amiibo.AmiiboDump(key, fp.read())
            return dump

def main(path):
    dump = open_bin(path)

    dump.unlock()

    mii = dump.data[0xA0:0x100]

    with open("mii.bin", "wb") as fp:
        fp.write(mii)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("usage: amii_getter.exe <amiibo-path>")