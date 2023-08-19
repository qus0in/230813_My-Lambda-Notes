export DK_IMG_NAME=dododock
export DK_IMG_TAG=aws_lambda
export TEST_URL=http://localhost:9000/2015-03-31/functions/function/invocations
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
docker run -d -p 9000:8080 $DK_IMG_NAME:$DK_IMG_TAG
# -d : detach, in backgroound; -p : port number
echo "😎 AWS LAMBDA TEST"
curl -XPOST $TEST_URL -d '{}'
echo ""

# [종료]
echo "😎 DOCKER KILL"
docker rm -f $(docker ps -f "ancestor=$DK_IMG_NAME:$DK_IMG_TAG" -q)
# rm -f : 컨테이너 정지 후 제거;
# -q : id만, -f : 필터 적용. ancestor: 특정한 부모 이미지를 통해 만들어졌는지...

# [업로드]
if [ -e "./.env" ]; then
    echo "😏 You have .env!"
    source ./.env
    echo $AWS_REGION $AWS_ACCOUNT_ID $AWS_ROLE
else
    echo "🤨 Please make .env!"
    exit
fi

# [인증]
echo "🤓 Check LOGIN"
aws ecr get-login-password \
--region $AWS_REGION \
| docker login \
    --username AWS \
    --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com

# [저장소]
echo "🤓 Check ECR"
aws ecr create-repository \
    --repository-name $DK_IMG_NAME \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE
export DK_REPO_URI="$AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/${DK_IMG_NAME}:latest"
docker tag $DK_IMG_NAME:$DK_IMG_TAG $DK_REPO_URI
docker push $DK_REPO_URI

# [람다함수 생성]
echo "🤓 Check AWS Lambda"
aws lambda create-function \
  --function-name $DK_IMG_NAME \
  --package-type Image \
  --code ImageUri=$DK_REPO_URI \
  --role $AWS_ROLE \
  --architectures arm64

# [람다함수 호출]
aws lambda invoke --function-name $DK_IMG_NAME response.json
echo "🥳 FINISH!"
