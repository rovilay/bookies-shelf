from api.helpers.user_helpers import validate_user_names, validate_email_password, get_token, authenticate

def test_valid_user():
  valid_user = {"firstname": "John", "lastname": "Doe", "email": "john.doe@test.com", "password": 1234567}
  valid, errors = validate_user_names(valid_user)
  valid, errors = validate_email_password(valid_user, errors_obj=errors)

  assert valid == True
  assert bool(errors) == False

def test_invalid_user():
  valid_user = {"firstname": "John", "email": "invalidemail.com"}
  valid, errors = validate_user_names(valid_user)
  valid, errors = validate_email_password(valid_user, errors_obj=errors)

  print(errors)

  assert valid == False
  assert errors["names"] == "firstname and lastname are required!"
  assert errors["data"] == "email and password are required!"
  assert errors["email"] == "email is not valid"

def test_get_token():
  secret = "secret"
  payload = {"email": "john.doe@test.com", "password": 1234567}
  token = get_token(secret_key=secret, payload=payload)

  assert bool(token) == True

def test_authenticate(mocker):
  secret = "secret"
  fake_token = "fake_token"
  dummy_user = {"id": 1, "email": "john.doe@test.com"}

  # mock validate_token function
  mock_validate_token = mocker.patch("api.helpers.user_helpers.validate_token")
  mock_validate_token.return_value = dummy_user

  # mock User.check_user_id class
  mock_check_user_id = mocker.patch("api.models.__models.User.check_user_id")
  mock_check_user_id.return_value = dummy_user

  result = authenticate(fake_token, secret_key=secret)

  assert result == dummy_user


