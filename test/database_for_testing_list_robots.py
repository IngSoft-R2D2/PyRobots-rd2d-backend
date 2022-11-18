import sys
sys.path.append('../src/')
from entities import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def define_database_for_testing():
    db = Database(**db_test)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    with db_session:
        db.User(
                    username="mati",email="matimail@gmail.com",
                    password=pwd_context.hash("ssssSSSS1"),avatar="avatar.img",
                    is_confirmed=True
                )
        db.User(
                    username="juan",email="juanmail@gmail.com",
                    password=pwd_context.hash("ssssSSSS1"),avatar="avatar.img",
                    is_confirmed=True
                )
        db.Robot(
                    user = db.User.get(username="mati"), name="optimus",
                    avatar="image1.64base_coded_img", behaviour_file="optimus.py"
                )
        db.Robot(
                    user = db.User.get(username="mati"), name="ratchet",
                    avatar="image2.64base_coded_img", behaviour_file="ratchet.py"
                )
        db.Robot(
                    user = db.User.get(username="juan"), name="megatron",
                    avatar="image3.64base_coded_img", behaviour_file="megatron.py"
                )
        db.Match(
                    creator=db.User.get(username="mati"),
                    name="partida1",
                    max_players=2,
                    min_players=2,
                    number_of_games=123,
                    number_of_rounds=123,
                    robots = [db.Robot[1],db.Robot[2]],
                    users = [db.User.get(username="mati"),db.User.get(username="juan")]
                )
        db.Match(
                    creator=db.User.get(username="juan"),
                    name="partida_de_juan",
                    max_players=2,
                    min_players=2,
                    number_of_games=113,
                    number_of_rounds=13,
                    robots = [db.Robot[2]],
                    users = [db.User.get(username="juan")]
                )
    return db

def get_db_override():
    return define_database_for_testing()
