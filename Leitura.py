import orm_sqlite


class Leitura(orm_sqlite.Model):
    time = orm_sqlite.IntegerField(primary_key=True)
    sensor = orm_sqlite.IntegerField()
    humidade = orm.sqlite.FloatField()
    temperatura = orm.sqlite.FloatField()
    pressao = orm.sqlite.FloatField()


db = orm_sqlite.Database('leituras.db')

Leitura.objects.backend = db

leitura = 


timestamp INTEGER PRIMARY KEY, 
		sensor INTEGER, h REAL, t REAL, p REAL,