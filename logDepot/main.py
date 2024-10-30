#LogDepot
from cloudevents.http import CloudEvent
import functions_framework,json,io
from google.cloud import bigquery,storage

@functions_framework.cloud_event
def logdepot(cloud_event: CloudEvent) -> tuple:
    data = cloud_event.data
    bucketF = data["bucket"]
    name = data["name"]
    timeCreated = data["timeCreated"]
    print(f"Bucket : {bucketF} ;  File: {name}")
    storageC=storage.Client()
    bucket = storageC.get_bucket('issues-secours')
    blob = bucket.blob(name)
    fileContent= (blob.download_as_string(client=None))
    
    def format_schema(schema):
        formatted_schema = []
        for row in schema:
            formatted_schema.append(bigquery.SchemaField(row['name'], row['type'], row['mode']))
        return formatted_schema

    table_schema = [{"name":"filename","type":"STRING","mode":"NULLABLE" },
    {"name":"HoroDate","type":"STRING","mode":"NULLABLE" },   
    {"name":"Longueur","type":"STRING","mode":"NULLABLE" },
        {"name":"Longueur2","type":"STRING","mode":"NULLABLE" },
    ]
    print('long schema:', len(table_schema ))
    client  = bigquery.Client()
    dataset  = client.dataset('rapports_visites')
    table = dataset.table('LogDepot')

    job_config = bigquery.LoadJobConfig()
   # job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = format_schema(table_schema)
    st3=name+','+timeCreated+','+str(len(fileContent))+',1'
    job = client.load_table_from_file(io.StringIO(st3), table, job_config = job_config)

    print(job.result())
    return name