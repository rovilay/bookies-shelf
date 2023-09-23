from flask import request, json
from ..helpers.book_helpers import validate_book, refine_book_data
from ..helpers.user_helpers import authenticate
from ..helpers.__helpers import server_res, CustomException
from ..models.__models import Book as BookModel

Book = BookModel()

def get_all_books(secret_key):
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        personal = request.args.get('personal')
        user_id = decoded_token['id']

        if personal is None or personal == '' or personal.lower() == 'false':
            all_books = Book.get_all_books(user_id=user_id)
            response = server_res('books retrieved successfully', success=True,
                                    status=200, book_data=all_books)
            return response
        elif personal.lower() == 'true':
            personal_books = Book.get_all_books(
                personal=True, user_id=user_id)
            response = server_res('books retrieved successfully', success=True,
                                    status=200, book_data=personal_books)
            return response
        else:
            message = 'personal query can either be True or False'
            response = server_res(message, status=400)
            return response
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        response = server_res(str(e))
        return response


def get_books_by_id(secret_key, id):
    location = f'/books/{id}'
    try:
        token = request.headers.get('authorization')
        authenticate(token, secret_key)

        found_book = Book.get_book(id)
        if found_book:
            message = 'book retrieved successfully'
            response = server_res(message, success=True, book_data=found_book,
                                  status=200, location=location)
            return response
        else:
            message = f'No book matching this id: {id}'
            response = server_res(message, status=404, location=location)
            return response
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        return server_res(str(e), location=location)


def create_books(secret_key):
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        new_book_data = request.get_json()
        book = validate_book(new_book_data)

        if book['is_valid']:
            title = new_book_data['title']
            price = new_book_data['price']
            isbn = new_book_data['isbn']
            user_id = decoded_token['id']
            image = new_book_data['image'] if "image" in new_book_data and new_book_data['image'] != "" else None
            new_book = Book.add_book(title, price, isbn, user_id, image)
            book_err_msg = 'Book with the same title already exist!'
            if isinstance(new_book, Exception) and str(new_book) == book_err_msg:
                raise CustomException(book_err_msg, status=409)
            else:
                response = server_res('book created successfully',
                                      success=True, book_data=new_book, status=201)
                return response
        else:
            props = ", ".join(book['missing_props'])
            response = server_res(
                f'book parameter(s): {props} is/are missing', status=400)
            return response
    except CustomException as e:
        print(e)
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        print(e)
        return server_res(str(e))


def modify_books(secret_key, id):
    location = f'/books/{id}'
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        book_update_data = request.get_json()
        # patch_book = True if request.method == 'PATCH' else False
        # refined_book = refine_book_data(book_update_data)
        book = validate_book(book_update_data)
        print('not_validddd')

        response = None
        if book['is_valid']:
            user_id = decoded_token['id']
            updated_book = Book.update_book(id, book_update_data, user_id)
            print('is_valid', updated_book)
            if updated_book == None:
                message = f'book with id: {id} was not found'
                raise CustomException(message=message, status=404)

            if updated_book["user_id"] != user_id:
                message = f'This book does not belong to you!'
                raise CustomException(message=message, status=403)

            message = 'Update successful'
            response = server_res(message, status=200, success=True,
                                      book_data=updated_book, location=location)
        else:
            message = 'Book parameters must contain title, price and/or isbn'
            response = server_res(message, status=400, location=location)
        return response
    except CustomException as e:
        print('not_valid', e)
        error_obj = e.get_exception_obj() 
        return server_res(error_obj['message'], status=error_obj['status'])
    except Exception as e:
        print('not_validd', e)
        return server_res(str(e), location=location)


def remove_books(secret_key, id):
    location = f'/books/{id}'
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        user_id = decoded_token['id']
        book_deleted = Book.delete_book(id, user_id)
        response = None
        if book_deleted is True:
            message = 'Delete successful'
            response = server_res(message, status=200, location=location)
        elif book_deleted == 403:
            message = f'This book does not belong to you'
            response = server_res(message, status=403, location=location)
        else:
            message = f'book with id: {id} was not found'
            response = server_res(message, status=404, location=location)
        return response
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        return server_res(str(e), location=location)


def fav_book(secret_key, id):
    location = f'/books/{id}/favourites'
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        user_id = decoded_token['id']
        favourite_book = Book.favourite_book(id, user_id)
        a = json.loads(str(favourite_book))
        a.update({'favourite': True})
        response = None
        if favourite_book:
            message = 'Book added as favourite'
            response = server_res(message, status=200, location=location, book_data=a, success=True)
        else:
            message = f'book with id: {id} was not found'
            response = server_res(message, status=404, location=location)
        return response
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        return server_res(str(e), location=location)


def del_fav_book(secret_key, id):
    location = f'/books/{id}/favourites'
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        user_id = decoded_token['id']
        remove_fav_book = Book.remove_favourite_book(id, user_id)
        response = None
        if remove_fav_book is True:
            message = 'Book removed as favourite'
            response = server_res(message, status=200, location=location, success=True)
        elif remove_fav_book is False:
            message = f'book with id: {id} was not found'
            response = server_res(message, status=404, location=location)
        else:
            message = 'Book not in your favourites'
            response = server_res(message, status=400, location=location)
        return response
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        return server_res(str(e), location=location)


def get_all_fav_books(secret_key):
    location = f'/books/favourites'
    try:
        token = request.headers.get('authorization')
        decoded_token = authenticate(token, secret_key)

        user_id = decoded_token['id']
        all_fav_books = Book.get_all_fav_books(user_id)
        a = json.loads(str(all_fav_books))
        for book in a:
            book.update({'favourite': True})

        message = 'your favourite books retrieved successfully'
        return server_res(message, status=200, success=True, location=location, book_data=a)
    except CustomException as e:
        error_obj = e.get_exception_obj() 
        response = server_res(error_obj['message'], status=error_obj['status'])
        return response
    except Exception as e:
        return server_res(str(e), location=location)
