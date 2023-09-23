import { useCallback, useEffect, useState } from "react"
import fetcher from '../utils/fetcher'
import useBooks from "../hooks/useBooks";

function BookModal({ book, open, onClose }) {
    const { mutate, books } = useBooks()
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const [title, setTitle] = useState(book?.title)
    const [price, setPrice] = useState(book?.price)
    const [isbn, setISBN] = useState(book?.isbn)

    const handleSubmit = useCallback((e) => {
        e.preventDefault()

        const payload = {
            title,
            price,
            isbn
        }
        console.log(payload)

        if (book?.id) {
            fetcher().put(`/books/${book?.id}`, payload)
                .then((response) => {
                    setMessage(response.data.message)
                    const bks = [...books]
                    if (book?.id) {
                        const i = bks.findIndex((bk) => bk.id === response?.data?.book_data?.id)
                        if (i >= 0) bks[i] = response.data.book_data
                    } else {
                        bks.push(response.data.book_data)
                    }

                    mutate(bks)
                    setLoading(false)

                    onClose(false)
                })
                .catch((error) => {
                    console.error('Error fetching data:', error);
                    setError(error.response.data.message)
                    setLoading(false);
                });

            return
        }

        fetcher().post('/books', payload)
            .then((response) => {
                // setData(response.data);
                console.log(response.data)
                setMessage(response.data.message)
                mutate([...books, response.data.book_data])
                setLoading(false)

                onClose(false)
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                setError(error.message)
                setLoading(false);
            });
    }, [mutate, books, setLoading, setMessage, setError, onClose, book, price, title, isbn])

    useEffect(() => {
        console.log(book)
        setTitle(book?.title || '')
        setPrice(book?.price || undefined)
        setISBN(book?.isbn || '')
    }, [book])

    return (
        <div id="defaultModal" tabIndex="-1" aria-hidden={!open} className={`${!open && 'hidden '}overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-modal md:h-full flex bg-gray-400 bg-opacity-50`}>
            <div className="relative p-4 w-full max-w-2xl h-full md:h-auto">
                <div className="relative p-4 bg-white rounded-lg shadow dark:bg-gray-800 sm:p-5">
                    <div className="flex justify-between items-center pb-4 mb-4 rounded-t border-b sm:mb-5 dark:border-gray-600">
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {!!book ? 'Update Book' : 'Add Book'}
                        </h2>
                        <button type="button" onClick={() => onClose()} className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-toggle="defaultModal">
                            <svg aria-hidden="true" className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
                            <span className="sr-only">Close modal</span>
                        </button>
                    </div>

                    {error && <p className='text-red-500'>{error}</p>}
                    {message && <p className='text-green-500'>{message}</p>}

                    <form onSubmit={handleSubmit}>
                        <div className="grid gap-4 mb-4 sm:grid-cols-2">
                            <div class="sm:col-span-2">
                                <label htmlFor="title" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Title</label>
                                <input type="text" name="title" onChange={(e) => setTitle(e.target.value)} id="title" value={title} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Book title" required />
                            </div>
                            <div>
                                <label htmlFor="price" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Price</label>
                                <input type="number" name="price" onChange={(e) => setPrice(e.target.value)} id="price" value={price} min='0' className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="$999" required />
                            </div>
                            <div>
                                <label htmlFor="isbn" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">ISBN</label>
                                <input type="text" name="isbn" id="isbn" onChange={(e) => setISBN(e.target.value)} value={isbn} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="ISBN" required />
                            </div>
                        </div>
                        <button disabled={loading} type="submit" className="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                            Submit
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default BookModal
