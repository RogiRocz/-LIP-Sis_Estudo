import axios from 'axios'

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
	headers: {
		'Content-Type': 'application/json'
	},
	withCredentials: true
})

api.interceptors.request.use((config) => {
	const token = localStorage.getItem('authToken')

	if(token){
		config.headers.set('Authorization', `Bearer ${token}`)
	}

	// Gambiarra para funcionar no ambiente virtual do google workstations que não suporta o método PUT
	if (config.method === 'put') {
        config.method = 'post';
        config.headers.set('X-HTTP-Method-Override', 'PUT');
    }

	return config
}, (error) => {
	// console.log(error)
	return Promise.reject(error)
})

export default api
