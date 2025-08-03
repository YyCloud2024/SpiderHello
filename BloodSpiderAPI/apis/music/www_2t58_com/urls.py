
from django.urls import path
from BloodSpiderAPI.apis.music.www_2t58_com import request
urlpatterns = [
    # 搜索音乐
    path("search/", request.search_music),
    # 获取音乐数据
    path("music/data/", request.get_music_data),
    # 获取热门歌单分类
    path("hot/list/classification/", request.get_hot_list_classification),
    # 根据热门歌单分类id获取歌曲
    path("hot/list/", request.get_music_by_hot_list_id),
    # 获取歌手的音乐
    path("singer/", request.get_music_by_singer_id),
    # 获取歌手的专辑
    path("singer/album/", request.get_singer_album),
]
