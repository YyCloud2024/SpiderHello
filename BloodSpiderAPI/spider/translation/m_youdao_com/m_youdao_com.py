# 有道翻译 - 手机版
import requests
from lxml import etree
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.translation import Translation
class YoudaoTranslate:
    def __init__(self):
        self.base_url = "https://m.youdao.com/translate"
        self.common_utils = GeneralToolkit()
        self.translation = Translation()
    # 获取翻译语言
    def get_language(self):
        html_text = etree.HTML(requests.get(self.base_url).text)
        options = html_text.xpath("//div[@class='select']/select/option")
        language_list = []
        for item in options:
            create_value = self.translation.get_language()
            create_value["name"] = item.xpath("./text()")[0]
            create_value["value"] = item.xpath("./@value")[0]
            language_list.append(create_value)
        return language_list


    # 翻译接口
    def translate(self, text, type_language="AUTO"):
        headers = self.common_utils.get_headers(ua_device_type="mobile")
        data = {
            'inputtext': text,
            'type': type_language,
        }
        create_translate = self.translation.translate()
        response = requests.post(self.base_url,  headers=headers, data=data).text
        html_text = etree.HTML(response)
        translation_text = html_text.xpath("//ul[@id='translateResult']/li/text()")[0]
        create_translate["text"] = text
        create_translate["translate_text"] = translation_text
        return create_translate

if __name__ == '__main__':
    youdao = YoudaoTranslate()
    print(youdao.get_language())
    print(youdao.translate("Warm reminder: The project is constantly being updated. It is recommended to pay attention to the project update status. If you need to be the first to receive notifications about new features, please add wechat: duyanbz to join the technical exchange group."))