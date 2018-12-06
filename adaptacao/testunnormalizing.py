def unnormalization(x, max, min, range_a, range_b):
    z = []
    for i in range(0, len(x)):
        j = ((float(x[i]) - float(range_a))*(float(max)-float(min)))/ (float(range_b) - float(range_a)) + float(min)
        z.append(j)
    return z
def normalization(x, min, max, range_a, range_b):
	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z

x = [20, 30]

max = 45
min = 12
range_a = 0.15
range_b = 0.85

x_ = [normalization(x[0], min, max, range_a, range_b), normalization(x[1], min, max, range_a, range_b)]

y = unnormalization(x_, max, min, range_a, range_b)

print(x, y)	    