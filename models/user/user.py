from library.graph import Graph
from models.utils.utils import Utils


class User(object):
    _instances = {}

    @classmethod
    def get_instance(cls, graph_tag='default'):
        if graph_tag not in cls._instances:
            cls._instances[graph_tag] = User(graph_tag)
        return cls._instances[graph_tag]

    def __init__(self, graph_tag):
        self.g = Graph(graph_tag)

    def find_similar_user(self, uid, top_n=3):
        """
        找到与当前用户兴趣相近的用户

        :param uid: 用户 ID
        :return: 兴趣相近的用户信息
        """
        dsl = """
            g.V(uid).as('v1').
                out('favorite_song').in('favorite_song').dedup().where(neq('v1')).as('v2').
                project('v1', 'v2', 'v1n', 'v2n').
                    by(select('v1')).
                    by(select('v2')).
                    by(select('v1').out('favorite_song').fold()).
                    by(select('v2').out('favorite_song').fold()).
                as('q1').
                project('v1', 'v2', 'i', 'u').
                    by(select('v1')).
                    by(select('v2')).
                    by(select('v1n').as('n').
                       select('q1').select('v2n').unfold().
                          where(within('n')).
                          count()).
                    by(union(select('v1n').
                             select('q1').select('v2n')).unfold().
                       dedup().count()).
                project('v1', 'v2', 'jaccard').
                    by(select('v1').valueMap(true)).
                    by(select('v2').valueMap(true)).
                    by(math('i/u')).order().by(select('jaccard'), desc).
                limit(top_n)
        """
        bindings = {"uid": uid, "top_n": top_n}
        callback = self.g.query_dsl(dsl, bindings)

        result = []

        for ret in callback.result():
            for data in ret:
                v2_vertex = Utils.format_graph_fields(data["v2"])
                result.append({
                    "uid": v2_vertex["id"],
                    "name": v2_vertex["name"],
                    "jaccard_score": round(data["jaccard"], 5)
                })
        return result


    def save_vertex(self, uid, properties):
        """
        保存用户

        :param uid: 用户 ID
        :param properties: 用户属性
        :return: 保存结果
        """
        return self.g.save_vertex("user", str(uid), properties)

    def save_edge(self, uid, related_id, related_type, properties):
        """
        保存用户关系

        :param uid: 用户 ID
        :param related_id: 相关联的顶点 ID
        :param related_type: 关系类型
        :param properties: 关系属性
        :return: 保存结果
        """
        return self.g.save_edge(related_type, str(uid), str(related_id), properties)
