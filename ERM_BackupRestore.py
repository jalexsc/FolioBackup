import argparse
import pathlib
import json
import requests
import sys
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
        pathPattern=pathPattern
        okapi_url=okapi_url
        json_file=json_file
        archivo=open(json_file+".json", 'w')
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        #username="folio"
        #password="Madison"
        #payload = {'username': username, 'password': password}
        perpage = 10
        page = 1
        paging_q = "?perPage={}&page={}"
        #length="9999"
        #start="0"
        #paging_q = f"?limit={length}&offset={start}"
        path = pathPattern+paging_q.format(perpage,page)
        #data=json.dumps(payload)
        url = okapi_url + path
        req = requests.get(url, headers=okapi_headers)
        if req.status_code != 201:

            print(req)
        
            print(req.encoding)
            #print(req.text)
            print(req.headers)
            response = json.loads(req.text)
            #total_recs = int(json_str["totalRecords"])
            #archivo.write(json.dumps(response, indent=4))
            #print('Datos en formato JSON',json.dumps(response, indent=2))
            #print('Datos en formato JSON',json.dumps(response))
            with open(json_file+".json", 'w+') as archivo:
            
                while len(response) == perpage:
                    page += 1
                    paging_q = "?perPage={}&page={}"
                    path = pathPattern+paging_q.format(perpage, page)
                    url = okapi_url + path
                    req = requests.get(url, headers=okapi_headers)
                    response = json.loads(req.text)
                    #archivo.write(json.dumps(response, indent=2))
                    archivo.write(json.dumps(response,indent=2))
                    #print('Datos en formato JSON',json.dumps(response, indent=2))
                    print('Datos en formato JSON',json.dumps(response))
                archivo.write(json.dumps(response, indent=2))
          
                
    

    def filebyline(filetoformat):
        f = open(filetoformat) 
        # returns JSON object as  
        # a dictionary 
        data = json.load(f)  
        # Iterating through the json 
        # list 
        for i in data['instances']: 
            print(i)
            a_line=str(i)
        print(scode)
        # Closing file 
        with open(filetoformat+"_by_line.json", "w") as write_file:
            json.dump(student, write_file)

        f.close() 
def Clients():
        # Opening JSON file
        dic=[]
        f = open("okapi_customers.json",) 
        data = json.load(f)  
        for i in data['okapi']:
            a_line=str(i)
            dic.append(i['name'])#+"- Version:"+['x-okapi-version']+"-Release: "+['x-okapi-release'])
        f.close()
        return dic

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
    try:
        valor="0"
        f = open("setting_data.json",) 
        data = json.load(f)  
        for i in data['settings']: 
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                valor=i['pathPattern']
                break                
        f.close()
        return valor
    except ValueError:
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

def test_a(filetoformat):
    try:
        valor="0"
        f = open(filetoformat,"r") 
        data = json.load(f)  
        for i in data['licenses']: 
            a_line=str(i)
            print(a_line)
        f.close()
        return valor
    except ValueError:
        return 0
  
def test(filetoformat):
    table = []
    with open(filetoformat, 'r') as f:
        for line in f:
            try:
                j = line.split('|')[-1]
                print(j)
                table.append(json.loads(j))
                
            except ValueError:
            # You probably have bad JSON
                continue


    for row in table:
        print(row)
    

def main():
    #test("licenses.json")
    client = {}
    print(Clients())
    print("Enter Customer name:")
    cuts_name = str(input())
    print(schemas())
    client=SearchClient(cuts_name)
    print("Enter schema name 'all' for fullbackup:")
    sn = input()
    print("searching the path...")
    if sn !="all":
        schema_name=str(sn)
        pathschema=get_one_schema(schema_name)
        if pathschema !=str(0):
            print("the path has been found "+pathschema)
        else:
            print("the path has been found "+pathschema)
            sys.exit()
    elif sn=="all":
        path=get_all()

    okapi=str(client.get('x_okapi_url'))
    tenant=str(client.get('x_okapi_tenant'))
    token=str(client.get('x_okapi_token'))
    filename=str(sn)
    a=backup()
            #(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file):
     
    #backup.make_get(pathschema,okapi,tenant,token,filename)
    backup.make_get(pathschema,okapi,tenant,token,filename)
   
    #backup.filebyline(filename)
   
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
    main()

