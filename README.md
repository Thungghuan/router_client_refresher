# Router_Client_Refresher

A little tool for me to refresh the router in my dormitory, and to learn docker...?

## Run the app

```shell
$ pip install  -r requirements.txt
$ export LUCI_PWD=<password>
$ python3 main.py 
```

## Run with [docker](https://hub.docker.com/r/thungghuan/router_client_refresher)

```shell
$ docker build -t thungghuan/router_client_refresher .
$ docker run -t -e LUCI_PWD=<password> thungghuan/router_client_refresher
```