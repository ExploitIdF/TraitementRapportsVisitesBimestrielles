from cloudevents.http import CloudEvent
import functions_framework,json,io
from google.cloud import bigquery,storage

@functions_framework.cloud_event
def hello_gcs(cloud_event: CloudEvent) -> tuple:
    data = cloud_event.data
    bucketF = data["bucket"]
    name = data["name"]
    print(f"Bucket: {bucketF}")
    print(f"File: {name}")

    storageC=storage.Client()
    bucket = storageC.get_bucket('issues-secours')
    blob = bucket.blob(name)
    json_object = json.loads(blob.download_as_string().decode('utf-8'))
    strObj=''
    table_schema =[]
    for k in json_object.keys():
        strObj=strObj+','+json_object[k]
        table_schema.append({"name":k,"type":"STRING","mode":"NULLABLE" })
    strObj=strObj[1:]
    print(strObj)
    print('long strObj:', len(strObj.split(',')))
    print(table_schema)

    def format_schema(schema):
        formatted_schema = []
        for row in schema:
            formatted_schema.append(bigquery.SchemaField(row['name'], row['type'], row['mode']))
        return formatted_schema
    print('long schema:', len(table_schema ))
    client  = bigquery.Client()
    dataset  = client.dataset('rapports_visites')
    table = dataset.table('tb4')

    job_config = bigquery.LoadJobConfig()
    job_config.schema = format_schema(table_schema)
    st8='L10.375C,2024-02-13 00:42:00,Karen,R2,R6,R0,R3,R1,R0,R4,R0,R0,R2,R2,R1,R1,R2,R0'
    job = client.load_table_from_file(io.StringIO(st8), table, job_config = job_config)

    print(job.result())

    return name