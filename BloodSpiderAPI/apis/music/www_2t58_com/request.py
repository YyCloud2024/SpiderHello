from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.music.www_2t58_com.main import BloodSpiderMusic2T58

music_data = BloodSpiderMusic2T58()

# 搜索音乐
def search_music(request):
    # 校验请求方法
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")

    # 获取并校验音乐名称
    music_name = request.POST.get("music_name")
    if not music_name:
        return response_dict(code=400, message="缺少必要参数：music_name")
    if not isinstance(music_name, str):
        return response_dict(code=400, message="参数类型错误：music_name必须为字符串")
    if len(music_name) > 100:
        return response_dict(code=400, message="参数长度超限：music_name最大长度为100")

    # 执行搜索
    try:
        index_data = music_data.search_music(music_name)
    except Exception as e:
        return response_dict(code=500, message=f"搜索过程出错：{str(e)}")

    # 检查搜索结果
    if not index_data:
        return response_dict(code=404, message="未找到匹配的音乐")

    return response_dict(message="搜索成功", data=index_data)

# 获取音乐数据
def get_music_data(request):
    # 校验请求方法
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")

    # 获取并校验音乐ID
    music_id = request.POST.get("music_id")
    if not music_id:
        return response_dict(code=400, message="缺少必要参数：music_id")

    # music_id长度不可以超出32位
    if len(music_id) > 32:
        return response_dict(code=400, message="参数错误：music_id长度不可以超出32位")

    # 执行获取操作
    try:
        index_data = music_data.get_music_data(music_id)
        # index_data = {
        #     "name": "陈奕迅《十面埋伏》[Mp3_Lrc]",
        #     "music_url": "https://er-sycdn.kuwo.cn/147697ea3d5b85e9cd71d5b1ad7d50f1/68969def/resource/30106/trackmedia/C200000lVKbP3bCwxu.m4a?from=vip",
        #     "music_cover": "https://img1.kuwo.cn/star/albumcover/300/s4s15/9/1486376130.jpg",
        #     "artistName": "陈奕迅",
        #     "artistId": "eG4",
        #     "artist_music_count": "2772",
        #     "albumName": "Live For Today",
        #     "albumId": "bWg"
        # }
    except Exception as e:
        return response_dict(code=500, message=f"获取音乐数据出错：{str(e)}")

    # 检查结果
    if not index_data:
        return response_dict(code=404, message="未找到指定音乐")

    return response_dict(message="获取成功", data=index_data)

# 获取热门榜单分类
def get_hot_list_classification(request):
    index_data = music_data.get_hot_list_classification()
    return response_dict(message="获取成功", data=index_data)

# 根据热门榜单分类id获取歌曲
def get_music_by_hot_list_id(request):
    # 校验请求方法
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")

    # 获取并校验热门榜单分类id
    hot_list_id = request.POST.get("hot_list_id")
    if not hot_list_id:
        return response_dict(code=400, message="缺少必要参数：hot_list_id")
    if not isinstance(hot_list_id, str):
        return response_dict(code=400, message="参数类型错误：hot_list_id必须为字符串")
    if len(hot_list_id) > 32:
        return response_dict(code=400, message="参数长度超限：hot_list_id最大长度为32")

    # 执行获取操作
    try:
        index_data = music_data.get_music_by_hot_list_id(hot_list_id)

    except Exception as e:
        return response_dict(code=500, message=f"获取歌曲数据出错：{str(e)}")

    # 检查结果
    if not index_data:
        return response_dict(code=404, message="未找到指定热门榜单分类下的歌曲")

    return response_dict(message="获取成功", data=index_data)

# 获取歌手的音乐
def get_music_by_singer_id(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    singer_id = request.POST.get("singer_id")
    if not singer_id:
        return response_dict(code=400, message="缺少必要参数：singer_id")
    if not isinstance(singer_id, str):
        return response_dict(code=400, message="参数类型错误：singer_id必须为字符串")
    if len(singer_id) > 32:
        return response_dict(code=400, message="参数长度超限：singer_id最大长度为32")
    try:
        index_data = music_data.get_music_by_singer_id(singer_id)
    except Exception as e:
        return response_dict(code=500, message=f"获取歌手音乐数据出错：{str(e)}")
    return response_dict(message="获取成功", data=index_data)

# 获取歌手的专辑
def get_singer_album(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    album_id = request.POST.get("album_id")
    if not album_id:
        return response_dict(code=400, message="缺少必要参数：album_id")
    if not isinstance(album_id, str):
        return response_dict(code=400, message="参数类型错误：album_id必须为字符串")
    if len(album_id) > 32:
        return response_dict(code=400, message="参数长度超限：album_id最大长度为32")
    index_data = music_data.get_singer_album(album_id)
    return response_dict(message="获取成功", data=index_data)
