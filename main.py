from cloudevents.http import CloudEvent
import functions_framework,json
from google.cloud import bigquery,storage

@functions_framework.cloud_event
def hello_gcs(cloud_event: CloudEvent) -> tuple:
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucketF = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]

    print(f"Event type: {event_type}")
    print(f"Bucket: {bucketF}")
    print(f"File: {name}")

    storageC=storage.Client()
    bucket = storageC.get_bucket('issues-secours')
    blob = bucket.blob(name)
    data = json.loads(blob.download_as_string(client=None))
    print(f"data: {data}")
    return bucket, name, timeCreated