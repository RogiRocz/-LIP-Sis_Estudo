# LIP - Sis_Estudo

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas nas versões especificadas:

*   **Python:** 3.12.7
*   **pip:** 25.3
*   **Node.js:** 24.12.0
*   **npm:** 11.6.2

## Configuração do Ambiente

### Backend

1.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

2.  **Instale as dependências:**

    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Crie um arquivo `.env` na pasta `backend/src` com as seguintes variáveis:**

    ```
    DATABASE_URL="postgresql+asyncpg://user:password@host:port/database"
    SECRET_KEY="your_secret_key"
    ```

### Frontend

1.  **Instale as dependências:**

    ```bash
    cd frontend
    npm install
    ```

2.  **Crie um arquivo `.env` na pasta `frontend` com as seguintes variáveis:**

    ```
    VITE_API_URL="http://localhost:8000"
    VITE_SUPABASE_URL="your_supabase_url"
    VITE_SUPABASE_KEY="your_supabase_key"
    ```

## Executando a Aplicação

### Backend

1.  **Execute o servidor:**

    ```bash
    uvicorn backend.src.main:app --reload
    ```

### Frontend

1.  **Execute o servidor de desenvolvimento:**

    ```bash
    cd frontend
    npm run dev
    ```
