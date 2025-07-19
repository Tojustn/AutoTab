import axios from "axios";

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || "5000";
const BACKEND_API = `http://localhost:${BACKEND_PORT}/api`;
const api = axios.create({
  baseURL: BACKEND_API,
});

export default api;
