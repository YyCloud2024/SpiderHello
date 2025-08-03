# 该文件负责文件上传的操作，包括切片文件、生成授权信息、上传切片和合并文件等。
import hmac
import hashlib
import base64
import requests
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import time
import json
from BloodSpiderModel.BloodSpiderPrint.blood_spider_print_logger import BloodSpiderPrintLogger

# 初始化日志记录器
logger = BloodSpiderPrintLogger(is_show=True)

class RecCloudUploader:
    def __init__(self, headers):
        # 初始化请求头
        self.headers = headers
        self.x_oss_user_agent = 'aliyun-sdk-js/6.9.0 Chrome 137.0.0.0 on Windows 10 64-bit'
        logger.blood_spider_print_info(f"RecCloudUploader 初始化完成，请求头: {self.headers}")

    # 生成XML
    def generate_xml(self, parts_data):
        logger.blood_spider_print_debug(f"开始生成XML，包含 {len(parts_data)} 个分片数据")
        try:
            root = ET.Element('CompleteMultipartUpload')

            for part in parts_data:
                part_element = ET.SubElement(root, 'Part')

                number_element = ET.SubElement(part_element, 'PartNumber')
                number_element.text = str(part['number'])

                tag_element = ET.SubElement(part_element, 'ETag')
                tag_element.text = part['tag']  # 假设输入数据已包含双引号

            # 简单美化（添加缩进）
            ET.indent(root, space='    ')

            # 生成不带声明的XML
            xml_bytes = ET.tostring(root, encoding='utf-8', method='xml')

            # 手动添加声明（兼容所有Python版本）
            xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
            xml_result = xml_declaration + xml_bytes.decode('utf-8')
            logger.blood_spider_print_debug("XML生成完成")
            return xml_result
        except Exception as e:
            logger.blood_spider_print_error(f"XML生成失败: {str(e)}")
            return None

    # 计算MD5 Base64编码
    def calculate_md5_base64(self, input_string):
        try:
            # 将输入字符串编码为UTF-8字节
            input_bytes = input_string.encode('utf-8')

            # 计算MD5哈希值
            md5_hash = hashlib.md5(input_bytes).digest()

            # 将哈希值转换为Base64编码
            base64_result = base64.b64encode(md5_hash).decode('ascii')

            logger.blood_spider_print_debug("MD5-Base64计算完成")
            return base64_result
        except Exception as e:
            logger.blood_spider_print_error(f"MD5-Base64计算失败: {str(e)}")
            return None

    # 把一个字典转换为json字符串，然后进行base64编码
    def base64_encode(self, data):
        try:
            result = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
            logger.blood_spider_print_debug("Base64编码完成")
            return result
        except Exception as e:
            logger.blood_spider_print_error(f"Base64编码失败: {str(e)}")
            return None

    # 生成格式为 'Mon, 23 Jun 2025 07:23:29 GMT' 的时间字符串
    def get_gmt_time(self, future_days=0, future_hours=0):
        """
        生成格式为 'Mon, 23 Jun 2025 07:23:29 GMT' 的时间字符串

        参数:
            future_days (int): 在当前时间基础上增加的天数
            future_hours (int): 在当前时间基础上增加的小时数

        返回:
            str: 格式化的时间字符串
        """
        try:
            # 获取当前时间并添加指定的偏移量
            current_time = datetime.now().timestamp()
            future_time = current_time + (future_days * 86400) + (future_hours * 3600)

            # 转换为GMT格式
            formatted_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(future_time))

            logger.blood_spider_print_debug(f"生成GMT时间: {formatted_time}")
            return formatted_time
        except Exception as e:
            logger.blood_spider_print_error(f"GMT时间生成失败: {str(e)}")
            return None

    # 计算HMAC-SHA1 Base64编码
    def calculate_hmac_sha1_base64(self, key: str, message: str) -> str:
        try:
            # 将密钥转换为字节（假设使用UTF-8编码）
            key_bytes = key.encode('utf-8')

            # 创建HMAC对象，使用SHA-1哈希算法
            hmac_obj = hmac.new(key_bytes, digestmod=hashlib.sha1)

            # 更新消息（转换为UTF-8字节）
            message_bytes = message.encode('utf-8')
            hmac_obj.update(message_bytes)

            # 计算哈希值并转换为Base64字符串
            digest_bytes = hmac_obj.digest()
            digest_base64 = base64.b64encode(digest_bytes).decode('ascii')

            logger.blood_spider_print_debug("HMAC-SHA1-Base64计算完成")
            return digest_base64
        except Exception as e:
            logger.blood_spider_print_error(f"HMAC-SHA1-Base64计算失败: {str(e)}")
            return None

    # 将XML字符串转换为字典
    def xml_to_dict(self, xml_string: str) -> dict:
        """将XML字符串转换为字典"""
        try:
            root = ET.fromstring(xml_string)
            result = {}
            for child in root:
                result[child.tag] = child.text
            logger.blood_spider_print_debug(f"XML转换为字典完成: {result}")
            return result
        except Exception as e:
            logger.blood_spider_print_error(f"XML转换为字典失败: {str(e)}")
            return {}

    # 制作headers中的authorization
    def get_authorization(self,
                          x_oss_security_token: str,
                          reccloudsz_bucket: str,
                          access_key_id: str,
                          access_key_secret: str,
                          content_md5: str = '',
                          x_oss_user_agent: str = None,
                          method: str = 'PUT',
                          content_type: str = 'video/mp4',
                          oss_date: str = None,
                          ) -> str:
        logger.blood_spider_print_debug(f"生成授权信息，方法: {method}, 内容类型: {content_type}")
        if x_oss_user_agent is None:
            x_oss_user_agent = self.x_oss_user_agent
        if oss_date is None:
            oss_date = self.get_gmt_time()
            if oss_date is None:
                logger.blood_spider_print_error("生成授权信息时，获取GMT时间失败，终止授权生成")
                return None

        message = f'{method}\n{content_md5}\n{content_type}\n{oss_date}\nx-oss-date:{oss_date}\nx-oss-security-token:{x_oss_security_token}\nx-oss-user-agent:{x_oss_user_agent}\n{reccloudsz_bucket}'
        hmac_result = self.calculate_hmac_sha1_base64(access_key_secret, message)
        if hmac_result is None:
            logger.blood_spider_print_error("生成授权信息时，HMAC-SHA1-Base64计算失败，终止授权生成")
            return None
        auth = "OSS " + access_key_id + ":" + hmac_result
        logger.blood_spider_print_debug("授权信息生成完成")
        return auth

    # 生成V2授权信息
    def get_authorization_v2(self,
                             method: str,
                             content_md5: str,
                             content_type: str,
                             date: str,
                             x_oss_callback: str,
                             x_oss_security_token: str,
                             x_oss_user_agent: str,
                             bucket: str,
                             access_key_id: str,
                             access_key_secret: str,
                             ) -> str:
        logger.blood_spider_print_debug(f"生成V2授权信息，方法: {method}, 内容类型: {content_type}")
        message = f"{method}\n{content_md5}\n{content_type}\n{date}\nx-oss-callback:{x_oss_callback}\nx-oss-date:{date}\nx-oss-security-token:{x_oss_security_token}\nx-oss-user-agent:{x_oss_user_agent}\n{bucket}"
        hmac_result = self.calculate_hmac_sha1_base64(access_key_secret, message)
        if hmac_result is None:
            logger.blood_spider_print_error("生成V2授权信息时，HMAC-SHA1-Base64计算失败，终止授权生成")
            return None
        auth = "OSS " + access_key_id + ":" + hmac_result
        logger.blood_spider_print_debug("V2授权信息生成完成")
        return auth

    # 按指定大小切片MP4文件
    def slice_mp4_file(self, file_path: str, slice_size: int = 2 * 1024 * 1024) -> list[bytes]:
        """
        按指定大小切片MP4文件

        参数:
        - file_path: MP4文件路径
        - slice_size: 每个切片的大小（默认2MB）

        返回:
        - 包含所有切片数据的列表，每个元素为bytes类型
        """
        logger.blood_spider_print_info(f"开始切片文件: {file_path}, 切片大小: {slice_size} 字节")
        slices = []

        try:
            with open(file_path, 'rb') as file:
                # 循环读取文件直到结束
                slice_count = 0
                while True:
                    data = file.read(slice_size)
                    if not data:
                        break
                    slices.append(data)
                    slice_count += 1
                    if slice_count % 10 == 0:  # 每10个切片记录一次日志
                        logger.blood_spider_print_debug(f"已完成 {slice_count} 个切片")

            logger.blood_spider_print_info(f"文件切片完成，共 {len(slices)} 个切片")

        except Exception as e:
            logger.blood_spider_print_error(f"文件切片过程中出错: {str(e)}")
            return []

        return slices

    # 上传文件到RecCloud
    def upload_file_to_reccloud(self, file_path):
        """
        上传文件到RecCloud，只需提供文件路径即可完成整个上传过程

        参数:
        - file_path: 要上传的文件路径

        返回:
        - 上传完成后的响应数据
        """
        logger.blood_spider_print_info(f"开始上传文件到RecCloud: {file_path}")

        # 基础准备
        filenames = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1] if "\\" in file_path else file_path
        logger.blood_spider_print_debug(f"文件名: {filenames}")
        date = self.get_gmt_time()
        if date is None:
            logger.blood_spider_print_error("上传文件时，获取GMT时间失败，终止上传")
            return {"success": False, "message": "获取GMT时间失败"}

        logger.blood_spider_print_info("开始切片文件")
        slices = self.slice_mp4_file(file_path)
        if not slices:
            logger.blood_spider_print_error("文件切片失败，终止上传")
            return {"success": False, "message": "文件切片失败"}

        # 请求oss获取上传配置密钥(准备工作)
        logger.blood_spider_print_info("请求OSS获取上传配置")

        data = f'{{"region":"","filenames":"{filenames}"}}'.encode()
        logger.blood_spider_print_debug("发送授权请求")
        try:
            authorizations_oss_response = requests.post(f'https://aw.aoscdn.com/app/reccloud/v2/authorizations/oss', headers=self.headers, data=data).json()
            logger.blood_spider_print_debug(f"授权响应: {authorizations_oss_response}")
        except Exception as e:
            logger.blood_spider_print_error(f"请求OSS授权时出错: {str(e)}")
            return {"success": False, "message": "请求OSS授权时出错"}

        if authorizations_oss_response.get('status') != 200:
            logger.blood_spider_print_error(f"获取上传配置失败: {authorizations_oss_response.get('message', '未知错误')}")
            return {"success": False, "message": "获取上传配置失败", "response": authorizations_oss_response}

        logger.blood_spider_print_info("成功获取上传配置")
        authorization = self.get_authorization(
            access_key_id=authorizations_oss_response['data']['credential']['access_key_id'],
            x_oss_security_token=authorizations_oss_response['data']['credential']['security_token'],
            reccloudsz_bucket=f"/{authorizations_oss_response['data']['bucket']}/{authorizations_oss_response['data']['objects'][filenames]}?uploads",
            access_key_secret=authorizations_oss_response['data']['credential']['access_key_secret'],
            oss_date=date,
            method="POST"
        )
        if authorization is None:
            logger.blood_spider_print_error("生成授权信息失败，终止上传")
            return {"success": False, "message": "生成授权信息失败"}

        # 保证全部请求头名称需要转为小写。
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'video/mp4',
            'Origin': 'https://reccloud.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://reccloud.cn/speech-to-text-online-start?v=startSelectFile',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'authorization': authorization,
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-oss-date': date,
            'x-oss-security-token': authorizations_oss_response['data']['credential']['security_token'],
            'x-oss-user-agent': self.x_oss_user_agent,
        }

        logger.blood_spider_print_info("初始化分片上传")
        try:
            xml_response = requests.post(
                f'https://reccloudsz.oss-cn-shenzhen.aliyuncs.com/{authorizations_oss_response["data"]["objects"][filenames]}',
                params={
                    'uploads': '',
                },
                headers=headers,
            ).text
            logger.blood_spider_print_debug(f"分片上传初始化响应: {xml_response}")
        except Exception as e:
            logger.blood_spider_print_error(f"分片上传初始化请求出错: {str(e)}")
            return {"success": False, "message": "分片上传初始化请求出错"}

        xml_to_dict_post = self.xml_to_dict(xml_response)
        upload_id = xml_to_dict_post.get('UploadId')
        if upload_id is None:
            logger.blood_spider_print_error("未获取到上传ID，终止上传")
            return {"success": False, "message": "未获取到上传ID"}
        logger.blood_spider_print_info(f"获取上传ID: {upload_id}")

        parts_data = []
        logger.blood_spider_print_info(f"开始上传文件切片，共 {len(slices)} 个切片")
        for i, slice in enumerate(slices):
            logger.blood_spider_print_info(f"上传切片 {i + 1}/{len(slices)}")
            date = self.get_gmt_time()
            if date is None:
                logger.blood_spider_print_error(f"上传切片 {i + 1} 时，获取GMT时间失败，终止上传")
                return {"success": False, "message": f"上传切片 {i + 1} 时，获取GMT时间失败"}

            authorization = self.get_authorization(
                access_key_id=authorizations_oss_response['data']['credential']['access_key_id'],
                x_oss_security_token=authorizations_oss_response['data']['credential']['security_token'],
                reccloudsz_bucket=f"/{authorizations_oss_response['data']['bucket']}/{authorizations_oss_response['data']['objects'][filenames]}?partNumber={i + 1}&uploadId={upload_id}",
                access_key_secret=authorizations_oss_response['data']['credential']['access_key_secret'],
                oss_date=date,
                method="PUT"
            )
            if authorization is None:
                logger.blood_spider_print_error(f"上传切片 {i + 1} 时，生成授权信息失败，终止上传")
                return {"success": False, "message": f"上传切片 {i + 1} 时，生成授权信息失败"}

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'video/mp4',
                'Origin': 'https://reccloud.cn',
                'Pragma': 'no-cache',
                'Referer': 'https://reccloud.cn/speech-to-text-online-start?v=startSelectFile',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'authorization': authorization,
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'x-oss-date': date,
                'x-oss-security-token': authorizations_oss_response['data']['credential']['security_token'],
                'x-oss-user-agent': self.x_oss_user_agent,
            }
            params = {
                'partNumber': i + 1,
                'uploadId': upload_id,
            }
            data = slice
            logger.blood_spider_print_debug(f"发送切片上传请求: 切片 {i + 1}")
            try:
                response = requests.put(
                    f'https://reccloudsz.oss-cn-shenzhen.aliyuncs.com/{authorizations_oss_response["data"]["objects"][filenames]}',
                    params=params,
                    headers=headers,
                    data=data,
                )
            except Exception as e:
                logger.blood_spider_print_error(f"上传切片 {i + 1} 时，请求出错: {str(e)}")
                return {"success": False, "message": f"上传切片 {i + 1} 时，请求出错"}

            if response.status_code == 200:
                logger.blood_spider_print_info(f"切片 {i + 1} 上传成功")
                # 得到服务器的ETag
                etag = response.headers.get('ETag')
                if etag is None:
                    logger.blood_spider_print_error(f"切片 {i + 1} 上传成功，但未获取到ETag，终止上传")
                    return {"success": False, "message": f"切片 {i + 1} 上传成功，但未获取到ETag"}
                logger.blood_spider_print_debug(f"切片 {i + 1} ETag: {etag}")
                # 将ETag添加到parts_data中
                parts_data.append({
                    'number': i + 1,
                    'tag': etag,
                })
            else:
                error_msg = f"切片{i + 1}上传失败: {response.status_code} - {response.text}"
                logger.blood_spider_print_error(error_msg)
                return {"success": False, "message": f"切片{i + 1}上传失败", "response": response.text}

        # 上传完所有切片后完成合并
        logger.blood_spider_print_info("所有切片上传完成，开始合并文件")
        date = self.get_gmt_time()
        if date is None:
            logger.blood_spider_print_error("合并文件时，获取GMT时间失败，终止合并")
            return {"success": False, "message": "合并文件时，获取GMT时间失败"}

        xml_data = self.generate_xml(parts_data)
        if xml_data is None:
            logger.blood_spider_print_error("合并文件时，生成XML数据失败，终止合并")
            return {"success": False, "message": "合并文件时，生成XML数据失败"}
        xml_data = xml_data.replace("        ", "").replace("    ", '')
        xml_data_md5 = self.calculate_md5_base64(xml_data)
        if xml_data_md5 is None:
            logger.blood_spider_print_error("合并文件时，计算XML数据MD5失败，终止合并")
            return {"success": False, "message": "合并文件时，计算XML数据MD5失败"}

        o = {
            "callbackUrl": authorizations_oss_response['data']['callback']['url'],
            "callbackBody": authorizations_oss_response['data']['callback']['body'].replace("${filename}", filenames)
        }
        logger.blood_spider_print_error(f"o =======   {o}")
        # 对 o 进行base64编码
        o = self.base64_encode(o)
        if o is None:
            logger.blood_spider_print_error("合并文件时，对回调信息进行Base64编码失败，终止合并")
            return {"success": False, "message": "合并文件时，对回调信息进行Base64编码失败"}

        logger.blood_spider_print_debug("生成合并请求授权")
        authorization = self.get_authorization_v2(
            method="POST",
            content_md5=xml_data_md5,
            content_type="application/xml",
            date=date,
            x_oss_callback=o,
            x_oss_security_token=authorizations_oss_response['data']['credential']['security_token'],
            x_oss_user_agent=self.x_oss_user_agent,
            bucket=f"/{xml_to_dict_post['Bucket']}/{xml_to_dict_post['Key']}?uploadId={upload_id}",
            access_key_id=authorizations_oss_response['data']['credential']['access_key_id'],
            access_key_secret=authorizations_oss_response['data']['credential']['access_key_secret'],
        )
        if authorization is None:
            logger.blood_spider_print_error("合并文件时，生成授权信息失败，终止合并")
            return {"success": False, "message": "合并文件时，生成授权信息失败"}

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Md5': xml_data_md5,
            'Content-Type': 'application/xml',
            'Origin': 'https://reccloud.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://reccloud.cn/speech-to-text-online-start?v=startSelectFile',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'host': 'reccloudsz.oss-cn-shenzhen.aliyuncs.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'authorization': authorization,
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-oss-callback': o,
            'x-oss-date': date,
            'x-oss-security-token': authorizations_oss_response['data']['credential']['security_token'],
            'x-oss-user-agent': self.x_oss_user_agent,
        }

        logger.blood_spider_print_info("发送文件合并请求")
        try:
            final_response = requests.post(
                f'https://{authorizations_oss_response["data"]["bucket"]}.{authorizations_oss_response["data"]["endpoint"]}/{authorizations_oss_response["data"]["objects"][filenames]}?uploadId={upload_id}',
                headers=headers,
                data=xml_data,
            )
        except Exception as e:
            logger.blood_spider_print_error(f"文件合并请求出错: {str(e)}")
            return {"success": False, "message": "文件合并请求出错"}

        try:
            result = final_response.json()
            logger.blood_spider_print_info("文件上传完成，服务器返回JSON响应")
            logger.blood_spider_print_debug(f"上传完成响应: {result}")
            return {"success": True, "data": result}
        except:
            logger.blood_spider_print_warning("文件上传完成，但返回结果不是JSON格式")
            logger.blood_spider_print_debug(f"非JSON响应内容: {final_response.text}")
            return {"success": True, "data": final_response.text}
