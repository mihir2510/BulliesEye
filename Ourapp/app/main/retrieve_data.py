from sqlalchemy.engine import create_engine
from sqlalchemy import inspect
engine = create_engine('sqlite:///../../database.db')
conn = engine.connect()

data = conn.execute("SELECT * FROM Tweets")

inspector = inspect(engine)

# Get table information
print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('Tweets'))

for da in data:
    print(da[1])
    # for a in da:
    #     print(a)

