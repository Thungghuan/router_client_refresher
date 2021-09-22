import requests
import os
import schedule
import time

hasNetwork = False


def refresh():
    # 没有断网的话不需要刷新配置
    global hasNetwork
    if hasNetwork:
        return

    session = requests.session()
    session.trust_env = False

    baseUrl = 'http://192.168.1.1/cgi-bin/luci'
    routerAdmin = {
        "luci_username": "root",
        "luci_password": os.getenv('LUCI_PWD')
    }

    loginRes = session.post(baseUrl, routerAdmin)
    loginRes.encoding = 'utf-8'
    token = loginRes.history[0].headers["Location"].split(';')[1]

    applyURL = baseUrl + '/;' + token
    applyData = {
        "cbi.submit": 1,
        "cbi.cbe.scutclient.cfg02c45e.enable": 1,
        "cbid.scutclient.cfg02c45e.enable": 1,
        "cbi.cbe.scutclient.cfg02c45e.plugin_redial": 1,
        "cbid.scutclient.cfg02c45e.plugin_redial": 1,
        "cbi.cbe.scutclient.cfg02c45e.debug": 1,
        "cbid.scutclient.cfg02c45e.mode": "Drcom",
        "cbid.scutclient.cfg04f383.username": "201930093111",
        "cbid.scutclient.cfg04f383.password": "11301711",
        "cbid.scutclient.cfg06c99a.version": "4472434f4d0096022a",
        "cbid.scutclient.cfg06c99a.hash": "2ec15ad258aee9604b18f2f8114da38db16efd00",
        "cbid.scutclient.cfg06c99a.server_auth_ip": "202.38.210.131",
        "cbid.scutclient.cfg06c99a.hostname": "DESKTOP-E513EA06",
        "cbid.scutclient.cfg06c99a.delay": 30,
        "cbi.apply": "Save & Apply"
    }
    applyRes = session.post(applyURL, applyData)
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
