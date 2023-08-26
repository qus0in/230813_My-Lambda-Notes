export DK_IMG_NAME=selena
export DK_IMG_TAG=aws_lambda
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