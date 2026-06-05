import axios from 'axios';
import config from '../config/index.js';
import { handleFulfilled, handleRejected, handleRequest } from './utils/index.js';

const client = axios.create({
  baseURL: 'https://serpapi.com',
  timeout: config.SERPAPI_TIMEOUT,
  headers: {
    'Accept-Encoding': 'gzip, deflate, compress',
  },
});

client.interceptors.request.use((c) => {
  c.params = {
    key: config.SERPAPI_API_KEY,
    ...c.params,
  };
  return handleRequest(c);
});

client.interceptors.response.use(handleFulfilled, (err) => {
  if (err.response?.data?.error) {
    err.message = err.response.data.error;
  }
  return handleRejected(err);
});

const search = ({
  location = config.SERPAPI_LOCATION,
  q,
}) => {
  const params = { location, q };
  if (config.SERPAPI_LANG) params.lr = config.SERPAPI_LANG;
  return client.get('/search', { params });
};

export {
  search,
};

export default null;
