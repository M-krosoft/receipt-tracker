from flask import request, jsonify, Blueprint

from app.exceptions import InvalidRequestFieldError, EmailTakenError, InvalidPasswordError, UserNotExistError
from app.reponses import ApiErrorResponse
from app.requests import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    @staticmethod
    def is_valid_field(field):
        return field is not None and field.strip() != ""

    @staticmethod
    def _verify_and_prepare_register_request() -> RegisterRequest:
        request_data = request.get_json()
        if request_data is None:
            raise InvalidRequestFieldError

        name = request_data.get('name')
        email = request_data.get('email')
        password = request_data.get('password')

        if not AuthController.is_valid_field(name) or not AuthController.is_valid_field(email) or not AuthController.is_valid_field(password):
            raise InvalidRequestFieldError

        return RegisterRequest(
            name=name,
            email=email,
            password=password)

    def _register(self):
        _request = None
        try:
            _request = self._verify_and_prepare_register_request()
            self.auth_service.register_user(register_request=_request)

            return 200
        except (InvalidRequestFieldError, EmailTakenError) as error:
            return jsonify(ApiErrorResponse(error).to_dict()), 400

    def _login(self):
        try:
            request_data = request.get_json()
            if request_data is None:
                raise InvalidRequestFieldError

            email = request_data.get('email')
            password = request_data.get('password')
            login_request = LoginRequest(email=email, password=password)
            access_token = self.auth_service.authenticate(login_request=login_request)

            return jsonify({"access_token": access_token}), 200
        except (UserNotExistError, InvalidPasswordError, InvalidRequestFieldError) as error:
            return jsonify(ApiErrorResponse(error).to_dict()), 400

    def create_blueprint(self) -> Blueprint:
        auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

        @auth_bp.route("/register", methods=["POST"])
        def register():
            return self._register()

        @auth_bp.route("/login", methods=["POST"])
        def login():
            return self._login()

        return auth_bp
