# /usr/bin/env

gcloud beta functions deploy webhook --runtime=python37 --source=. --trigger-http --region=europe-west1
