SHELL := /usr/bin/env bash

# Commands API: UMAP
export_documents:
	python export_documents.py document https://www.notion.so/jasonbenn/d7a04baa1cea4dda983747b04ae3ddaa?v=727ed26317ec44caa4c9f2d8393a09b5

vectorize_documents:
	python vectorize.py

plot_umap:
	python plot_umap.py

# Utility
copy_umap_json:
	cat ~/.notion-to-anki/umaps/nieghbors_10__min_dist_0.5.json | pbcopy

# DB
initdb:
	createuser -s -P worldview


createdb:
	echo "make password worldview"
	createdb -W -h 127.0.0.1 worldview -U worldview -p 5432
	./manage.py migrate
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'nah@nah.com', 'admin')" | python manage.py shell
	./manage.py seed_notion_dbs

dropdb:
	dropdb worldview


psql:
	psql postgresql://notion_to_anki:notion_to_anki@127.0.0.1:5432/notion_to_anki

migrate:
	web/manage.py migrate

init_bert_as_a_service:
	echo "ssh ml-box"
	echo "cd code/text-mapper"
	echo "./run.sh"


# Server
runserver:
	./manage.py runserver --nothreading --noreload
