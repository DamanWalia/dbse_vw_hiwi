import os
import psycopg2
from timeit import default_timer as timer

start = timer()
conn = psycopg2.connect("host=localhost dbname=postgres user=[username] password=[passwd]")


for filename in os.listdir("[folder path]"):
	cur = conn.cursor()
	with open(filename, 'r') as f:
        # Notice that we don't need the `csv` module.
    		next(f) # Skip the header row.
    		cur.copy_from(f, '[TABLE NAME]', sep=',')

#	conn.commit()
end = timer()
print(end - start)
