from firebase import firebase, FirebaseApplication, FirebaseAuthentication
from celery import Celery, task
from django.http import HttpResponse
from firebase.jsonutil import JSONEncoder
import ansible.runner, ansible.utils
import json, os

celery = Celery('destinyCelery', broker='amqp://guest@localhost//')

def ansible_jeneric_view(request, user_id, project_id, job_id):
    ansible_jeneric.delay(user_id, project_id, job_id)
    return HttpResponse("ansible_jeneric task sent")

@celery.task
def ansible_jeneric(user_id, project_id, job_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + str(user_id)
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/external_data/'
    #myExternalData = FirebaseApplication(URL)
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job and set ansible options
    job = myExternalData.get(URL, job_id)

    # set vars from job data in firebase
    myHostList = job['host_list']
    myModuleName = job['module_name']
    myModuleArgs = job['module_args']
    myPattern = job['pattern']
    myRemoteUser = job['remote_user']
    myRemotePass = job['remote_pass']
    myProjectID = job['project_id']

    # set and get Ansible Project Inventory
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + myProjectID
    job = myExternalData.get(URL, 'inventory')

    # creating Ansible Inventory based on host_list
    myInventory = ansible.inventory.Inventory(myHostList)

    # set Host objects in Inventory object based on hosts_lists
    for key, host in job.iteritems():
        if host['name'] in myHostList:
            tmpHost = myInventory.get_host(host['name'])
            tmpHost.set_variable("ansible_ssh_host", host['ansible_ssh_host'])
            tmpHost.set_variable("ansible_ssh_user", host['ansible_ssh_user'])
            tmpHost.set_variable("ansible_ssh_pass", host['ansible_ssh_pass'])

 
    # run ansible module
    results = ansible.runner.Runner(
        pattern=myPattern,
        forks=10,
        module_name=myModuleName,
        module_args=myModuleArgs,
        #remote_user=myRemoteUser,
        #remote_pass=myRemotePass,
        inventory=myInventory,
    ).run()
    
    # set status to COMPLETE
    myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))

    # jsonify the results
    json_results = ansible.utils.jsonify(results)

    #
    # HELP! can't get a proper json object to pass, but below string works
    #
    myExternalData.post(job_id + '/returns', json_results)
    #myExternalData.patch(job_id + '/returns', json.loads('{"contacted": {"Cloud-Server-13": {"changed": true, "cmd": ["hostname"], "delta": "0:00:00.002057", "end": "2014-05-08 04:01:49.692771", "invocation": {"module_args": "hostname", "module_name": "command"}, "rc": 0, "start": "2014-05-08 04:01:49.690714", "stderr": "", "stdout": "cloud-server-13"}, "Cloud-Server-14": {"changed": true, "cmd": ["hostname"], "delta": "0:00:00.001994", "end": "2014-05-08 04:01:49.449724", "invocation": {"module_args": "hostname", "module_name": "command"}, "rc": 0, "start": "2014-05-08 04:01:49.447730", "stderr": "", "stdout": "cloud-server-14"}}, "dark": {}}'))

    return json_results
