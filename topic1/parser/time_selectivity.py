import datetime

mn = 1549029041.000477 - 3600
mx = 1549033720.096763 - 3600

diff = (mx - mn)

limits = []
sels = [0.01, 0.05, 0.1, 0.5, 1, 5] + list(range(10, 110, 10))

for i in range(len(sels)):
    sel = sels[i]
    val = min(mx, mn + diff * sel / 100)
    val = datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S')
    limits.append(val)

for l in limits:
    print(l)
