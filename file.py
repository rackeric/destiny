import ast
from ansible import utils
from firebase import firebase, FirebaseApplication, FirebaseAuthentication
from celery import Celery
from celery import task
import ansible.runner, json, os
from django.http import HttpResponse
from firebase.jsonutil import JSONEncoder

celery = Celery('file', broker='amqp://guest@localhost//')

@celery.task
def ansible_jeneric(job_id, user_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + user_id
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/external_data/'
    #myExternalData = Firebase(URL)
    #myExternalData = FirebaseApplication(URL)
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myExternalData.get(URL, job_id)

    myHostList = job['host_list']
    myModuleName = job['module_name']
    myModuleArgs = job['module_args']
    myPattern = job['pattern']
    myRemoteUser = job['remote_user']
    myRemotePass = job['remote_pass']

    myInventory = ansible.inventory.Inventory(myHostList)
 
    results = ansible.runner.Runner(
        pattern=myPattern,
        forks=10,
        module_name=myModuleName,
        module_args=myModuleArgs,
        remote_user=myRemoteUser,
        remote_pass=myRemotePass,
        inventory=myInventory,
    ).run()
    
    # get it to a good format
    #data = json.loads(results)
    #data = json.dumps(results)

    # set status to COMPLETE
    myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))

    #json_results = ansible.utils.jsonify(results)
    #loads_results = json.loads(json_results)
    #loads_results = json.dumps(results)
    #print loads_results
    json_results = ansible.utils.jsonify(results)

    #myJson = firebase.JSONEncoder(results)
    #new_results = myJson.encode()
    
    # post results to firebase
    #myExternalData.post(job_id + '/returns', unescape(json.loads(json_results)))
    #myExternalData.post(job_id + '/returns/', results.decode('string-escape'))
    #myExternalData.post(job_id + '/returns/', ast.literal_eval(json.loads(json_results)))
    #data = json.dumps(results, cls=JSONEncoder)

    myExternalData.post(job_id + '/returns', json.loads(json_results))
    #myExternalData.post(job_id + '/returns', firebase.json.loads(results))
    #myExternalData.put(job_id + '/returns', json.loads('{"contacted": {"162.242.225.175": {"changed": false, "invocation": {"module_args": "", "module_name": "ping"}, "ping": "pong"}}, "dark": {}}'), connection=None)

    #myExternalData.patch(job_id + '/returns', json.loads('{"contacted": {"Cloud-Server-13": {"changed": true, "cmd": ["hostname"], "delta": "0:00:00.002057", "end": "2014-05-08 04:01:49.692771", "invocation": {"module_args": "hostname", "module_name": "command"}, "rc": 0, "start": "2014-05-08 04:01:49.690714", "stderr": "", "stdout": "cloud-server-13"}, "Cloud-Server-14": {"changed": true, "cmd": ["hostname"], "delta": "0:00:00.001994", "end": "2014-05-08 04:01:49.449724", "invocation": {"module_args": "hostname", "module_name": "command"}, "rc": 0, "start": "2014-05-08 04:01:49.447730", "stderr": "", "stdout": "cloud-server-14"}}, "dark": {}}'))

    #returns.patch(job_id + '/returns', json.dumps(results))
    return json_results

def ansible_jeneric_view(request, job_id, user_id):
    ansible_jeneric.delay(job_id, user_id)
    return HttpResponse("ansible_jeneric task sent")

