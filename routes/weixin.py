from routes import *

import json

from models.user import User

import time

main = Blueprint('weixin', __name__)

_MODEL = User

# user = _MODEL.query.get_or_404(1)
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)



conf = WechatConf(
    token='vfg454t43jiog9s0u4g94gjor',
    appid='wxe4264a10d7d21d50',
    appsecret='5aec6ca609c887fe348c512bd54d64ef',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)


@main.route('/', methods=['GET', 'POST'])
def send_msg():
    data = request.args
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    signature = data.get('signature')

    status = wechat.check_signature(signature, timestamp, nonce)
    if not status:
        return abort(500)
    if request.method == 'GET':
        return data.get('echostr')
    else:
        try:
            print('\n into try')
            wechat.parse_data(request.data)
            message = wechat.message

            mt = message.type
            u = message.source
            print('\nmt check type', mt, 'and the user is', u)
            info = wechat.get_user_info(u, lang='zh_CN')
            print('\nthis is user info \n', type(info), info)
            if mt == 'click':
                k = wechat.message.key
                if k == 'KEY_CARD':
                    print('\ninto key card fuck this is fuck data', data)

                    # print('\n\n<', data, '>\n\n')
                    erwzma_info = {
                        # "expire_seconds": 604800,
                        "action_name": "QR_LIMIT_STR_SCENE",
                        "action_info": {
                            "scene": {
                                "scene_str": u
                            }
                        }
                    }

                    erwzma = wechat.create_qrcode(erwzma_info)
                    ticket = erwzma.get('ticket')
                    url = erwzma.get('url')
                    last_time = erwzma.get('expire_seconds')
                    print('\n\n this is ticket', ticket, '\nthis is url', url, '\n this is last time', last_time)
                    res =  wechat.show_qrcode(ticket)
                    file = 'static/img/{}.jpg'.format(u)
                    with open(file, 'wb') as fd:
                        print('\n\n', 'has been write', '\n\n')
                        for chunk in res.iter_content(1024):
                            fd.write(chunk)

                    f = open(file, "rb")

                    data = wechat.upload_media(media_type='image',media_file=f)
                    f.close()
                    fuck = data['media_id']
                    response = wechat.response_image(fuck)
                    return response
                                    # response = wechat.response_text(content='您的微信昵称是' + info.get('nickname'))
                    # return response

                    # response = wechat.response_image(
                    #     media_id='')
                    # return response
                return wechat.response_text(content='fuck')

            elif mt == 'subscribe':

                try:
                    # ticket = message.content
                    key = message.key
                    info = wechat.get_user_info(key[8:], lang='zh_CN')
                    text = '欢迎关注, 来自{}的推荐'.format(info.get('nickname'))
                    print(
                        '\nthis is key', key, type(key), '\n', info
                    )
                except:
                    text = '欢迎关注'


                response = wechat.response_text(content=text)

                return response


            if isinstance(message, TextMessage):
                reply_text = 'this is a TextMessage, content:' + wechat.message.content
                # return response
            elif isinstance(message, VoiceMessage):
                reply_text = 'voice'
            elif isinstance(message, ImageMessage):
                reply_text = 'image'
            elif isinstance(message, LinkMessage):
                reply_text = 'link'
            elif isinstance(message, LocationMessage):
                reply_text = 'location'
            elif isinstance(message, VideoMessage):
                reply_text = 'video'
            elif isinstance(message, ShortVideoMessage):
                reply_text = 'shortvideo'
            else:
                reply_text = '欢迎'
                return wechat.response_news([
                    {
                        'title': u'dfdfdfd',
                        'description': u'第一条新闻描述，这条新闻没有预览图',
                        'picurl':
                            u'https://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8qum85uzqj203d03fglj.jpg',
                        'url': u'https://www.baidu.com',
                    }
                ])
            response = wechat.response_text(content=reply_text)
            return response
        except:
            print('into except')
            response = wechat.response_text(content='uayemzgj')
            return response

            # return wechat.response_text(content='')
            # for i in request.args:
            #     print('this is new args', i, '\n\n\n')
            #
            # print()
            # return render_template('weixin_test.html')


@main.route('/fake/')
def fake_api():
    menu = {
        'button': [
            {
                'type': 'view',
                'name': '支持商户',
                'url': 'https://biaojiepay.com'
            },
            {
                'name': '@我',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': '1、认识我们',
                        'url': 'https://biaojiepay.com',
                    },
                    {
                        'type': 'view',
                        'name': '2、账户余额',
                        'url': 'https://biaojiepay.com',
                    },
                    {
                        'type': 'click',
                        'name': '3、专属名片',
                        'key': 'KEY_CARD',
                    },
                    {
                        'type': 'view',
                        'name': '4、账户充值',
                        'url': 'https://biaojiepay.com',
                    },
                    {
                        'type': 'view',
                        'name': '5、免费硬件',
                        'url': 'https://biaojiepay.com',
                    },
                ]
            }
        ]
    }

    wechat.create_menu(menu)

    return render_template('weixin_test.html')
