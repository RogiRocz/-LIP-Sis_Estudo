export const formatarData = (dataStr: string) => {
	const dateForm = new Date(dataStr).toLocaleDateString('pt-BR', {
		timeZone: 'America/Sao_Paulo',
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
	return dateForm
}
