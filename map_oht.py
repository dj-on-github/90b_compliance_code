
biases = [0.1+(0.01*x) for x in range(81)]
sccs   = [(-0.9)+(0.01*x) for x in range(181)]

print("bias, scc, oht_health_ratio")
for bias in biases:
    for correlation in sccs:
        start = f"djenrandom -m markov_2_param --correlation={correlation} --bias={bias} -k 100 | ./drng_oht.py -q | grep "
        hr = "\"Health ratio\""
        awk = "| awk \'{ print "
        location = f"\"{bias},\" , \"{correlation}, \""
        ending = " $4 }\'"

        print(start, hr, awk, location, ending)

