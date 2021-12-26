setup: ##@Install Dependencies
	mkdir ~/.virtualenvs
	python3 -m venv ~/.virtualenvs/kibaro-user-svc.py
	source ~/.virtualenvs/kibaro-user-svc.py/bin/activate
	pip install -r requirements.txt
up: ##@Run locally
	docker-compose up --build
down: ##@Stop containers
	docker-compose down
deploy: ##@Build and deploy to Cloud Run
	gcloud builds submit --tag gcr.io/kibaro-test/kibarot-user-svc.py
	gcloud beta run deploy --image gcr.io/kibaro-test/kibaro-user-svc.py --platform managed --allow-unauthenticated
