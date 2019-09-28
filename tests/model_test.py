import sys

sys.path.append("../")

from models.user.user import User
from models.utils.utils import Utils

if __name__ == "__main__":
    # ret = User.get_instance().find_similar_user('user-1')
    # print(ret)

    ret = Utils.get_instance().graph_visualization()
    print(ret)