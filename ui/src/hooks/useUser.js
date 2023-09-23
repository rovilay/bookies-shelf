import useSWR from 'swr'
import fetcher from '../utils/fetcher'

const userFetcher = () => fetcher().get('/me')
    .then((response) => {
        return response.data.user
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
        throw error
    });

function useUser() {
    const { data, mutate, error } = useSWR('/me', userFetcher);
    const loading = !data && !error;
    const loggedOut = error && error?.response?.status === 401;

    return {
        user: data,
        mutate,
        error,
        loading,
        loggedOut
    }
}

export default useUser
