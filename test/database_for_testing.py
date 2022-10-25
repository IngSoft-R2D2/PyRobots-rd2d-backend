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
        db.User(username="angelescch",email="angelescch@gmail.com",
                password=pwd_context.hash("ssssSSS1"),avatar="avatar.img")
        db.User(username="keyword",email="keyword@gmail.com",
                password=pwd_context.hash("htL8s1D498"),avatar="avatar.img")
        db.Robot(user = db.User.get(username="angelescch"), name="R2D2", avatar="image.jpg", behaviour_file="RSD2.py")
        db.Robot(user = db.User.get(username="angelescch"), name="MEGATRON", avatar="image.jpg", behaviour_file="MegaRobot.py")
        db.Robot(user = db.User.get(username="angelescch"), name="Robot3000", avatar="image.jpg", behaviour_file="Robot3000.py")
        db.Robot(user=db.User.get(username="keyword"),name="MEGATRON",avatar="64base_coded_img",behaviour_file="64base_coded_file")
        db.Match(creator=db.User.get(username="angelescch"),
                name="epic",
                max_players=4,
                min_players=2,
                number_of_games=100,
                number_of_rounds=10000,
                password="secret",
                robots = [db.Robot[1]])
        db.Match(creator=db.User.get(username="keyword"),
                name="pool",
                max_players=10,
                min_players=8,
                number_of_games=125,
                number_of_rounds=1010,
                robots = [db.Robot[4]])
        db.Match(creator=db.User.get(username="keyword"),
                name="NGBI",
                max_players=5,
                min_players=3,
                number_of_games=5,
                number_of_rounds=10,
                password="AGSV87NG4",
                robots = [db.Robot[4]])
        db.Match(creator=db.User.get(username="angelescch"),
                name="KGN",
                max_players=5,
                min_players=3,
                number_of_games=5,
                number_of_rounds=10,
                robots = [db.Robot[3]])
    return db

def get_db_override():
    return define_database_for_testing()
