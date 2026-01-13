interface Usuario {
	ID?: number
	supabase_id?: string
	nome: string
	email: string
	ui_theme: string
	intervalo_revisoes: number[]
	senha?: string
	confirmar_senha?: string
}

interface TokenResponse {
	token: string
	refresh_token: string
	expires_at: string
	token_type: string
	user: Usuario
}

interface RefreshTokenResponse {
	token: string
	refresh_token?: string
	token_type: string
	expires_at: string
}

interface RefreshTokenRequest {
	refresh_token: string
}

interface PageParams {
	page?: number
	size?: number
}

interface Page<T> {
	items: T[]
	total: number
	page: number
	size: number
	pages: number
}

interface Tema {
	ID?: number
	disciplina_id: number
	nome: string
	descricao: string
}

interface Disciplina {
	ID?: number
	tema_id?: number
	nome: string
	descricao: string | null
	cor: string
}

interface Revisao {
	ID?: number
	tema_id?: number
	data_prevista: string | null
	data_realizada: string | null
	tempo_dedicado: number | null
	status: string
	descricao: string | null
}

interface Estatisticas {
	total_disciplinas: number
	total_temas: number
	total_revisoes: number
	revisoes_hoje: number
}

interface EvolucaoSemanal {
	data: string
	revisoes_realizadas: number
}

interface RevisaoDoDia {
	id_revisao: number
	titulo_tema: string
	nome_disciplina: string
}

interface SeedRequest {
	num_disciplinas?: number
	num_temas_por_disciplina?: number
	dias_retroceder?: number
}

interface SeedResponse {
	disciplinas_criadas: number
	temas_criados: number
	revisoes_criadas: number
	mensagem: string
}

export type {
	Usuario,
	TokenResponse,
	RefreshTokenResponse,
	RefreshTokenRequest,
	PageParams,
	Page,
	Tema,
	Disciplina,
	Revisao,
	Estatisticas,
	EvolucaoSemanal,
	RevisaoDoDia,
	SeedRequest,
	SeedResponse,
}
