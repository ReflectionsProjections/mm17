#!/usr/bin/env python

import random, string, sys

def r():
    return"".join(random.choice(string.letters + string.digits) for i in xrange(10))

print "["


players = []
print "Starting with", len(sys.argv), "players:", " ".join(sys.argv)

