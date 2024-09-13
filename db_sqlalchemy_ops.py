import sqlalchemy as db
from sqlalchemy import inspect

# Подключение к базе данных
engine = db.create_engine('sqlite:///cocktails-sqlachemy.db')
connection = engine.connect()

# Получаем объект инспектора для работы с метаданными
inspector = inspect(engine)

# Проверка существования таблицы и её удаление, если она существует
if 'recipes' in inspector.get_table_names():
    metadata = db.MetaData()
    recipes_table = db.Table("recipes", metadata, autoload_with=engine)
    recipes_table.drop(engine)

# Определение таблицы заново
metadata = db.MetaData()
recipes_table = db.Table("recipes", metadata,
    db.Column('recipe_id', db.Integer, primary_key=True),
    db.Column('name', db.String, nullable=False),
    db.Column('instruction', db.Text, nullable=False),
)

# Создание таблицы
metadata.create_all(engine)

# Вставка данных
try:
    insertion_query = recipes_table.insert().values([
        {'name': 'Gin-tonic', 'instruction': 'Mix it 1 to 4'},
        {'name': 'Whiskey-cola', 'instruction': 'Mix it 1 to 3'}
    ])
    result = connection.execute(insertion_query)
    print(f"{result.rowcount} rows inserted.")
except Exception as e:
    print(f"An error occurred: {e}")

# Проверка данных
try:
    # Создаем запрос, выбирающий все данные из таблицы
    select_query = db.select(recipes_table)
    result = connection.execute(select_query).fetchall()
    
    print("Data in 'recipes' table:")
    for row in result:
        print(row)
except Exception as e:
    print(f"An error occurred while selecting data: {e}")

# Закрытие соединения
connection.close()


