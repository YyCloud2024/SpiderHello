import requests
from lxml import etree
from BloodSpiderModel.spiderMusic.PublicConfiguration import MusicPublicConfiguration
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.BloodSpiderPrint.blood_spider_print_logger import BloodSpiderPrintLogger

class BloodSpiderMusic2T58:
    def __init__(self):
        self.base_url = "https://www.2t58.com"
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': self.base_url,
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        self.cookies = {}
        
        self.blood_spider_print_logger = BloodSpiderPrintLogger(is_show=False)
        self.blood_spider_print_logger.blood_spider_print_info("初始化 BloodSpiderMusic2T58 类")
        
        self.music_config = MusicPublicConfiguration()
        self.common_utils = GeneralToolkit()
        
        self.blood_spider_print_logger.blood_spider_print_info(f"基础 URL 设置为: {self.base_url}")
        self.blood_spider_print_logger.blood_spider_print_info("初始化完成")

    def _get_song_ranking(self, lis):
        """
        获取歌曲飙升榜的名称、跳转链接、如果有 mv 还需要单独用一个字典包裹住，里面是有两个字段，第一个是是否有 mv，第二个是 mv 的跳转链接
        :param lis: 包含歌曲飙升榜信息的 etree 字符串
        :return: 包含歌曲飙升榜信息的列表，每个元素是一个字典，包含 'name', 'music_id',二个字段
        """
        self.blood_spider_print_logger.blood_spider_print_info("开始解析歌曲飙升榜信息")
        self.blood_spider_print_logger.blood_spider_print_debug(f"输入参数 lis 类型: {type(lis)}")
        
        tree = lis
        songs = []
        
        self.blood_spider_print_logger.blood_spider_print_debug("查找所有歌曲项目")
        song_items = tree.xpath('./li')
        self.blood_spider_print_logger.blood_spider_print_debug(f"找到 {len(song_items)} 个歌曲项目")
        
        for index, item in enumerate(song_items):
            self.blood_spider_print_logger.blood_spider_print_debug(f"处理第 {index+1}/{len(song_items)} 个歌曲项目")
            
            name = item.xpath('.//div[@class="name"]/a/text()')
            link = item.xpath('.//div[@class="name"]/a/@href')
            
            self.blood_spider_print_logger.blood_spider_print_debug(f"解析结果 - name: {name}, link: {link}")
            
            if name and link:
                self.blood_spider_print_logger.blood_spider_print_debug("找到有效歌曲信息，构建歌曲配置")
                music_config = self.music_config.get_music_name_and_music_id()
                music_config["name"] = name[0]
                
                music_id = str(link[0]).split("/")[-1].split(".")[0]
                music_config["music_id"] = music_id
                
                songs.append(music_config)
                self.blood_spider_print_logger.blood_spider_print_debug(f"添加歌曲: {name[0]} (ID: {music_id})")
        
        self.blood_spider_print_logger.blood_spider_print_info(f"歌曲飙升榜信息解析完成，共解析出 {len(songs)} 首歌曲")
        return songs

    # 下载html并且提供解析成etree服务
    def _get_html_tree(self, url, is_tree=True):
        self.blood_spider_print_logger.blood_spider_print_info(f"开始请求 URL: {url}")
        self.blood_spider_print_logger.blood_spider_print_debug(f"请求参数 - is_tree: {is_tree}")
        
        ua = self.common_utils.get_ua()
        self.headers["User-Agent"] = ua
        self.blood_spider_print_logger.blood_spider_print_debug(f"设置 User-Agent 为: {ua}")
        
        try:
            self.blood_spider_print_logger.blood_spider_print_debug("发送 HTTP GET 请求")
            response = requests.get(url, headers=self.headers, cookies=self.cookies).text
            self.blood_spider_print_logger.blood_spider_print_info(f"成功获取 URL: {url} 的响应")
            self.blood_spider_print_logger.blood_spider_print_debug(f"响应内容长度: {len(response)}")
            
            if is_tree:
                self.blood_spider_print_logger.blood_spider_print_debug("开始解析 HTML 为 etree 对象")
                tree = etree.HTML(response)
                self.blood_spider_print_logger.blood_spider_print_debug("HTML 解析完成")
                return tree
                
            return response
            
        except Exception as e:
            self.blood_spider_print_logger.blood_spider_print_error(f"请求 URL: {url} 时出现错误: {e}")
            self.blood_spider_print_logger.blood_spider_print_debug(f"错误类型: {type(e).__name__}")
            return None

    # 获取热门榜单分类
    def get_hot_list_classification(self):
        self.blood_spider_print_logger.blood_spider_print_info("开始获取热门榜单分类")
        
        request_url = self.base_url + "/list/top.html"
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建请求 URL: {request_url}")
        
        tree = self._get_html_tree(request_url)
        
        if tree is None:
            self.blood_spider_print_logger.blood_spider_print_error("获取热门榜单分类时，HTML 解析失败")
            return []
            
        self.blood_spider_print_logger.blood_spider_print_debug("查找所有热门榜单分类项目")
        lis = tree.xpath('//div[@class="ilingku_fl"]/li')
        self.blood_spider_print_logger.blood_spider_print_debug(f"找到 {len(lis)} 个热门榜单分类项目")
        
        hot_list = []
        for index, li in enumerate(lis):
            self.blood_spider_print_logger.blood_spider_print_debug(f"处理第 {index+1}/{len(lis)} 个热门榜单分类项目")
            
            music_config = self.music_config.get_music_name_and_music_id()
            
            name = li.xpath('.//a/text()')
            hot_id = str(li.xpath('.//a/@href')).split("/")[-1].split(".")[0]
            
            self.blood_spider_print_logger.blood_spider_print_debug(f"解析结果 - name: {name}, hot_id: {hot_id}")
            
            music_config["name"] = name[0]
            music_config["music_id"] = hot_id
            
            hot_list.append(music_config)
            self.blood_spider_print_logger.blood_spider_print_debug(f"添加热门榜单分类: {name[0]} (ID: {hot_id})")
        
        self.blood_spider_print_logger.blood_spider_print_info(f"热门榜单分类获取完成，共获取 {len(hot_list)} 个分类")
        return hot_list

    # 根据热门榜单分类id获取歌曲
    def get_music_by_hot_list_id(self, hot_list_id):
        self.blood_spider_print_logger.blood_spider_print_info(f"开始根据热门榜单分类 ID {hot_list_id} 获取歌曲")
        
        request_url = self.base_url + f"/list/{hot_list_id}.html"
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建请求 URL: {request_url}")
        
        tree = self._get_html_tree(request_url)
        
        if tree is None:
            self.blood_spider_print_logger.blood_spider_print_error(f"根据热门榜单分类 ID {hot_list_id} 获取歌曲时，HTML 解析失败")
            return []
            
        self.blood_spider_print_logger.blood_spider_print_debug("查找歌曲列表元素")
        song_list_element = tree.xpath('//div[@class="play_list"]/ul')
        
        if not song_list_element:
            self.blood_spider_print_logger.blood_spider_print_warning(f"未找到歌曲列表元素，可能页面结构变化")
            return []
            
        self.blood_spider_print_logger.blood_spider_print_debug("开始解析歌曲信息")
        songs = self._get_song_ranking(song_list_element[0])
        
        self.blood_spider_print_logger.blood_spider_print_info(f"根据热门榜单分类 ID {hot_list_id} 获取歌曲完成，共获取 {len(songs)} 首歌曲")
        return songs

    # 获取歌手的音乐
    def get_music_by_singer_id(self, singer_id):
        self.blood_spider_print_logger.blood_spider_print_info(f"开始根据歌手 ID {singer_id} 获取音乐")
        
        request_url = self.base_url + f"/singer/{singer_id}/1.html"
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建请求 URL: {request_url}")
        
        tree = self._get_html_tree(request_url)
        
        if tree is None:
            self.blood_spider_print_logger.blood_spider_print_error(f"根据歌手 ID {singer_id} 获取音乐时，HTML 解析失败")
            return {}
            
        self.blood_spider_print_logger.blood_spider_print_debug("查找歌曲列表元素")
        song_list_element = tree.xpath('//*[@class="play_list"]/ul')
        
        if not song_list_element:
            self.blood_spider_print_logger.blood_spider_print_warning(f"未找到歌曲列表元素，可能页面结构变化")
            return {}
            
        self.blood_spider_print_logger.blood_spider_print_debug("开始解析歌曲信息")
        music_list = self._get_song_ranking(song_list_element[0])
        
        self.blood_spider_print_logger.blood_spider_print_debug("获取艺人信息")
        # 艺人介绍
        artist_name_elements = tree.xpath('//div[@class="singer_info"]/div[@class="list_r"]/h1/text()')
        artistName = artist_name_elements[0] if artist_name_elements else "未知艺人"
        
        # artistDesc
        artist_desc_elements = tree.xpath('//div[@class="singer_info"]/div[@class="list_r"]/div[@class="info"]/p/text()')
        artistDesc = artist_desc_elements[0] if artist_desc_elements else "无介绍"
        
        self.blood_spider_print_logger.blood_spider_print_debug(f"艺人名称: {artistName}")
        
        music_config = self.music_config.get_singer_name_and_singer_introduction_and_singer_music_list()
        music_config["artistName"] = artistName
        music_config["artistDesc"] = artistDesc
        music_config["singer_music_list"] = music_list
        
        self.blood_spider_print_logger.blood_spider_print_info(f"根据歌手 ID {singer_id} 获取音乐完成，共获取 {len(music_list)} 首歌曲")
        return music_config

    # 获取音乐数据
    def get_music_data(self, music_id):
        self.blood_spider_print_logger.blood_spider_print_info(f"开始获取音乐 ID {music_id} 的数据")
        
        data = {
            'id': music_id,
            'type': 'music',
        }
        
        self.blood_spider_print_logger.blood_spider_print_debug(f"准备 POST 请求数据: {data}")
        
        try:
            self.blood_spider_print_logger.blood_spider_print_debug("发送 HTTP POST 请求")
            response = requests.post(f'{self.base_url}/js/play.php', data=data, headers=self.headers).json()
            
            self.blood_spider_print_logger.blood_spider_print_info(f"成功获取音乐 ID {music_id} 的基本数据")
            self.blood_spider_print_logger.blood_spider_print_debug(f"响应数据: {response}")
            
            music_config = self.music_config.get_music_name_and_music_url_and_music_cover()
            music_config["name"] = response["title"]
            music_config["music_url"] = response["url"]
            music_config["music_cover"] = response['pic']
            
            self.blood_spider_print_logger.blood_spider_print_debug(f"音乐名称: {response['title']}")
            
            # 获取音乐播放页数据
            self.blood_spider_print_logger.blood_spider_print_info(f"开始获取音乐 ID {music_id} 的播放页数据")
            music_config.update(self.get_music_page_data(music_id))
            
            self.blood_spider_print_logger.blood_spider_print_info(f"成功获取音乐 ID {music_id} 的完整数据")
            return music_config
            
        except Exception as e:
            self.blood_spider_print_logger.blood_spider_print_error(f"获取音乐 ID {music_id} 的数据时出现错误: {e}")
            self.blood_spider_print_logger.blood_spider_print_debug(f"错误类型: {type(e).__name__}")
            return {}

    # 搜索音乐
    def search_music(self, music_name: str):
        self.blood_spider_print_logger.blood_spider_print_info(f"开始搜索音乐: {music_name}")
        
        search_url = self.base_url + f"/so/{music_name}/1.html"
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建搜索 URL: {search_url}")
        
        response = requests.get(search_url).text
        self.blood_spider_print_logger.blood_spider_print_info(f"搜索请求成功，开始解析结果")
        
        tree = etree.HTML(response)
        
        self.blood_spider_print_logger.blood_spider_print_debug("查找歌曲列表元素")
        song_list_element = tree.xpath('//div[@class="play_list"]/ul')
        
        if not song_list_element:
            self.blood_spider_print_logger.blood_spider_print_warning(f"未找到歌曲列表元素，可能没有搜索结果")
            return []
            
        music_list = self._get_song_ranking(song_list_element[0])
        
        self.blood_spider_print_logger.blood_spider_print_info(f"音乐搜索完成，共找到 {len(music_list)} 条结果")
        return music_list

    # 获取音乐播放页的 数据
    def get_music_page_data(self, music_id):
        response_url = self.base_url + f"/song/{music_id}.html"
        self.blood_spider_print_logger.blood_spider_print_info(f"开始获取音乐 ID {music_id} 播放页的数据")
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建请求 URL: {response_url}")
        
        tree = self._get_html_tree(response_url)
        
        if tree is None:
            self.blood_spider_print_logger.blood_spider_print_error(f"获取音乐 ID {music_id} 播放页的数据时，HTML 解析失败")
            return {'name': '服务器负载过高⚠️',
                    'music_cover': 'https://img1.kuwo.cn/star/albumcover/300/4/59/69715678.jpg',
                    'artistName': 'BloodSpider', 'artistId': 'BloodSpider', 'artist_music_count': '1',
                    'albumName': 'Spider Not Get Data', 'albumId': 'BloodSpider'}
                    
        self.blood_spider_print_logger.blood_spider_print_debug("检查播放页结构是否存在")
        if len(tree.xpath('//*[@class="play_singer"]')) == 0:
            self.blood_spider_print_logger.blood_spider_print_warning(f"音乐 ID {music_id} 播放页数据获取失败，返回默认数据")
            return {'name': '服务器负载过高⚠️',
                    'music_cover': 'https://img1.kuwo.cn/star/albumcover/300/4/59/69715678.jpg',
                    'artistName': 'BloodSpider', 'artistId': 'BloodSpider', 'artist_music_count': '1',
                    'albumName': 'Spider Not Get Data', 'albumId': 'BloodSpider'}
        
        self.blood_spider_print_logger.blood_spider_print_debug("开始解析播放页数据")
        
        # 歌手名称
        artist_name_elements = tree.xpath('//*[@class="play_singer"]//div[@class="name"]/a/text()')
        artistName = artist_name_elements[0] if artist_name_elements else "未知歌手"
        
        # 歌手id
        artist_id_elements = tree.xpath('//*[@class="play_singer"]/div[@class="center"]/div[@class="name"]/a/@href')
        artistId = str(artist_id_elements[0]).split("/")[-1].split(".")[0] if artist_id_elements else "unknown"
        
        # 一共多少音乐
        music_count_elements = tree.xpath('//*[@class="play_singer"]/div[@class="center"]/div[@class="info"]/span/text()')
        music_count = music_count_elements[0] if music_count_elements else "0"
        
        # 所属专辑
        album_name_elements = tree.xpath('//*[@class="player_right"]/div[@class="sm"]/a/text()')
        albumName = album_name_elements[0] if album_name_elements else "未知专辑"
        
        # 所属专辑ID
        album_id_elements = tree.xpath('//*[@class="player_right"]/div[@class="sm"]/a/@href')
        albumId = str(album_id_elements[0]).split("/")[-1].split(".")[0] if album_id_elements else "unknown"
        
        self.blood_spider_print_logger.blood_spider_print_debug(f"解析结果 - 歌手: {artistName}, 专辑: {albumName}")
        
        music_config = self.music_config.get_music_play_page_data()
        music_config["artistName"] = artistName
        music_config["artistId"] = artistId
        music_config["artist_music_count"] = music_count
        music_config["albumName"] = albumName
        music_config["albumId"] = albumId
        
        self.blood_spider_print_logger.blood_spider_print_info(f"成功获取音乐 ID {music_id} 播放页的数据")
        return music_config

    # 获取歌手的专辑
    def get_singer_album(self, album_id):
        request_url = self.base_url + f"/album/{album_id}/1.html"
        self.blood_spider_print_logger.blood_spider_print_info(f"开始根据专辑 ID {album_id} 获取歌手的专辑")
        self.blood_spider_print_logger.blood_spider_print_debug(f"构建请求 URL: {request_url}")
        
        tree = self._get_html_tree(request_url)
        
        if tree is None:
            self.blood_spider_print_logger.blood_spider_print_error(f"根据专辑 ID {album_id} 获取歌手的专辑时，HTML 解析失败")
            return {}
            
        self.blood_spider_print_logger.blood_spider_print_debug("查找歌曲列表元素")
        song_list_element = tree.xpath('//*[@class="play_list"]/ul')
        
        if not song_list_element:
            self.blood_spider_print_logger.blood_spider_print_warning(f"未找到歌曲列表元素，可能页面结构变化")
            return {}
            
        self.blood_spider_print_logger.blood_spider_print_debug("开始解析歌曲信息")
        music_list = self._get_song_ranking(song_list_element[0])
        
        # 艺人介绍
        artist_name_elements = tree.xpath('//div[@class="singer_info"]/div[@class="list_r"]/h1/text()')
        artistName = artist_name_elements[0] if artist_name_elements else "未知艺人"
        
        # artistDesc
        artist_desc_elements = tree.xpath('//div[@class="singer_info"]/div[@class="list_r"]/div[@class="info"]/p/text()')
        artistDesc = artist_desc_elements[0] if artist_desc_elements else "无介绍"
        
        self.blood_spider_print_logger.blood_spider_print_debug(f"艺人名称: {artistName}")
        
        music_config = self.music_config.get_singer_name_and_singer_introduction_and_singer_music_list()
        music_config["artistName"] = artistName
        music_config["artistDesc"] = artistDesc
        music_config["singer_music_list"] = music_list
        
        self.blood_spider_print_logger.blood_spider_print_info(f"根据专辑 ID {album_id} 获取歌手的专辑完成，共获取 {len(music_list)} 首歌曲")
        return music_config


if __name__ == '__main__':
    blood_spider_2t58 = BloodSpiderMusic2T58()
    
    index_data = blood_spider_2t58.get_singer_album("eHh3Y2Nz")
    
    print(f"获取完成，共获取 {len(index_data.get('singer_music_list', []))} 首歌曲 {index_data}")
    # print(index_data)  # 注释掉原始打印，避免输出大量数据