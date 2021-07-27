import math
import sys
import os

print("bias, entropy, health_ratio")

for i in range(101):
    bias = 0.01*i
    astr = "djenrandom -m biased --bias=%0.02f -k 16 | python2.7.5 ./drng_oht.py -q -t" % bias
     
    p = max(bias, 1.0-bias)
    entropy = -math.log(p,2)

    print(f"{bias:0.4f},{entropy:0.4f},",end="")
    sys.stdout.flush()
    os.system(astr)
    sys.stdout.flush()



