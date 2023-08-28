```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install requests
$ pip install pandas
$ pip freeze > requirements.txt
$ export notion_api_key=...
$ python main.py
$ sh sh/build_and_test.sh && sh sh/ecr.sh
```