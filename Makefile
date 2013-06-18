testenv:
	pip install -e .
	pip install -r requirements-test.txt
	pip install Django

test:
	flake8 dblogging --ignore=E501,E128,F403
	coverage run --branch --source=dblogging `which django-admin.py` test --settings=dblogging.tests.test_app.settings dblogging
	coverage report --omit=dblogging/tests*

.PHONY: test