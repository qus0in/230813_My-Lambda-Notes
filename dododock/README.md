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

#### 참고
* [컨테이너 이미지로 Python Lambda 함수 배포 - AWS Lambda](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-image.html#python-alt-test)
* [Docker 컨테이너 관련 커맨드 사용법](https://www.daleseo.com/docker-containers/)
* [\[Docker\] docker ps 명령어 및 옵션 사용법](https://freedeveloper.tistory.com/474)
* [Shell script\(쉘\) if 조건문, 조건식](https://hand-over.tistory.com/32)
* [\[Shell Script\] if ... else 조건문](https://brownbears.tistory.com/221)
* [awscli](https://formulae.brew.sh/formula/awscli)