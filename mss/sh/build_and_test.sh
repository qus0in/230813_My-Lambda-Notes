source sh/.sh
echo "DOCKER IMAGE : $DK_IMG_NAME:$DK_IMG_TAG"

# [빌드]
echo "😎 DOCKER BUILD"
if [ -e "./venv" ]; then
    echo "😏 You use venv!"
    source venv/bin/activate
    pip freeze > requirements.txt 
else
    echo "😉 requirements.txt ONLY"
fi
docker build -t $DK_IMG_NAME:$DK_IMG_TAG .

# [테스트]
echo "😎 DOCKER RUN"
# docker run -d -p 9000:8080 $DK_IMG_NAME:$DK_IMG_TAG
docker run --env-file .env -d -p 9000:8080 $DK_IMG_NAME:$DK_IMG_TAG 
# -d : detach, in backgroound; -p : port number
echo "😎 AWS LAMBDA TEST"
curl -XPOST $TEST_URL -d '{}'
echo ""

# [종료]
echo "😎 DOCKER KILL"
docker rm -f $(docker ps -f "ancestor=$DK_IMG_NAME:$DK_IMG_TAG" -q)
# rm -f : 컨테이너 정지 후 제거;
# -q : id만, -f : 필터 적용. ancestor: 특정한 부모 이미지를 통해 만들어졌는지...