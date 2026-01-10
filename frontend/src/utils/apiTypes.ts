interface Usuario {
	nome: string
	email: string
	ui_theme: string
	intervalo_revisoes: number[]
}

interface AuthResponse {
	token: string
	user: Usuario
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
  total_disciplinas: number;
  total_temas: number;
  total_revisoes: number;
  revisoes_hoje: number;
}

interface EvolucaoSemanal {
  data: string;
  revisoes_realizadas: number;
}

interface RevisaoDoDia {
  id_revisao: number;
  titulo_tema: string;
  nome_disciplina: string;
}

export type {
	Usuario,
	AuthResponse,
	PageParams,
	Page,
	Tema,
	Disciplina,
	Revisao,
	Estatisticas,
	EvolucaoSemanal,
	RevisaoDoDia
}
