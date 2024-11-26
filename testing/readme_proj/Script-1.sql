    ALTER TABLE RECORDS 
    ADD COLUMN 新地址 TEXT

    ALTER TABLE RECORDS 
    ADD COLUMN 行政區 TEXT
    
    ALTER TABLE RECORDS 
    ADD COLUMN Lat TEXT
    
    ALTER TABLE RECORDS 
    ADD COLUMN Lon TEXT
    
    ALTER TABLE RECORDS 
    ADD COLUMN 日期 TEXT
    
   	SELECT 新地址,行政區 FROM records 
   	WHERE 新地址 LIKE '%東區%'
   	
   	UPDATE records SET 行政區 = '大安區' WHERE 行政區 = '東區地下街'
   	
	SELECT strftime('%Y-%m-%d', 
	                substr(RCVdate , 1, 4) || '-' || substr(RCVdate , 5, 2) || '-' || substr(RCVdate , 7, 2)) 
	       AS formatted_date
	FROM records
	
	UPDATE records 
	SET 日期=  (SELECT strftime('%Y-%m-%d', 
	              substr(RCVdate , 1, 4) || '-' || substr(RCVdate , 5, 2) || '-' || substr(RCVdate , 7, 2)) )
	              
    SELECT 日期,
    新地址,
	printf("%.6f", ROUND(lat, 6)) AS Lat ,
    printf("%.6f", ROUND(lon, 6)) as Lon 
    FROM records
    ORDER BY RCVdate DESC
   
    SELECT c.Bill_code, c.Lat, c.Lon
    FROM coordinates c
    JOIN records r ON c.Bill_code = r.Bill_code
    WHERE r.新地址 = '臺灣10554臺北市中崙松山區美仁里八德路三段25城市舞台';
    
    SELECT r.新地址 
    FROM coordinates c
    JOIN records r ON c.Bill_code = r.Bill_code
    WHERE r.Bill_code = '10967113569468';
   
   SELECT 新地址
   from records r 
   WHERE Bill_code = '10967113569840'
   
