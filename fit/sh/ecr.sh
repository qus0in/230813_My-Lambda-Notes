source sh/.sh
echo "DOCKER IMAGE : $DK_IMG_NAME:$DK_IMG_TAG"
echo $AWS_REGION $AWS_ACCOUNT_ID $AWS_ROLE

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