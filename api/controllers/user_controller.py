from flask import request
from ..helpers.user_helpers import validate_user_names, validate_email_password, get_token
from ..helpers.__helpers import server_res, CustomException
from ..helpers.user_helpers import authenticate
from ..models.__models import User as UserModel

def signup_user(secret_key):
    location = '/register'
    try:
        print('hello')
        user_data = request.get_json()
        if isinstance(user_data, dict):
            valid, init_errors = validate_user_names(user_data)
            valid, errors = validate_email_password(user_data, errors_obj=init_errors)

            if valid == False:
                message = str(errors)
                raise CustomException(message, status=400)
            else:
                firstname = user_data['firstname']
                lastname = user_data['lastname']
                email = user_data['email']
                password = user_data['password']

                new_user = UserModel().add_user(firstname, lastname, email, password)
                if isinstance(new_user, Exception) and str(new_user) == 'Email already exist':
                    message = 'Email already exist'
                    raise CustomException(message, status=409)
                elif isinstance(new_user, Exception):
                    raise Exception(str(new_user))
                else:
                    token = get_token(secret_key, new_user)
                    response = server_res('Signup successful!', success=True,
                                          status=201, location='/register', token=str(token), id=new_user['id'], email=new_user['email'])
                    return response

        else:
            message = 'User data not in correct format'
            raise CustomException(message, status=400)
    except CustomException as e:
        print(e)
        response = server_res(e.message, status=e.status, location='/login')
        return response
    except Exception as e:
        print(e)
        response = server_res(str(e), location=location)
        return response


def login_user(secret_key):
    try:
        user_data = request.get_json()
        if isinstance(user_data, dict) and ('email' and 'password' in user_data):
            email = user_data['email']
            password = user_data['password']
            
            confirmed_user = UserModel().check_user_password(email, password)

            if isinstance(confirmed_user, dict) and ('email' in confirmed_user):
                token = get_token(secret_key, confirmed_user)
                response = server_res('Login successful!', success=True, status=200, location='/login', token=str(token), id=confirmed_user['id'], email=confirmed_user['email'])
                return response
            else:
                message = 'Invalid Email or Password!'
                raise CustomException(message, status=400)
        else:
            raise CustomException(
                'User credentials must contain email and password', status=400)
    except CustomException as e:
        response = server_res(e.message, status=e.status, location='/login')
        return response
    except Exception as e:
        response = server_res(str(e), location='/login')
        return response

def get_user(secret_key):
    try:
        token = request.headers.get('authorization')
        confirmed_user = authenticate(token, secret_key)

        response = server_res('user retrieved successfully!', success=True, status=200, location='/me', user=confirmed_user)
        return response
    except CustomException as e:
        response = server_res(e.message, status=e.status, location='/me')
        return response
    except Exception as e:
        response = server_res(str(e), location='/me')
        return response
