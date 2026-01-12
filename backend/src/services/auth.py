from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserLogin, User
from ..schemas.auth import Token
from ..security import verify_password, create_access_token, get_password_hash
from ..core.config import settings
from ..core.supabase_client import supabase
import uuid

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.user_repo = UserRepository(db)
        self.db = db

    async def register(self, user_data: UserCreate) -> Token:
        if user_data.senha != user_data.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="As senhas não conferem"
            )

        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado"
            )

        # 1. Criar usuário no Supabase Auth
        try:
            print(f"Criando usuário no Supabase Auth: {user_data.email}")
            
            # Usa a API do Supabase para criar o usuário
            auth_response = supabase.auth.admin.create_user({
                "email": user_data.email,
                "password": user_data.senha,
                "email_confirm": True,  # Auto-confirma o email para desenvolvimento
                "user_metadata": {
                    "nome": user_data.nome
                }
            })
            
            supabase_user = auth_response.user
            supabase_id = str(supabase_user.id)
            
            print(f"Usuário criado no Supabase Auth com ID: {supabase_id}")
            
        except Exception as e:
            print(f"Erro ao criar usuário no Supabase Auth: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar usuário no sistema de autenticação: {str(e)}"
            )

        # 2. Criar usuário na sua tabela local
        hashed_password = get_password_hash(user_data.senha)
        
        db_user = await self.user_repo.create_user(user_data, hashed_password)
        db_user.ui_theme = settings.DEFAULT_THEME
        db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
        db_user.supabase_id = uuid.UUID(supabase_id)  # Converte para UUID
        
        await self.user_repo.update_user(db_user)
        
        print(f"Usuário criado na tabela local com ID: {db_user.ID}")

        # 3. Gerar token JWT
        token = create_access_token(
            data={
                "sub": supabase_id, 
                "email": db_user.email,
                "nome": db_user.nome,
                "role": "authenticated", 
                "aud": "authenticated"
            }
        )
        
        user_schema = User.model_validate(db_user)
        return Token(token=token, token_type="bearer", user=user_schema)

    async def login(self, user_data: UserLogin) -> Token:
        # 1. Tentar autenticar no Supabase
        try:
            print(f"Tentando login no Supabase: {user_data.email}")
            
            auth_response = supabase.auth.sign_in_with_password({
                "email": user_data.email,
                "password": user_data.senha
            })
            
            supabase_user = auth_response.user
            supabase_id = str(supabase_user.id)
            
            print(f"Login bem-sucedido no Supabase: {supabase_id}")
            
        except Exception as e:
            print(f"Erro no login do Supabase: {e}")
            
            # Fallback: Verificar na base local (para compatibilidade)
            db_user = await self.user_repo.get_user_by_email(user_data.email)
            if not db_user or not verify_password(user_data.senha, db_user.senha):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email ou senha incorretos",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Se o usuário não tem supabase_id, tentar vincular
            if not db_user.supabase_id:
                try:
                    # Buscar usuário no Supabase pelo email
                    auth_users = supabase.auth.admin.list_users()
                    for auth_user in auth_users:
                        if auth_user.email == user_data.email:
                            db_user.supabase_id = uuid.UUID(str(auth_user.id))
                            await self.user_repo.update_user(db_user)
                            supabase_id = str(auth_user.id)
                            break
                except Exception as supabase_error:
                    print(f"Erro ao vincular com Supabase: {supabase_error}")
                    # Se não conseguir vincular, usa o ID local
                    supabase_id = f"local-{db_user.ID}"
            else:
                supabase_id = str(db_user.supabase_id)

        # 2. Buscar ou criar usuário na tabela local
        db_user = await self.user_repo.get_user_by_email(user_data.email)
        
        if not db_user:
            # Se o usuário existe no Supabase mas não na tabela local, criar
            print(f"Usuário {user_data.email} existe no Supabase mas não localmente. Criando...")
            
            hashed_password = get_password_hash(user_data.senha)
            
            db_user = await self.user_repo.create_user(
                UserCreate(
                    email=user_data.email,
                    nome=user_data.email.split('@')[0],  # Nome padrão
                    senha=user_data.senha,
                    confirmar_senha=user_data.senha
                ),
                hashed_password
            )
            
            db_user.ui_theme = settings.DEFAULT_THEME
            db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
            
            if supabase_id and not supabase_id.startswith("local-"):
                db_user.supabase_id = uuid.UUID(supabase_id)
            
            await self.user_repo.update_user(db_user)

        # 3. Gerar token JWT
        token = create_access_token(
            data={
                "sub": supabase_id,
                "email": db_user.email,
                "nome": db_user.nome,
                "role": "authenticated", 
                "aud": "authenticated"
            }
        )
        
        user_schema = User.model_validate(db_user)
        return Token(token=token, token_type="bearer", user=user_schema)