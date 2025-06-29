import axios from 'axios'

const BACKEND_API = 'http://localhost:5000'
const api = axios.create({
    baseURL: BACKEND_API,
    headers: {
        'Content-Type': 'application/json',
    },
})






export default api