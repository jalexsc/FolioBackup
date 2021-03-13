import argparse
import pathlib
import json
import requests
import sys
from requests.exceptions import HTTPError
import time



#from folioclient.FolioClient import FolioClient

class backup:
    def __ini__(path,x_okapi_url, x_okapi_tenant, x_okapi_token):
        x_okapi_url = x_okapi_url
        x_okapi_tenant = x_okapi_tenant
        x_okapi_token = x_okapi_token
        content_type = "application/json"
        print('initializing Backup')
        #self.user = user
        #self.password = password
        #self.x_okapi_version = x-okapi-version
        #self.x_okapi_release = x-okapi-release
        #self.x_okapi_status = x-okapi-status

    def make_get(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file):
        try:
            pathPattern=pathPattern
            okapi_url=okapi_url
            json_file=json_file
            
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            #username="folio"
            #password="Madison"
            #payload = {'username': username, 'password': password}
            length="9999"
            #typein="General note Orders"
            ##fc="&metadata.createdByUserId='2bd750b9-1362-4807-bd73-2be9d8d63436'"
            start="0"
            #paging_q = f"?limit={length}#&offset={start}"
            #paging_q = f"/notes?query=type=="General note Orders""
            #paging_q = f"?limit={length}&query=type=={typein}"
            paging_q = f"?limit={length}"
            path = pathPattern+paging_q
            #data=json.dumps(payload)
            url = okapi_url + path
            req = requests.get(url, headers=okapi_headers,timeout=40)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))            
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
        else:
            if req.status_code != 201:
                print(req)
                print(req.encoding)
                #print(req.text)
                print(req.headers)
                if req.status_code==200:
                    archivo=open(json_file, 'w')
                    json_str = json.loads(req.text)
                    #total_recs = int(json_str["totalRecords"])
                    archivo.write(json.dumps(json_str, indent=2))
                    #archivo.write(json.dumps(json_str)+"\n")
                    #print('Datos en formato JSON',json.dumps(json_str, indent=2))
                    archivo.close()
                    print('Success!')
                elif req.status_code==500:
                    print(req.text)
                elif req.status_code==502:
                    print(req.text)
                elif req.status_code==504:
                    print(req.text)
                    
    def make_del(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file, schema,client):
        try:
            countrecord=0
            countdel=0
            countnodel=0
            deletedRecords=open(client+"_"+schema+"_recordDeleted.txt", 'w')
            Recordsnodeleted=open(client+"_"+schema+"_record_to_delete_not_found.txt", 'w')
            pathPattern=pathPattern
            okapi_url=okapi_url
            json_file=json_file
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            id=""
            paging_q="/"
            path = pathPattern+paging_q
            #data=json.dumps(payload)
            url = okapi_url + path
            d = open(json_file)
            data = json.load(d)
            tini=0
            for i in data[schema]:
                countrecord=+1
                id=i['id']
                po=i['poNumber']
                print("==================================")
                print("Record no: "+str(countrecord)+" searching POnumber:"+str(po)+"            id:"+id)
                url = okapi_url + path+id
                tini = time.perf_counter()
                req = requests.delete(url, headers=okapi_headers,timeout=40)
                tend = time.perf_counter()
                #print(req.status_code)
                #print(req.headers)
                #print(req.text)
                if req.status_code==404:
                    print("POnumber: "+str(po)+f" not found Deleting ({tini - tend:0.4f}) seconds")
                    deletedRecords.write("POnumber: "+str(po)+f" not found ({tini - tend:0.4f}) seconds \n")
                    countnodel=+1
                    print("==================================")
                elif req.status_code==204:
                    print("POnumber: "+str(po)+f" has been deleted (time in) { tini - tend: 0.4f}) seconds")
                    deletedRecords.write("POnumber: "+str(po)+f" has been deleted ({tini - tend: 0.4f}) seconds\n")
                    countdel=+1
                    print("==================================")
                    
            deletedRecords.close()
        
        except ValueError:
            print("General Error on DEL")

            
    def filebyline(filetoformat,schema,client):
        try:
            f = open(filetoformat)
            archivo=open(client+"_"+str(filetoformat)+"byline.json", 'w')
            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # Iterating through the json
            # list
            for i in data[schema]:
                print(i)
                a_line=str(i)
                archivo.write(a_line+"\n")
            print("file by line, ready")
            # Closing file
            f.close()
        except: 
            print("OOPS!! instance Error of File not found")
            
def Clients():
    try:
        # Opening JSON file
        dic=[]
        f = open("okapi_customers.json",)
        data = json.load(f)
        for i in data['okapi']:
            a_line=str(i)
            dic.append(i['name'])#+"- Version:"+['x-okapi-version']+"-Release: "+['x-okapi-release'])
        f.close()
        return dic
    except: 
        print("OOPS!! General error occurred in Clients")
        
def schemas():
        # Opening JSON file
        dic=[]
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            a_line=str(i)
            dic.append(i['name'])#+"- Version:"+['x-okapi-version']+"-Release: "+['x-okapi-release'])
        f.close()
        return dic

def get_one_schema(code_search):
    valor=[]
    try:
        #valor="0"
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                valor.append(i['pathPattern'])
                valor.append(i['schema'])
                break
        f.close()
        return valor
    except ValueError:
        print("schema does not found")
        return 0

        
def get_all_schemas(self,code_search):
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            valor=i['path']
            break
        f.close()
        return valor

def SearchClient(code_search):
        # Opening JSON file
        dic =dic= {}
        f = open("okapi_customers.json",)
        data = json.load(f)
        for i in data['okapi']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                 dic=i
                 del dic['name']
                 del dic['user']
                 del dic['password']
                 del dic['x_okapi_version']
                 del dic['x_okapi_status']
                 del dic['x_okapi_release']
                 break
        f.close()
        return dic
    
def main(opt):
    try:
        okapi=""
        tenant=""
        token=""
        filename=""
        client = {}
        print(Clients())
        print("Enter Customer name:")
        cuts_name = str(input())
        print(schemas())
        client=SearchClient(cuts_name)
        if len(client)>0:
            ale=str(cuts_name)
            okapi=str(client.get('x_okapi_url'))
            tenant=str(client.get('x_okapi_tenant'))
            token=str(client.get('x_okapi_token'))
            print("Enter schema name:")
            sn = input()
            print("searching the path in setting file...")
            schema_name=str(sn)
            paths=get_one_schema(schema_name)
            if len(paths)>0:
                print("the path has been found "+schema_name)
                pathschema=paths[0]
                nameschema=paths[1]
                if opt==1:
                    filename=str(ale)+"_"+str(sn)+".json"
                    a=backup()
                    backup.make_get(pathschema,okapi,tenant,token,filename)
                    #backup.filebyline(filename,nameschema,ale)
                elif opt==4:
                    tic = time.perf_counter()
                    filename=ale+"_"+str(sn)+".json"
                    print("is it the JSON file name:"+filename+" ?")
                    a=backup()
                    backup.make_del(pathschema,okapi,tenant,token,filename,nameschema,ale)
                    toc = time.perf_counter()
                    print(f"Deleting time in {toc - tic:0.4f} seconds")
            else:
                print("the path has not been found "+schema_name)
                sys.exit()
        else:
            print("Customer does not exist in the okapi file, try again the okapi customer should be include in okapi file")
    except ValueError:
        print("Main Error"+str(ValueError))        

    #with open(args.settings_file) as settings_file:
    #    configuration = json.load(settings_file)

    #if args.function == "backup":
    #    print("Backup")
    #    backup = Backup(folio_client, args.from_path, args.set_name)
    #    backup.backup(configuration)
    #if args.function == "restore":
    #    print("Restore")
    #    restore = Restore(folio_client, args.from_path, args.set_name)
    #    restore.restore(configuration)
    #if args.function == "purge":
    #    print("purge")
    #    purge = Purge(folio_client, args.from_path, args.set_name)
    #    purge.purge(configuration)

    

if __name__ == "__main__":
    """This is the Starting point for the script"""
    print("MENU")
    print("1. GET"+"\n"+"2. POST"+"\n"+"3.PUT"+"\n"+"4.DEL")
    option = int(input())
    main(option)
