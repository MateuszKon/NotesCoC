from flask import request, render_template, url_for

from models.users import RegisterUserModel, UserModel
from schemas.users import UserSchema, RegisterUserSchema

INVALID_REGISTRATION_HASH = "Invalid registration hash!"
INVALID_CREDENTIALS = "Invalid username or password!"
USERNAME_EXIST_ERROR = "Username with name {} already exist!"

register_user_schema = RegisterUserSchema()
user_schema = UserSchema()


class UserRegister:

    @classmethod
    def register_user(cls, registration_hash: str):
        register_user = RegisterUserModel.get_by_hash(registration_hash)
        if register_user is None:
            return {"message": INVALID_REGISTRATION_HASH}, 404
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["new-password"]
            if UserModel.get_by_login(username):
                return {"message": USERNAME_EXIST_ERROR.format(username)}, 400
            new_user = UserModel(username, password, register_user.person_name)
            new_user.save_to_db()
            register_user.delete_from_db()
            return {"message": "Registration complete!"}, 201
        return render_template(
            'register.html',
            person_name=register_user.person_name,
            register_hash=registration_hash,
        )

    @classmethod
    def add_registration_record(cls):
        print(request.json)
        user_register: RegisterUserModel = register_user_schema.load(request.json)
        user_register.save_to_db()
        print(user_register)
        return register_user_schema.dump(user_register), 201

    @classmethod
    def get_registration_records(cls):
        return {"registers": register_user_schema.dump(
            RegisterUserModel.get_all(),
            many=True
        )}, 200


class UserLogin:

    @classmethod
    def login_user(cls):
        if request.method == "POST":
            username = request.form['username']
            password = request.form['current-password']
            user_obj = UserModel.get_by_login(username)
            if user_obj and password and user_obj.check_password(password):
                return {"mesage": "Logged in."}
            return {"message": INVALID_CREDENTIALS}, 404
        return render_template(
            'login.html',
            next=request.args.get('next', None),
        )


class User:

    @classmethod
    def get_all(cls):
        return {'users': user_schema.dump(
            UserModel.get_all(),
            many=True
        )}
