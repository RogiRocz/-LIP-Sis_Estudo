from fastapi import FastAPI
from src.routers import auth, user, disciplina, tema, revisao
from src.database import Base, engine
from sqlalchemy import text
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE OR REPLACE FUNCTION update_revisao_status()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.data_realizada IS NOT NULL THEN
                    NEW.status := 'REALIZADA';
                ELSIF NEW.data_prevista < CURRENT_DATE THEN
                    NEW.status := 'ATRASADA';
                ELSE
                    NEW.status := 'PENDENTE';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))
        connection.execute(text("""
            DROP TRIGGER IF EXISTS trg_update_revisao_status ON "Revisao";
        """))
        connection.execute(text("""
            CREATE TRIGGER trg_update_revisao_status
            BEFORE INSERT OR UPDATE ON "Revisao"
            FOR EACH ROW
            EXECUTE FUNCTION update_revisao_status();
        """))
        connection.commit()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(disciplina.router)
app.include_router(tema.disciplina_tema_router)
app.include_router(tema.tema_router)
app.include_router(revisao.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
