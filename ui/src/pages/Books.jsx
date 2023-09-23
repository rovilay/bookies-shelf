import React, { useEffect, useState } from 'react';
import useUser from '../hooks/useUser';
import { useNavigate } from 'react-router-dom';
import useBooks from '../hooks/useBooks';
import BookCard from '../components/BookCard';
import BookModal from '../components/BookModal';
import { Spinner } from 'flowbite-react';

function Books() {
    const { user, loading: userLoading } = useUser()
    const { books, loading } = useBooks()
    const navigate = useNavigate()

    const [openModal, setOpenModal] = useState(false)
    const [bookToUpdate, setBookToUpdate] = useState(null)

    useEffect(() => {
        if (!user && !userLoading) return navigate('/login')
    }, [user, navigate, userLoading, books])

    if (loading) return <Spinner />

    return (
        <>
            <div className="bg-white">
                <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold tracking-tight text-gray-900">All Books</h2>
                        <button
                            type="button" 
                            onClick={() => {
                                setOpenModal(true)
                            }} 
                            className="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
                        >
                            Add book
                        </button>
                    </div>

                    <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
                        {books?.map((bk, i) => <BookCard key={i} book={bk} onClick={() => {
                            setBookToUpdate(bk)
                            setOpenModal(true)
                        }} />)}
                    </div>
                </div>
            </div>

            {openModal && <BookModal open={openModal} onClose={() => {
                setOpenModal(false)
                setBookToUpdate(null)
            }} book={bookToUpdate} />}
        </>

    )
}

export default Books
