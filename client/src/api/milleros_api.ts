import axios from "axios";


export const milleros_api = axios.create({
  baseURL: import.meta.env.VITE_MILLEROS_BASE_URL ?? "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  }
})
