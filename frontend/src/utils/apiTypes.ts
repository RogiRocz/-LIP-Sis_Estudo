interface Usuario {
    nome: string
    email: string
    ui_theme: string
    intervalo_revisoes: string
}

interface AuthResponse {
    token: string;
    user: Usuario;
}

export type {
    Usuario,
    AuthResponse
}