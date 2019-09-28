import sys

sys.path.append("../")

from models.singer.singer import Singer
from models.song.song import Song
from models.user.user import User
from faker import Faker
import random
import json


class Mock(object):
    _data = None

    def __init__(self):
        self._faker = Faker()
        self.generate_data()

    def save_to_graph(self):
        singer_model = Singer.get_instance()
        user_model = User.get_instance()
        song_model = Song.get_instance()

        for user in self._data["users"]:
            user_model.save_vertex(user["uid"], user["properties"])
        for singer in self._data["singers"]:
            singer_model.save_vertex(singer["singer_id"], singer["properties"])
        for song in self._data["songs"]:
            song_model.save_vertex(song["song_id"], song["properties"])
            song_model.save_edge(song["song_id"], song["singer"], "create_song")

            for uid in song["user_favorite"]:
                song_model.save_edge(song["song_id"], uid, "favorite_song")

    def print_data(self):
        print(json.dumps(self._data))

    def generate_data(self):
        SONG_NUM = SINGER_NUM = 100
        USER_NUM = 5

        user_list = []
        for i in range(USER_NUM):
            user_list.append({
                "uid": "user-{}".format(i),
                "properties": {
                    "name": self._faker.last_name(),
                    "level": random.choice(range(1, 11)),
                    "age": random.choice(range(20, 30)),
                    "sex": random.choice(["male", "female"])
                }
            })

        song_list = []
        for i in range(SONG_NUM):
            song_list.append({
                "song_id": "song-{}".format(i),
                "properties": {
                    "name": self._faker.name()
                },
                "singer": "singer-{}".format(i),
                "user_favorite": [
                    "user-{}".format(random.choice(range(USER_NUM))),
                    "user-{}".format(random.choice(range(USER_NUM)))
                ]
            })

        singer_list = []
        for i in range(SINGER_NUM):
            singer_list.append({
                "singer_id": "singer-{}".format(i),
                "properties": {
                    "name": self._faker.last_name()
                }
            })

        self._data = {
            "users": user_list,
            "singers": singer_list,
            "songs": song_list
        }


if __name__ == "__main__":
    mock = Mock()
    # mock.print_data()
    mock.save_to_graph()
