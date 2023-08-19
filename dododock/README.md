```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip freeze > requirements.txt 
```

```shell
$ source venv/bin/activate
$ pip freeze > requirements.txt 
$ docker build -t dododock:aws_lambda .
$ docker run -d -p 9000:8080 dododock:aws_lambda # -d : detach, in backgroound; -p : port number
$ docker ps
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
$ docker rm -f $(docker ps -f "ancestor=dododock:aws_lambda" -q)
# rm -f : 컨테이너 정지 후 제거; -q : id만, -f : 필터 적용. ancestor: 특정한 부모 이미지를 통해 만들어졌는지...
```