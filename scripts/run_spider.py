import sys

sys.path.append("../")

from spiders.netease_cloud_music.core import NeteaseCloudMusicRequest
from models.singer.singer import Singer
from models.song.song import Song
from models.user.user import User


class Spider(object):
    CRAWL_PAGE_COUNT = 100  # 默认抓取前 100 条评论
    CRAWL_PAGE_SIZE = 20  # 每页评论的数量

    @classmethod
    def run(cls, song_ids):
        for song_id in song_ids:
            for i in range(cls.CRAWL_PAGE_COUNT):
                offset = i * cls.CRAWL_PAGE_SIZE
                comment_list = NeteaseCloudMusicRequest.music_comment(song_id, offset, cls.CRAWL_PAGE_SIZE)
                for comment in comment_list.get("comments"):
                    user_info = comment.get("user")
                    uid, nickname = user_info.get("userId"), user_info.get("nickname")
                    user_detail = {
                        "uid": uid,
                        "properties": {
                            "name": nickname
                        }
                    }
                    ret = User.get_instance().save_vertex(**user_detail)
                    print("save user:", user_detail, ret)

                    playlist_all = NeteaseCloudMusicRequest.user_playlist(uid, offset, cls.CRAWL_PAGE_SIZE)
                    playlist = playlist_all.get("playlist")[0] if playlist_all.get("playlist") else None
                    if playlist and playlist.get("name") == "{}喜欢的音乐".format(nickname):
                        playlist_id = playlist.get("id")
                        playlist_detail = NeteaseCloudMusicRequest.play_list_detail(playlist_id)

                        song_id_list = []
                        for track_id_info in playlist_detail.get("playlist").get("trackIds"):
                            song_id_list.append(track_id_info["id"])

                        favorite_song_list = NeteaseCloudMusicRequest.song_detail(song_id_list)
                        for favorite_song in favorite_song_list.get("songs"):
                            singer_info = favorite_song.get("ar")[0]  # 只保留第一作者
                            singer_id, singer_name = singer_info.get("id"), singer_info.get("name")
                            singer_detail = {
                                "singer_id": singer_id,
                                "properties": {
                                    "name": singer_name
                                }
                            }
                            ret = Singer.get_instance().save_vertex(**singer_detail)
                            print("save singer:", singer_detail, ret)

                            song_detail = {
                                "song_id": favorite_song.get("id"),
                                "properties": {
                                    "name": favorite_song.get("name")
                                }
                            }
                            ret = Song.get_instance().save_vertex(**song_detail)
                            print("save song:", song_detail, ret)

                            Song.get_instance().save_edge(song_detail["song_id"], uid, "favorite_song", {})
                            print("save {}--favorite_song-->{}".format(uid, song_detail["song_id"]))
                            Song.get_instance().save_edge(song_detail["song_id"], singer_id, "create_song", {})
                            print("save {}--create_song-->{}".format(singer_id, song_detail["song_id"]))


if __name__ == "__main__":
    Spider.run(["1342950406"])
