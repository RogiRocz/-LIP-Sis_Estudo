export const formatarData = (dataStr: string) => {
	const date = new Date(dataStr)

	const options: Intl.DateTimeFormatOptions = {
		year: 'numeric',
		month: '2-digit',
		day: '2-digit',
		timeZone: 'UTC',
	}

	return date.toLocaleDateString('pt-BR', options)
}
