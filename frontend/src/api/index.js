import axios from 'axios';

const $host = axios.create({
  baseURL: '/',
  timeout: 5000,
  withCredentials: true,
});

export default $host;