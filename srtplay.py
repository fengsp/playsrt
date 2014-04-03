"""
    srtplay
    ~~~~~~~

    Play srt subtitle in your terminal.

    :copyright: (c) 2014 by fsp.
    :license: BSD.
"""
import sys
import time
import codecs


def strtosecond(string):
    hms, ms = string.split(',')
    h, m, s = hms.split(':')
    h, m, s, ms = int(h), int(m), int(s), int(ms)
    seconds = h * 3600 + m * 60 + s + float(ms)/1000
    return seconds


class Node(object):
    """One play node.
    """
    def __init__(self):
        self.seq = None
        self.start = None
        self.end = None
        self.content = []
        self.displayed = False

    def add(self, line):
        if not self.seq:
            try:
                self.seq = int(line)
            except:
                print line
        elif not self.start:
            start, end = line.split(" --> ")
            self.start, self.end = strtosecond(start), strtosecond(end)
        else:
            self.content.append(line)


def play(source):
    """Play the srt source file.

    :param source: The srt source content.
    """
    lines = source.splitlines()
    nodes = []
    current = Node()
    for line in lines:
        if line:
            current.add(line)
        else:
            if current.seq:
                nodes.append(current)
            current = Node()

    start_time = time.time()
    for node in nodes:
        current_time = time.time() - start_time
        time.sleep(node.start - current_time)
        print "\n".join(node.content)
        time.sleep(node.end - node.start)


def usage():
    return """Usage:
python srtplay.py filepath encoding"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print usage()
        sys.exit(0)
    elif len(sys.argv) < 3:
        filepath = sys.argv[1]
        encoding = "utf-8"
    else:
        filepath = sys.argv[1]
        encoding = sys.argv[2]
    
    source = codecs.open(filepath, encoding=encoding).read()
    try:
        play(source)
    except KeyboardInterrupt:
        print ""
        sys.exit(0)
