from units import UserNode
from sql_user import UserGraphApp

def main():
    app = UserGraphApp()

    # Creating or logging in users
    user1 = UserNode(id=1, full_name="Alice Johnson", school="ABC University", graduation_year=2023, major="Computer Science", age=22, location="New York")
    user2 = UserNode(id=2, full_name="Bob Smith", school="ABC University", graduation_year=2022, major="Mathematics", age=23, location="New York")
    user3 = UserNode(id=3, full_name="Charlie Brown", school="XYZ University", graduation_year=2023, major="Physics", age=22, location="San Francisco")

    # Add users to the database and graph
    app.create_or_login_user(user1)
    app.add_user_to_graph(user1)

    app.create_or_login_user(user2)
    app.add_user_to_graph(user2)

    app.create_or_login_user(user3)
    app.add_user_to_graph(user3)

    # Get similar users for user1 (connected components)
    similar_users_to_user1 = app.get_user_graph(1)
    print(f"Connected users to {user1.full_name}: {similar_users_to_user1}")

if __name__ == "__main__":
    main()
