from fastapi import FastAPI
from routers import auth, user, disciplina, tema, revisao
from database import Base, engine
from sqlalchemy import text
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("""
            CREATE OR REPLACE FUNCTION update_revisao_status()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.data_realizada IS NOT NULL THEN
                    NEW.status := '''REALIZADA''';
                ELSIF NEW.data_prevista < CURRENT_DATE THEN
                    NEW.status := '''ATRASADA''';
                ELSE
                    NEW.status := '''PENDENTE''';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))
        await conn.execute(text('''DROP TRIGGER IF EXISTS trg_update_revisao_status ON "Revisao"'''))
        await conn.execute(text("""
            CREATE TRIGGER trg_update_revisao_status
            BEFORE INSERT OR UPDATE ON "Revisao"
            FOR EACH ROW
            EXECUTE FUNCTION update_revisao_status();
        """))
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
