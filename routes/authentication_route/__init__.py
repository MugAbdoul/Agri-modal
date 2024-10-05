from flask import Blueprint
from flask_restful import Api

authBlueprint = Blueprint("Auth", __name__, url_prefix="/api/v1/auth")
authApi = Api(authBlueprint)


# Import and register resources
from .Signup import SignupResource
from .ValidateCode import ValidateCodeResource
from .ValidateCode import ResendCodeResource
from .Login import LoginResource
from .passwordResetRequest import PasswordResetResource, VerifyPasswordResetResource

# Add login and signup resources
authApi.add_resource(SignupResource, "/signup")
authApi.add_resource(ValidateCodeResource, "/validate-code")
authApi.add_resource(ResendCodeResource, "/resend-code")
authApi.add_resource(LoginResource, "/login")
authApi.add_resource(PasswordResetResource, '/password-reset')
authApi.add_resource(VerifyPasswordResetResource, '/password-reset/verify')