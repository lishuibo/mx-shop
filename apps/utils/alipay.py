from datetime import datetime

from Crypto.PublicKey import RSA

from Crypto.Signature import PKCS1_v1_5

from Crypto.Hash import SHA256

from base64 import b64encode, b64decode

from urllib.parse import quote_plus

from urllib.parse import urlparse, parse_qs

from urllib.request import urlopen

from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """

    支付宝支付接口

    """

    def __init__(self, appid, app_notify_url, app_private_key_path,

                 alipay_public_key_path, return_url, debug=False):

        self.appid = appid

        self.app_notify_url = app_notify_url

        self.app_private_key_path = app_private_key_path

        self.app_private_key = None

        self.return_url = return_url

        with open(self.app_private_key_path) as fp:

            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path

        with open(self.alipay_public_key_path) as fp:

            self.alipay_public_key = RSA.import_key(fp.read())

        if debug is True:

            self.__gateway = "https://openapi.alipaydev.com/gateway.do"

        else:

            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):

        biz_content = {

            "subject": subject,

            "out_trade_no": out_trade_no,

            "total_amount": total_amount,

            "product_code": "FAST_INSTANT_TRADE_PAY",

            # "qr_pay_mode":4

        }

        biz_content.update(kwargs)

        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)

        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):

        data = {

            "app_id": self.appid,

            "method": method,

            "charset": "utf-8",

            "sign_type": "RSA2",

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "version": "1.0",

            "biz_content": biz_content

        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url

            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):

        data.pop("sign", None)

        # 排序后的字符串

        unsigned_items = self.ordered_data(data)

        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)

        sign = self.sign(unsigned_string.encode("utf-8"))

        ordered_items = self.ordered_data(data)

        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串

        signed_string = quoted_string + "&sign=" + quote_plus(sign)

        return signed_string

    def ordered_data(self, data):

        complex_keys = []

        for key, value in data.items():

            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来

        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):

        # 开始计算签名

        key = self.app_private_key

        signer = PKCS1_v1_5.new(key)

        signature = signer.sign(SHA256.new(unsigned_string))

        # base64 编码，转换为unicode表示并移除回车

        sign = encodebytes(signature).decode("utf8").replace("\n", "")

        return sign

    def _verify(self, raw_content, signature):

        # 开始计算签名

        key = self.alipay_public_key

        signer = PKCS1_v1_5.new(key)

        digest = SHA256.new()

        digest.update(raw_content.encode("utf8"))

        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True

        return False

    def verify(self, data, signature):

        if "sign_type" in data:
            sign_type = data.pop("sign_type")

        # 排序后的字符串

        unsigned_items = self.ordered_data(data)

        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)

        return self._verify(message, signature)


if __name__ == "__main__":
    """支付请求过程"""

    # 传递参数初始化支付类

    alipay = AliPay(
        appid="2016101100663368",  # 设置签约的appid
        app_notify_url="http://10.10.10.167:8000/alipay/return",  # 异步支付通知url
        app_private_key_path="../trade/keys/private_2048.txt",
        alipay_public_key_path="../trade/keys/alipay_key_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,                                  # 设置是否是沙箱环境，True是沙箱环境
        return_url="http://10.10.10.167:8000/alipay/return"  # 同步支付通知url
    )

    # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，

    url = alipay.direct_pay(
        subject="123",  # 订单名称
        # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
        out_trade_no="201702021227",  # 订单号
        total_amount=0.01,  # 支付金额
        return_url="http://10.10.10.167:8000/alipay/return"  # 支付成功后，跳转url
    )



    # 将前面后的支付参数，拼接到支付网关

    # 注意：下面支付网关是沙箱环境，

    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)

    # 最终进行签名后组合成支付宝的url请求






    return_url = 'http://10.10.10.167:8000/alipay/return/?charset=utf-8&out_trade_no=20191014223058147&method=alipay.trade.page.pay.return&total_amount=23.00&sign=HAbuKs8XIqeWkt%2FQitQOgbvN0UoiCCMxNbxWcKMPHvsKINrFtBafqCX1p%2FnZ%2BTt3qDi4JLKacUA4msUaUO37rRrimPZ2wT0N%2FmqhvX79RiUXbBJU46%2FwMAdRW%2F5TJkplVOdiYu9jOX%2BQyj5W%2Flpb%2BQ59MFAbyMQldf3ubE0iQFNGq8Lop1Qr0Wv%2BHQ5y4DdDLLO16%2FET5NBH6VFwyY%2BoOj02lAdY8yklSUOJfkIXmY51WdTcxkJm0Lt5qajJ83Lb0uIdMHDvtY%2BLqqeVRLyIEMmbCMAaadPSLqPEpntJmasBHoGMWd%2FdTB2pyFuIJqZNZuZ2p7zDXN9jp9xLyqvl0Q%3D%3D&trade_no=2019101422001400821000080978&auth_app_id=2016101100663368&version=1.0&app_id=2016101100663368&sign_type=RSA2&seller_id=2088102179131003&timestamp=2019-10-14+22%3A31%3A58'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]

    for key, value in query.items():
        processed_query[key] = value[0]
    print (alipay.verify(processed_query, ali_sign))

    verify_re = alipay.verify(processed_query, ali_sign)

    if verify_re is True:
        order_sn = processed_query.get('out_trade_no', None)
        trade_no = processed_query.get('trade_no', None)
        trade_status = processed_query.get('trade_status', None)
        print(trade_status,trade_no,order_sn)
