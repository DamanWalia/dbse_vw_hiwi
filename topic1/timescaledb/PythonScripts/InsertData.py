import csv
import psycopg2
from timeit import default_timer as timer
 
start = timer()
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = conn.cursor()
with open('[filename]', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cur.execute(
        "INSERT INTO users VALUES (%s, %s, %s, %s)",
        row
    )
    conn.commit()
end = timer()
print(end - start)
