import requests
import sys, os

class Translate:
    def __init__(self,path, namespace, auth):
        self.path = path
        self.namespace = namespace
        self.auth = auth
        self.json = None
        self.name = None
        self.env = None
        self.port = None
        self.vol = None
        self.labels = None
    def pull_data(self):
        r = requests.get('http://www.google.com')
        #r = requests.get(self.path, auth=self.auth)
        #if(r.status_code == 200):
            #print(r.json())
            #self.json = r.json()
    def parse_data(self):
        #Smart code from RancherDeploy
        '''
        c_json = self.json
        self.name = c_json['name']
        self.image = c_json['launchConfig']['imageUuid']
        self.ports = c_json['launchConfig'].get('ports', [])
        self.env = c_json['launchConfig'].get('environment', {})
        self.labels = c_json['launchConfig'].get('labels', {})
        self.vol = c_json?
        '''
        self.name = 'example'
        self.image = 'rancher/hello-world'
        self.env = {'env_var': 'val'}
        self.port = [{'containerPort': '80', 'hostPort' : '4000', 'protocol': 'TCP'}]
        #self.vol = Gotta read an example file
        self.labels = {'label': 'val'}
    def write_yaml(self):
        f = open('translations/'+self.name+'.yaml', 'w')
        f.write('---\napiVersion: apps/v1\nkind: Deployment' + '\n') #For the time only deployments
        f.write('metadata:\n  name: ' + self.name + '\n')
        f.write('  labels:\n')
        for i, j in self.labels.items():
            f.write('    ' + i +': '+j+ '\n')
        f.write('spec:\n  selector:\n    matchLabels:\n')
        for i, j in self.labels.items():
            f.write('      '+ i + ': ' + j + '\n')
        f.write('  replicas: 1\n  template:\n    metadata:\n      labels:\n')
        for i, j in self.labels.items():
            f.write('        '+ i + ': ' + j + '\n')
        f.write('    spec:\n      containers:\n      - name: ' + self.name + '\n')
        f.write('        image: ' + self.image + '\n')
        f.write('        ports\n')
        for item in self.port:
            iteration = 0
            for i, j in item.items():
                if(iteration ==0):
                    f.write('        - ' + i + ': ' + j + '\n')
                else:
                    f.write('          ' + i + ': ' + j + '\n')
                iteration +=1
              
        #Ports
        f.write('        env:\n')
        for i, j in self.env.items():
            f.write('        - name: ' + i + '\n')
            f.write('          value: ' + j + '\n')
        f.close()
#Eventually args
def main():
    path = "P"
    namespace = 'test'
    username = 'username'
    password = 'password'
    #path = sys.argv[1]
    #namespace = sys.argv[2]
    #username = sys.argv[3]
    #password = sys.argv[4]
    rancher_auth = (username, password)
    t = Translate(path, namespace, rancher_auth)
    t.pull_data()
    t.parse_data()
    #st.ensure_dir()
    t.write_yaml()

if __name__ == "__main__":
    main()
    
#Need to login with credentials this time --> See rancher deploy
    #https://github.com/DeluxeCorporation/RancherDeploy/blob/master/RancherDeploy/RancherDeploy_CLI.py

''' Todo:
Vols not right - Fix looking at api/actual yamls - write conditionals for when does not exist
No evidence api calls work
None of this creates load balancers, services, pods, or volumes. Additionally I suspect it processes multi apps badly
It might make sense for this script to make a folder for its namespace? Or maybe that happens in ansible
Namespaces not handled 
'''
'''
Ordered List
1) Run code and kubectl resulting yaml
2) Test code from ansible
3) Try a run on an actual target
4) Make volume adjustments/conditionals for saftey
5) Do some type safe stuff to look for Deployment, Service, Pod, Loadbalancers, and meeting volume claims
6) Think about secrets, commands, etc
-- After this is complete then transfer entire dev stack and troubleshoot errors
7) Create collections of files based on 5) and run kubectl recursivly agains them
8) Alter script to move resulting script into a helm deployment (ansible)
9) Read up on helm templating
10) Exectre helm templating script
'''



        
