import axios from "axios";

const BACKEND_API = "http://localhost:5000/api";
const api = axios.create({
  baseURL: BACKEND_API,
});

export default api;
