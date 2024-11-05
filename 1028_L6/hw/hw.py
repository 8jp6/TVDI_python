import hwresource
import sqlite3

sql = '''
CREATE TABLE IF NOT EXISTS records (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   
	sitename TEXT NOT NULL,
	county TEXT,
	aqi INTEGER,
	status TEXT,
	pm25 NUMERIC,
	date TEXT,
	lat NUMERIC,
	lon NUMERIC,
    UNIQUE(id,sitename,county,aqi,status,pm25,date,lat,lon)
);
'''

conn = sqlite3.connect("aqi1.db")
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
cursor.close()

insertSQL = '''
INSERT INTO records (sitename, county, aqi, status, pm25, date, lat, lon)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''

data = hwresource.get_selected_data()
cursor = conn.cursor()
cursor.executemany(insertSQL,data)
conn.commit()


cursor.close()
conn.close()