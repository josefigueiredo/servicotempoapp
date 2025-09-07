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


CREATE TABLE tbl_tempaparente(time INTEGER,
		tempaparente	REAL, 
		FOREIGN KEY(time) REFERENCES tbl_leituras(time) );

CREATE TABLE tbl_ultimoProcessado(time INTEGER,
		FOREIGN KEY(time) REFERENCES tbl_leituras(time) );

COMMIT

