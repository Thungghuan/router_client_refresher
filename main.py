import requests
import json
import schedule
import time

hasNetwork = False

with open('config.json', 'r') as f:
    config = json.load(f)


def refresh():
    # 没有断网的话不需要刷新配置
    global hasNetwork
    if hasNetwork:
        return
    
    session = requests.session()
    session.trust_env = False

    baseUrl = config["routerHost"] + '/cgi-bin/luci'

    loginRes = session.post(baseUrl, config["routerAdmin"])
    loginRes.encoding = 'utf-8'
    token = loginRes.history[0].headers["Location"].split(';')[1]

    applyURL = baseUrl + '/;' + token
    applyRes = session.post(applyURL, config["applyData"])
    print(applyRes.status_code)


def testNetwork():
    r = requests.get('http://www.baidu.com', timeout=5)
    print(r)
    global hasNetwork
    if r.status_code == 200:
        hasNetwork = True
    else:
        hasNetwork = False


def main():
    print("Refresh server started.")

    # 每天3点检查当晚是否断网
    schedule.every().day.at("03:00").do(testNetwork)

    # 每天6点15进行配置更新
    schedule.every().day.at("06:15").do(refresh)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
