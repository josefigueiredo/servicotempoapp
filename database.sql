DROP TABLE tbl_sensores;
DROP table tbl_leituras;

CREATE table tbl_sensores(
	id_sensor INTEGER PRIMARY KEY,
	tipo	TEXT,
	local	TEXT);

INSERT INTO tbl_sensores(id_sensor,tipo,local) VALUES(1,"Tipo a","Sacada");


CREATE TABLE tbl_leituras(time INTEGER PRIMARY KEY, 
		sensor INTEGER, h REAL, t REAL, p REAL, 
		FOREIGN KEY(sensor) REFERENCES tbl_sensores(sensor_id) );


COMMIT

