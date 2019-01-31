import time
test = range(80)
# res = test[::-1]
# n = len(test)
# c = int(10/(n-10))
# k = c
# print(c)
# i = 0
# while True:
#     if i == c:
#         res.pop(i)
#         if len(res) == 10:
#             break
#         c += k
#     i += 1
# res = res[::-1]
# print(res)

t = time.time()
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    seq = seq[::-1]
    res = []

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    for list in out[::-1]:
        res.append(list[0])
    return res

res = chunkIt(test, 10)
print(res)
print(len(res))
elapsed = time.time() - t
print(elapsed, "seconds.")