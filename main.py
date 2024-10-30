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
    json_object = json.loads(blob.download_as_string(client=None))
    strObj=''
    for k in json_object.keys():
        strObj=strObj+','+json_object[k]
    strObj=strObj[1:]
    print('#'+strObj+'#')
    print('long strObj:', len(strObj.split(',')))

    def format_schema(schema):
        formatted_schema = []
        for row in schema:
            formatted_schema.append(bigquery.SchemaField(row['name'], row['type'], row['mode']))
        return formatted_schema

    table_schema = [{"name":"Tatouage","type":"STRING","mode":"NULLABLE" },{"name":"HoroDate","type":"STRING","mode":"NULLABLE" },{"name":"PorteTunnelDef","type":"STRING","mode":"NULLABLE" },{"name":"PorteExterieureDef","type":"STRING","mode":"NULLABLE" },{"name":"PorteInterieureDef","type":"STRING","mode":"NULLABLE" },{"name":"PropreteDef","type":"STRING","mode":"NULLABLE" },{"name":"VacuiteDef","type":"STRING","mode":"NULLABLE" },{"name":"EclairageDef","type":"STRING","mode":"NULLABLE" }]
    print('long schema:', len(table_schema ))
    client  = bigquery.Client()
    dataset  = client.dataset('rapports_visites')
    table = dataset.table('tb3')

    job_config = bigquery.LoadJobConfig()
   # job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = format_schema(table_schema)
    st8='c10.366R,zz,"3ê",c0,0_Serrurerie,c1_Main courrante,c0_Issu,c1_2'
    job = client.load_table_from_file(io.StringIO(st8), table, job_config = job_config)

    print(job.result())

    return name