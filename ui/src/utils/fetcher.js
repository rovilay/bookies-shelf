import axios from 'axios'

const instance = () => {
  const token = localStorage.getItem('bsu') || '';
  return axios.create({
    baseURL: `${process.env.REACT_APP_BASE_URL}`,
    headers: {
      Authorization: `Bearer ${token}`
    },
  });
};

export default instance;

