import useSWR from 'swr'
import fetcher from '../utils/fetcher'

const bookFetcher = () => fetcher().get('/books')
    .then((response) => {
        return response.data.book_data
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
        throw error
    });

function useBooks() {
    const { data, mutate, error } = useSWR('/books', bookFetcher);
    const loading = !data && !error;

    return {
        books: data,
        mutate,
        error,
        loading,
    }
}

export default useBooks
