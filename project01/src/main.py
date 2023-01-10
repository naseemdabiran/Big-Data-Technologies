from sodapy import Socrata
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, date
import json
import argparse
import sys
import os

 
parser = argparse.ArgumentParser(description='Fire Incident Dispatch Data')
parser.add_argument('--page_size', type=int, help='how many rows to get per page', required=True)
parser.add_argument('--num_pages', type=int, help='how many pages to get in total')
args = parser.parse_args(sys.argv[1:])
print(args)

DATASET_ID=os.environ["DATASET_ID"]     
APP_TOKEN=os.environ["APP_TOKEN"]       
ES_HOST=os.environ["ES_HOST"]           
ES_USERNAME=os.environ["ES_USERNAME"]  
ES_PASSWORD=os.environ["ES_PASSWORD"]  
INDEX_NAME=os.environ["INDEX_NAME"]    


if __name__ == '__main__':
    
    try:
        resp = requests.put(f"{ES_HOST}/{INDEX_NAME}", auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                json={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 1
                    },
                    "mappings": {
                        "properties": {
                            "starfire_incident_id": {"type": "float"},
                            "incident_datetime": {"type": "date"},
                            "incident_classification": {"type": "keyword"},
                            "incident_borough": {"type": "keyword"},
                            "engines_assigned_quantity": {"type": "float"},
                            "incident_response_seconds_qy": {"type": "float"},
                            "valid_incident_rspns_time_indc": {"type": "keyword"},
                        }
                    },
                }
            )
        resp.raise_for_status()
        print(resp.json())
        
    except Exception as e:
        print("Index already exists! Skipping")    

    client = Socrata("data.cityofnewyork.us", APP_TOKEN, timeout=10000)
    
    tot_rows=client.get(DATASET_ID, select="COUNT(*)")[0]["COUNT"]
    record_count = 0
    if (not args.num_pages):
        args.num_pages =  (int(tot_rows)//args.page_size) + 1
    
    for n in range(args.num_pages):
        rows = client.get(DATASET_ID, limit=args.page_size, offset=n*args.page_size, where = "incident_datetime IS NOT NULL AND starfire_incident_id IS NOT NULL")
        es_rows=[]
    
        for row in rows:
            try:
                # Convert
                es_row = {}
                es_row["starfire_incident_id"] = float(row["starfire_incident_id"])
                es_row["incident_datetime"] = row["incident_datetime"] 
                es_row["incident_classification"] = row["incident_classification"]
                es_row["incident_borough"] = row["incident_borough"]
                es_row["engines_assigned_quantity"] = row["engines_assigned_quantity"]
                es_row["incident_response_seconds_qy"] = row["incident_response_seconds_qy"]
                es_row["valid_incident_rspns_time_indc"] = row["valid_incident_rspns_time_indc"]
    
            except Exception as e:
                print (f"Error!: {e}, skipping row: {row}")
                continue
            
            es_rows.append(es_row)
            record_count +=1
        
        
        bulk_upload_data = ""
        for line in es_rows:
            print(f'Handling row {line["starfire_incident_id"]}')
            action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + str(line["starfire_incident_id"]) + '"}}'
            data = json.dumps(line)
            bulk_upload_data += f"{action}\n"
            bulk_upload_data += f"{data}\n"
    
    
        try:
            resp = requests.post(f"{ES_HOST}/_bulk", data=bulk_upload_data,auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD), headers = {"Content-Type": "application/x-ndjson"})
            resp.raise_for_status()
            print ('Done')
                
        except Exception as e:
            print(f"Failed to insert in ES: {e}")
    
    print(f"Total number of rows: {record_count}")
