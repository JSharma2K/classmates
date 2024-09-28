from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import networkx as nx
from units import UserNode
from find_friends import ScoreCard

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    school = Column(String, nullable=False)
    graduation_year = Column(Integer, nullable=True)
    major = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class UserGraph:
    def __init__(self):
        self.graphs = {}  # Dictionary to store user's individual graphs

    def create_or_append_graph(self, user_id: int, connected_user_id: int):
        if user_id not in self.graphs:
            self.graphs[user_id] = nx.Graph()  # Create new graph for the user

        # Add the connected user to the graph
        self.graphs[user_id].add_edge(user_id, connected_user_id)

    def get_connected_component(self, user_id: int):
        if user_id not in self.graphs:
            return []  # No graph for this user
        # Find all connected components in the user's graph
        return list(nx.connected_components(self.graphs[user_id]))

    def get_graph(self, user_id: int):
        return self.graphs.get(user_id, None)


class UserGraphApp:
    def __init__(self):
        self.db = SessionLocal()
        self.user_graph = UserGraph()  # For storing user-specific graphs
        self.scorecard = ScoreCard()  # For calculating similarity

    # Function to create a new user or log in an existing user
    def create_or_login_user(self, user_data: UserNode):
        # Check if the user already exists in the database
        existing_user = self.db.query(User).filter(User.id == user_data.id).first()
        if existing_user:
            print(f"User {user_data.full_name} already exists. Logging in...")
            return existing_user
        else:
            # Create a new user entry in the database
            new_user = User(
                id=user_data.id,
                full_name=user_data.full_name,
                school=user_data.school,
                graduation_year=user_data.graduation_year,
                major=user_data.major,
                age=user_data.age,
                location=user_data.location
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            print(f"User {user_data.full_name} created successfully.")
            return new_user

    # Function to add user to the graph and update cache
    def add_user_to_graph(self, user_data: UserNode):
        # Compare with all other users in the database
        all_users = self.db.query(User).all()

        for other_user in all_users:
            if other_user.id != user_data.id:
                # Convert SQLAlchemy User to Pydantic UserNode
                other_user_node = UserNode(
                    id=other_user.id,
                    full_name=other_user.full_name,
                    school=other_user.school,
                    graduation_year=other_user.graduation_year,
                    major=other_user.major,
                    age=other_user.age,
                    location=other_user.location
                )

                # Calculate similarity
                similarity_score = ScoreCard(user_data,other_user_node).get_score()

                # If similarity score is greater than 0.7, connect users
                if similarity_score > 0.7:
                    print(f"Connecting {user_data.full_name} with {other_user.full_name}")

                    # Append this connection to both users' cached graphs
                    self.user_graph.create_or_append_graph(user_data.id, other_user.id)
                    self.user_graph.create_or_append_graph(other_user.id, user_data.id)

    # Function to get the graph for a specific user
    def get_user_graph(self, user_id: int):
        user_graph = self.user_graph.get_graph(user_id)
        if user_graph:
            # Return the connected components of this user's graph
            return self.user_graph.get_connected_component(user_id)
        else:
            print(f"No graph found for user {user_id}")
            return []
