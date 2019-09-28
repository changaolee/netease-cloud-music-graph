from library.graph import Graph


class Singer(object):
    _instances = {}

    @classmethod
    def get_instance(cls, graph_tag='default'):
        if graph_tag not in cls._instances:
            cls._instances[graph_tag] = Singer(graph_tag)
        return cls._instances[graph_tag]

    def __init__(self, graph_tag):
        self.g = Graph(graph_tag)

    def save_vertex(self, singer_id, properties):
        """
        保存歌手

        :param singer_id: 歌手 ID
        :param properties: 歌手属性
        :return: 保存结果
        """
        return self.g.save_vertex("singer", str(singer_id), properties)

    def save_edge(self, singer_id, related_id, related_type, properties):
        """
        保存歌手关系

        :param singer_id: 歌手 ID
        :param related_id: 相关联的顶点 ID
        :param related_type: 关系类型
        :param properties: 关系属性
        :return: 保存结果
        """
        return self.g.save_edge(related_type, str(singer_id), str(related_id), properties)
