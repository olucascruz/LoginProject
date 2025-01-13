from sqlalchemy.ext.declarative import declarative_base

# URL de conexão com o banco PostgreSQL
DATABASE_URL = "postgresql://postgres:password123@localhost:5432/teste"



# Base para modelos
Base = declarative_base()
