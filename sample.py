from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=True)


@user_api.route("/register")
class Register(Resource):
    @user_api.doc("register_user")
    @user_api.expect(user_model)
    def post(self):
        """Register a new user"""
        user_data = request.json
        # Check if the email already exists in the users_data
        for user in users_data:
            if user["email"] == user_data["email"]:
                return {"message": "Email already exists"}, 400
        # Assign unique ID based on the existing users' length
        user_data["id"] = len(users_data) + 1
        # Hash the password before saving
        user_data["password"] = generate_password_hash(user_data["password"])
        # Append the new user to the users_data list
        users_data.append(user_data)
        # Save the updated users data to file
        save_users_data()
        return user_data, 201
