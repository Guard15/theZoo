#!/usr/bin/python

import os
import sys
import hashlib
import subprocess

BINARIES_FOLDER = "malwares/Binaries"
SOURCE_FOLDER = "malwares/Source/Original"

def _help():
    print("Please run with '%s {input folder} {output filename} {s|b}'." % sys.argv[0])
    return

def _Do(input_folder, name, type):

    if type == 'b':
        path = BINARIES_FOLDER + "/" + name
    elif type == 's':
        path = SOURCE_FOLDER + "/" + name
    else:
        print("Type Source or Binary not valid ('s' or 'b').")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        _help()
        print("Seems like '%s' is not a input_folder." % input_folder)
        sys.exit(1)

    try:
        os.makedirs(path)
    except OSError:
        print("Folder exists. Please remove it before continuing.")
        sys.exit(1)

    # Create ZIP Archive:
    try:
        subprocess.call(['7z', 'a', '-pinfected', '-y', '%s/%s.zip' % (path, name), '%s/*' % input_folder])
    except:
        print("Seems like you don't have 7z in your path. Please install or add with:\n\tbrew install 7zip #(OSX)\n\tsudo apt-get install p7zip-full #(Linux)")
        sys.exit(1)

    compressed_path = '%s/%s.zip' % (path, name)
    print("Created ZIP Archive.")
    md5sum = hashlib.md5(open(compressed_path, 'rb').read()).hexdigest()
    sha1sum = hashlib.sha1(open(compressed_path, 'rb').read()).hexdigest()
    open("%s/%s.md5" % (path, name), 'w').write(md5sum)
    open("%s/%s.sha" % (path, name), 'w').write(sha1sum)
    open("%s/%s.pass" % (path, name), 'w').write("infected")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        _help()
        sys.exit(1)

    _Do(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Please don't forget to add details to 'conf/maldb.db'.\n")
    print("Thanks for helping us get this accessible to everyone.\n")
