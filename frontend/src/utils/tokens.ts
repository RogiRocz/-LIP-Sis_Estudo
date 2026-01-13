// utils/tokens.js
export const isTokenExpired = (expiryDate) => {
	if (!expiryDate) return true

	try {
		const now = new Date()
		const expiry = new Date(expiryDate)
		return now >= expiry
	} catch (error) {
		console.error('Erro ao verificar expiração do token:', error)
		return true
	}
}

export const shouldRefreshToken = (expiryDate, thresholdMDays = 7) => {
	if (!expiryDate) return true

	try {
		const now = new Date()
		const expiry = new Date(expiryDate)
		const threshold = thresholdMDays * 24 * 60 * 60 * 1000

		return expiry.getTime() - now.getTime() <= threshold
	} catch (error) {
		console.error('Erro ao verificar refresh do token:', error)
		return true
	}
}

export const getTokenRemainingTime = (expiryDate) => {
	if (!expiryDate) return 0

	try {
		const now = new Date()
		const expiry = new Date(expiryDate)
		return expiry.getTime() - now.getTime()
	} catch (error) {
		console.error('Erro ao calcular tempo restante do token:', error)
		return 0
	}
}
