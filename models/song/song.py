from library.graph import Graph


class Song(object):
    _instances = {}

    @classmethod
    def get_instance(cls, graph_tag='default'):
        if graph_tag not in cls._instances:
            cls._instances[graph_tag] = Song(graph_tag)
        return cls._instances[graph_tag]

    def __init__(self, graph_tag):
        self.g = Graph(graph_tag)

    def save_vertex(self, song_id, properties):
        """
        保存歌曲

        :param song_id: 歌曲 ID
        :param properties: 歌曲属性
        :return: 保存结果
        """
        return self.g.save_vertex("song", str(song_id), properties)

    def save_edge(self, song_id, related_id, related_type, properties):
        """
        保存歌曲关系

        :param song_id: 歌曲 ID
        :param related_id: 相关联的顶点 ID
        :param related_type: 关系类型
        :param properties: 关系属性
        :return: 保存结果
        """
        return self.g.save_edge(related_type, str(related_id), str(song_id), properties)
