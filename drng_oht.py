#!/usr/bin/env python
import sys
from optparse import OptionParser
import Queue


class drng_oht():

    def __init__(self, quiet):
        self.sample = list()
        self.sampleindex=0
        self.queue = Queue.Queue()
        self.block = 0
        self.leftoverbyte=False
        self.byte=0x00
        self.quiet = quiet
        self.healthycount = 0
        self.unhealthycount = 0
        self.finish = 0

    def ascii_to_nibble(self,a):
        if a=='0':
            return (True,0)
        if a=='1':
            return (True,1)
        if a=='2':
            return (True,2)
        if a=='3':
            return (True,3)
        if a=='4':
            return (True,4)
        if a=='5':
            return (True,5)
        if a=='6':
            return (True,6)
        if a=='7':
            return (True,7)
        if a=='8':
            return (True,8)
        if a=='9':
            return (True,9)
        if a=='a':
            return (True,10)
        if a=='b':
            return (True,11)
        if a=='c':
            return (True,12)
        if a=='d':
            return (True,13)
        if a=='e':
            return (True,14)
        if a=='f':
            return (True,15)
        if a=='A':
            return (True,10)
        if a=='B':
            return (True,11)
        if a=='C':
            return (True,12)
        if a=='D':
            return (True,13)
        if a=='E':
            return (True,14)
        if a=='F':
            return (True,15)
        return (False,0)

    def gimme_a_byte(self):
        byte = self.queue.get()
        return byte

    def get_a_byte(self):
        finish=0
        try:
            while True and finish==0:
                ch = sys.stdin.read(1)
                if len(ch)==0: #EOF?
                    raise EOFError
                    break
                (good,highnibble) = self.ascii_to_nibble(ch)
                if good:
                    break
            while True and finish==0:
                ch = sys.stdin.read(1)
                if len(ch)==0: #EOF?
                    raise EOFError
                    break
                (good,lownibble) = self.ascii_to_nibble(ch)
                if good:
                    break

            byte = lownibble + (highnibble*16)
            self.queue.put(byte)
        except EOFError:
            finish=1
            #if (self.quiet==False):
            #    print "EOF"
        except KeyboardInterrupt:
            finish=1
            if (self.quiet==False):
                print "Keyboard Interrupt"
        if finish==1:
            self.finish=1

    def get_a_sample(self):
        finish = 0
        self.sampleindex=0

        while (self.queue.qsize() < 257) and (self.finish==0):
            #print "Getting a byte queue size = %d" % self.queue.qsize()
            self.get_a_byte()
            #print "Got a byte queue size = %d" % self.queue.qsize()
        if (self.finish==0):
            return True
        else:
            return False
    #Read in Data
    #length is the requested number of bytes
    #Returns (length,list_of_bytes) where length is the number of bytes actually received

    def process_a_sample(self):
        self.block +=1

        count1    = 0
        count01   = 0
        count010  = 0
        count0110 = 0
        count101  = 0
        count1001 = 0

        if self.leftoverbyte==True:
            byte = self.byte
            #if (self.quiet==False):
            #    print "%02X" % byte,
            self.leftoverbyte=False
        else:
            byte = self.gimme_a_byte()
            #if (self.quiet==False):
            #    print "%02X" % byte,
        byte2 = self.gimme_a_byte()
        #if (self.quiet==False):
        #    print "%02X" % byte2,
        for i in xrange(32):    # 32 bytes is 256 bits
            word = byte + (byte2 * 256)
            if (self.quiet==False):
                print "%02X" % byte,
            #print "Word %04X" % word
            for j in xrange(8):
                if (word & 0x01) == 0x01:
                    count1 += 1
                if (word & 0x03) == 0x01:
                    count01 += 1
                if (word & 0x07) == 0x02:
                    count010 += 1
                if (word & 0x0f) == 0x06:
                    count0110 += 1
                if (word & 0x07) == 0x05:
                    count101 += 1
                if (word & 0x0f) == 0x09:
                    count1001 += 1
                # Shift bits
                word = word >> 1
            if i < 31:
                byte = byte2
                #if (self.quiet==False):
                #    print "%02X" % byte2,
                byte2 = self.gimme_a_byte()
            else:
                self.byte = byte2
                self.leftoverbyte=True
        
        comp1    = False
        comp01   = False
        comp010  = False
        comp0110 = False
        comp101  = False
        comp1001 = False
        if ((count1 > 95) and (count1 < 160)):
            comp1=True 
        if ((count01 > 43) and (count01 < 88)):
            comp01=True 
        if ((count010 > 8) and (count010 < 59)):
            comp010=True 
        if ((count0110 > 3) and (count0110 < 36)):
            comp0110=True 
        if ((count101 > 8) and (count101 < 59)):
            comp101=True 
        if ((count1001 > 3) and (count1001 < 36)): 
            comp1001=True 

        if (comp1 and comp01 and comp010 and comp0110 and comp101 and comp1001):
            healthy=True
            self.healthycount +=1
            if (self.quiet==False):
                print "    Healthy"
        else:
            healthy=False
            self.unhealthycount +=1
            if (self.quiet==False):
                print "    Unhealthy"
            if comp1==False or True:
                if (self.quiet==False):
                    print "comp1    (96-159):%d" % count1
            if comp01==False or True:
                if (self.quiet==False):
                    print "comp01   (44-87  ):%d" % count01
            if comp010==False or True:
                if (self.quiet==False):
                    print "comp010  (9-58   ):%d" % count010
            if comp0110==False or True:
                if (self.quiet==False):
                    print "comp0110 (4-35   ):%d" % count0110
            if comp101==False or True:
                if (self.quiet==False):
                    print "comp101  (9-58   ):%d" % count101
            if comp1001==False or True:
                if (self.quiet==False):
                    print "comp1001 (4-34   ):%d" % count1001
        return healthy

    def ratios(self):
        if ((float(self.healthycount) + float(self.unhealthycount)) == 0):
            ratio = 0.0;
        else:
            ratio = (float(self.healthycount))/(float(self.healthycount) + float(self.unhealthycount))
        return (self.healthycount, self.unhealthycount, ratio)

#Handle the command line options
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Write output to <filename> instead of stdout", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_true", dest="quiet", default=False,
                  help="Don't print status messages to stdout")
parser.add_option("-t", "--csv",
                  action="store_true", dest="terse", default=False,
                  help="Don't print status messages to stdout")
#parser.add_option("-b", "--binary",
#                  action="store_true", dest="use_binary", default=False,
#                  help="Read binary. If not set, defaults to reading hex.")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Show many internal gory details")

(options, args) = parser.parse_args()

options.use_stdin = (len(args) == 0)

c = drng_oht(options.quiet)
terse = options.terse

while c.get_a_sample():
    if not options.quiet:
        print "Got a sample"
    c.process_a_sample()

(healthy, unhealthy, ratio) = c.ratios()
if terse:
    print "%0.4f" % ratio
else:
    print "Healthy Samples   : %d" % healthy
    print "Unhealthy Samples : %d" % unhealthy
    print "Health ratio      : %f" % ratio

