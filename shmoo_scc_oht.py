import math
import sys
import os

print("bias, entropy, health_ratio")

for i in range(201):
    scc = -1.0 + (0.01*i)
    astr = "djenrandom -m correlated --correlation=%0.02f -k 16 | python2.7.5 ./drng_oht.py -q -t" % scc
     
    p = (abs(scc)/2.0)+0.5
    entropy = -math.log(p,2)

    print(f"{scc:0.4f},{entropy:0.4f},",end="")
    sys.stdout.flush()
    os.system(astr)
    sys.stdout.flush()



