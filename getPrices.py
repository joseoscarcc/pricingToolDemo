# import packages
import psycopg2
import pandas as pd
import datetime
import config
  
# establish connections
conn1 = psycopg2.connect(database=config.db,
                         host=config.hosting,
                         user=config.usuario,
                         password=config.contrasena,
                         port=config.puerto)
  
conn1.autocommit = True
cursor = conn1.cursor()
  
sql = """
        select s.place_id, s.cre_id, s.marca, s.x,s.y, s.prices, s.product, s.compite_a, (s.prices - precios_site.prices) as "dif"
from (select c.place_id, c.cre_id, c.marca, c.x,c.y, p.prices, p.product, c.compite_a from demo_competencia AS c
left join precios_site AS p
on c.place_id = CAST(p.place_id AS INT)
WHERE p.date = (SELECT MAX(date) FROM precios_site)) s
left join 
precios_site
on s.compite_a = CAST(precios_site.place_id AS INT) and s.product = precios_site.product
WHERE precios_site.date = (SELECT MAX(date) FROM precios_site) 
"""
sql2 = """
    select c.place_id, c.cre_id, c.marca, p.date, p.prices, p.product, c.compite_a from demo_competencia AS c
left join precios_site AS p
on c.place_id = CAST(p.place_id AS INT)
WHERE p.date > now() - interval '30 day'
"""
sql3 = """
    select * from demo_sites
"""
worktable = pd.read_sql_query(sql, conn1)
preciosHist = pd.read_sql_query(sql2,conn1)
TGSites = pd.read_sql_query(sql3, conn1)
conn1.commit()
conn1.close()

worktable['dif'].round(2)