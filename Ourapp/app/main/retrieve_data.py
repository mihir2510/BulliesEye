from sqlalchemy.engine import create_engine
from sqlalchemy import inspect
engine = create_engine('sqlite:///./tweets.db')
conn = engine.connect()

data = conn.execute("SELECT * FROM Tweets")

inspector = inspect(engine)

# # Get table information
# print(inspector.get_table_names())

# # Get column information
# print(inspector.get_columns('Tweets'))
print(inspector.get_columns('affective_sense'))
# print(inspector.get_columns('tweets'))
for da in data:
    print(da[4])
    # for a in da:
    #     print(a)

