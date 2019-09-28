from library.graph import Graph
import json


class Utils(object):
    _instances = {}

    @classmethod
    def get_instance(cls, graph_tag='default'):
        if graph_tag not in cls._instances:
            cls._instances[graph_tag] = Utils(graph_tag)
        return cls._instances[graph_tag]

    def __init__(self, graph_tag):
        self.g = Graph(graph_tag)

    @staticmethod
    def format_graph_fields(graph_data):
        format_data = {}
        for k, v in graph_data.items():
            format_data[str(k)] = v[0] if type(v) == list else v

        format_data['id'] = format_data['T.id']
        format_data['label'] = format_data['T.label']

        del format_data['T.id']
        del format_data['T.label']

        return format_data

    def graph_visualization(self, size=100):
        """
        将图数据库中的数据可视化

        :param size: 起始点的数量（歌曲）
        :return:
        """
        dsl = """
            g.V().hasLabel('song').limit(size).as('SONGS').
                project('song', 'user', 'singer').
                    by(select('SONGS').valueMap(true)).
                    by(select('SONGS').in('favorite_song').valueMap(true).fold()).
                    by(select('SONGS').in('create_song').valueMap(true).fold())
        """
        bindings = {"size": size}
        callback = self.g.query_dsl(dsl, bindings)

        relation = {"vertex": [], "edge": []}

        for ret in callback.result():
            for data in ret:
                song = self.format_graph_fields(data["song"])
                relation["vertex"].append(song)

                user_list = []
                for user in data["user"]:
                    user = self.format_graph_fields(user)
                    user_list.append(user)
                    relation["edge"].append({
                        "from": user["id"],
                        "to": song["id"],
                        "type": "favorite_song"
                    })
                relation["vertex"].extend(user_list)

                singer_list = []
                for singer in data["singer"]:
                    singer = self.format_graph_fields(singer)
                    singer_list.append(singer)
                    relation["edge"].append({
                        "from": singer["id"],
                        "to": song["id"],
                        "type": "create_song"
                    })
                relation["vertex"].extend(singer_list)

        result = {
            "type": "force",
            "categories": [
                {
                    "name": "用户"
                },
                {
                    "name": "歌曲"
                },
                {
                    "name": "歌手"
                }
            ],
            "nodes": [],
            "links": []
        }
        category_index = {
            "user": 0, "song": 1, "singer": 2
        }

        vertex_index = {}

        for i, vertex in enumerate(relation["vertex"]):
            result["nodes"].append({
                "name": vertex["name"],
                "value": 1,
                "category": category_index[vertex["label"]]
            })
            vertex_index[vertex["id"]] = i

        for edge in relation["edge"]:
            result["links"].append({
                "source": vertex_index[edge["from"]],
                "target": vertex_index[edge["to"]]
            })

        return json.dumps(result)
