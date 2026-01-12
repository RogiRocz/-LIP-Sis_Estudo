import asyncio
from sqlalchemy import text

# Imports relativos ao pacote 'src'
from .database import engine
from .core.supabase_client import supabase
from .core.config import settings

async def migrate_existing_users():
    """
    Migra usuários existentes para o Supabase Auth de forma eficiente.
    """
    print("Iniciando migração de usuários para Supabase Auth...")

    # 1. Buscar usuários do Supabase
    print("Buscando usuários existentes no Supabase Auth...")
    try:
        # Nas versões recentes, list_users() retorna DIRETAMENTE uma lista
        auth_users = supabase.auth.admin.list_users()
        
        # Criar um mapa de email para usuário para busca rápida
        # Tratamos 'auth_users' como lista conforme o erro anterior indicou
        supabase_users_map = {user.email: user for user in auth_users}
        print(f"Encontrados {len(supabase_users_map)} usuários no Supabase.")
    except Exception as e:
        print(f"Aviso ao buscar lista global: {e}")
        print("Tentando migração individual por tentativa de criação...")
        supabase_users_map = {}

    async with engine.begin() as conn:
        # 2. Buscar apenas usuários locais sem supabase_id
        # Nota: Usei "ID" entre aspas pois o SQLAlchemy respeita o case-sensitive do Postgres
        result = await conn.execute(
            text('SELECT "ID", email, nome FROM "Usuario" WHERE supabase_id IS NULL')
        )
        users_to_migrate = result.fetchall()

        print(f"Encontrados {len(users_to_migrate)} usuários locais pendentes.")

        migrated_count = 0
        error_count = 0

        # 3. Iterar e migrar
        for user_id, email, nome in users_to_migrate:
            try:
                print(f"\nProcessando usuário: {email}")
                supabase_id = None

                # Verificamos se ele já estava na lista que baixamos
                if email in supabase_users_map:
                    supabase_id = supabase_users_map[email].id
                    print(f"  ! Usuário já existe no Auth (ID: {supabase_id}). Vinculando...")
                else:
                    # Tenta criar o usuário
                    try:
                        auth_response = supabase.auth.admin.create_user({
                            "email": email,
                            "password": "TempPassword123!",
                            "email_confirm": True,
                            "user_metadata": {"nome": nome or email.split("@")[0]},
                        })
                        supabase_id = auth_response.user.id
                        print(f"  ✓ Usuário criado com sucesso: {supabase_id}")
                    except Exception as create_error:
                        print(f"  ✗ Erro ao criar/localizar no Supabase: {create_error}")
                        error_count += 1
                        continue

                # 4. Atualiza o banco local
                if supabase_id:
                    await conn.execute(
                        text('UPDATE "Usuario" SET supabase_id = :supabase_id WHERE "ID" = :user_id'),
                        {"supabase_id": supabase_id, "user_id": user_id},
                    )
                    migrated_count += 1
                    print(f"  ✓ Banco local atualizado para {email}")

            except Exception as e:
                print(f"  ✗ Erro inesperado no usuário {email}: {e}")
                error_count += 1

        await conn.commit()

    print(f"\n--- Resumo da Migração ---")
    print(f"Migrados/Vinculados: {migrated_count}")
    print(f"Erros: {error_count}")

if __name__ == "__main__":
    print("Executando script de migração...")
    asyncio.run(migrate_existing_users())
    print("Script finalizado.")