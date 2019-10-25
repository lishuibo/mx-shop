__author__ = 'litl'
"""

    client_id   必填  string  申请应用时分配的AppKey。

    redirect_uri    必填  string  授权回调地址，站外应用需与设置的回调地址一致。

    """

# 获取微博登录页面url

def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"

    redirect_url = "http://127.0.0.1:8000/complete/weibo"

    client_id = "836476381"

    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=client_id,

                                                                                      re_url=redirect_url)

    print(auth_url)


#获取登录的token，这里是拿到登录的code

#code会拼接在回调地址后面返回http://127.0.0.1:8001/complete/weibo/?code=c53bd7b5af51ec985952a3c03de3b

def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"

    import requests

    re_dict = requests.post(access_token_url, data={

        "client_id": "AppKey",

        "client_secret": "App Secret",

        "grant_type": "authorization_code",

        "code": code,

        "redirect_uri": "http://127.0.0.1:80001/complete/weibo/",

    })

    # '{"access_token":"2.00oneFMeMfeS0889036fBNW_B","remind_in":"15799","expires_in":15799,"uid":"5675652","isRealName":"true"}'

    pass


#获取带有微博用户json信息的url

def get_user_info(access_token):
    user_url = "https://api.weibo.com/2/users/show.json"

    uid = "5675652"

    get_url = user_url + "?access_token={at}&uid={uid}".format(at=access_token, uid=uid)

    print(get_url)


if __name__ == '__main__':
    get_auth_url()

    #通过code获取access_token

    # get_access_token("c53bd7b5af51ec985952a3c03de3b")

    #通过access_token获取用户的信息

    # get_user_info("2.00oneFMeMfeS0889036fBNW_B")