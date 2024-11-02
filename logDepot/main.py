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
    fileContent= (blob.download_as_string(client=None).decode())
    
    def format_schema(schema):
        formatted_schema = []
        for row in schema:
            formatted_schema.append(bigquery.SchemaField(row))
        return formatted_schema
    lst_schema_VBIS = ['Tatouage', 'HoroDate', 'Agent', 'PC0', 'CM0', 'PC1', 'CM1', 'PC2', 'CM2', 'PC3', 'CM3', 'PC4', 'CM4', 'PC5', 'CM5', 'PC6', 'CM6', 
                  'PC7', 'CM7', 'PC8', 'CM8', 'PC9', 'CM9', 'PC10', 'CM10', 'PC11', 'CM11', 'PC12', 'CM12', 'PC13', 'CM13', 'PC14', 'CM14']

    client  = bigquery.Client()
    dataset  = client.dataset('rapports_visites')
    table = dataset.table('LogDepot')

    job_config = bigquery.LoadJobConfig()
   # job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = format_schema(lst_schema_VBIS)
    st3=name+','+timeCreated+','+str(len(fileContent))+',1'
    job = client.load_table_from_file(io.StringIO(st3), table, job_config = job_config)

    print(job.result())
    return name