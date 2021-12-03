signal_selectivities = [
    ['0.01', 'SELECT COUNT(*) from tab1 WHERE s < -8'],
    ['0.05', 'SELECT COUNT(*) from tab1 WHERE s < -5.9'],
    ['0.1', 'SELECT COUNT(*) from tab1 WHERE s < -4'],
    ['0.5', 'SELECT COUNT(*) from tab1 WHERE s < -1.76'],
    ['1', 'SELECT COUNT(*) from tab1 WHERE s < -1.55'],
    ['5', 'SELECT COUNT(*) from tab1 WHERE s < -0.76'],
    ['10', 'SELECT COUNT(*) from tab1 WHERE s < -0.32'],
    ['20', 'SELECT COUNT(*) from tab1 WHERE s < -0.01'],
    ['38', 'SELECT COUNT(*) from tab1 WHERE s != 0'],
    ['61', 'SELECT COUNT(*) from tab1 WHERE s = 0'],
    ['79', 'SELECT COUNT(*) from tab1 WHERE s >= 0'],
    ['100', 'SELECT COUNT(*) from tab1']
]

time_selectivities = [
    ['0.01', 'SELECT COUNT(*) from tab1 WHERE t < 1549029041.4683867'],
    ['0.05', 'SELECT COUNT(*) from tab1 WHERE t < 1549029043.3400252'],
    ['0.1', 'SELECT COUNT(*) from tab1 WHERE t < 1549029045.6795733'],
    ['0.5', 'SELECT COUNT(*) from tab1 WHERE t < 1549029064.3959584'],
    ['1', 'SELECT COUNT(*) from tab1 WHERE t < 1549029087.79144'],
    ['5', 'SELECT COUNT(*) from tab1 WHERE t < 1549029274.9552913'],
    ['10', 'SELECT COUNT(*) from tab1 WHERE t < 1549029508.9101057'],
    ['20', 'SELECT COUNT(*) from tab1 WHERE t < 1549029976.8197343'],
    ['30', 'SELECT COUNT(*) from tab1 WHERE t < 1549030444.7293627'],
    ['40', 'SELECT COUNT(*) from tab1 WHERE t < 1549030912.6389914'],
    ['50', 'SELECT COUNT(*) from tab1 WHERE t < 1549031380.54862'],
    ['60', 'SELECT COUNT(*) from tab1 WHERE t < 1549031848.4582486'],
    ['70', 'SELECT COUNT(*) from tab1 WHERE t < 1549032316.3678772'],
    ['80', 'SELECT COUNT(*) from tab1 WHERE t < 1549032784.2775056'],
    ['90', 'SELECT COUNT(*) from tab1 WHERE t < 1549033252.1871343'],
    ['100', 'SELECT COUNT(*) from tab1']
]

time_selectivities_2 = [
    ["0.01", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:50:41'"],
    ["0.05", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:50:43'"],
    ["0.1", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:50:45'"],
    ["0.5", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:51:04'"],
    ["1", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:51:27'"],
    ["5", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:54:34'"],
    ["10", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 13:58:28'"],
    ["20", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:06:16'"],
    ["30", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:14:04'"],
    ["40", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:21:52'"],
    ["50", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:29:40'"],
    ["60", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:37:28'"],
    ["70", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:45:16'"],
    ["80", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 14:53:04'"],
    ["90", "SELECT COUNT(*) from tab1 WHERE t < '2019-02-01 15:00:52'"],
    ["100", "SELECT COUNT(*) from tab1"]
]
