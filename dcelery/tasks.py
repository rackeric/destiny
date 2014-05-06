from firebase import FirebaseApplication, FirebaseAuthentication
from celery.decorators import task
from ansible import utils
import ansible.runner, json, os

@task()
def ansible_jeneric_testing(job_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    URL = 'https://deploynebula.firebaseio.com/external_data/'
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myExternalData.get(URL, job_id)

    myHostList = job['host_list'] +','
    myModuleName = job['module_name']
    if (job['module_args']): 
        myModuleArgs = job['module_args']
    else:
        myModuleArgs = ''
    myPattern = job['pattern']
    myRemoteUser = job['remote_user']
    myRemotePass = job['remote_pass']

    #myKeyFile = job['private_key_file']

    #tmpFile = open("/tmp/" + job_id, "w")
    #tmpFile.write(myKeyFile)
    #tmpFile.close()

    results = ansible.runner.Runner(
        pattern=myPattern,
        forks=10,
        module_name=myModuleName,
        module_args=myModuleArgs,
        remote_user=myRemoteUser,
        remote_pass=myRemotePass,
        host_list=myHostList
        #private_key_file='/tmp/keykey'
    ).run()

    # get it to a good format
    #data = json.loads(results)
    #data = json.dumps(results)

    # set status to COMPLETE
    myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))

    #if type(results) == dict:
    #    results = utils.jsonify(results)

    # post results to firebase
    myExternalData.post(job_id + '/returns', json.loads(results), {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
    #returns.patch(job_id + '/returns', json.dumps(results))
    return results



@task()
def ansible_jeneric(job_id, user_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + user_id
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/external_data/'
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myExternalData.get(URL, job_id)

    myHostList = job['host_list'] +','
    myModuleName = job['module_name']
    myModuleArgs = job['module_args']
    myPattern = job['pattern']
    myRemoteUser = job['remote_user']
    myRemotePass = job['remote_pass']

    runString = ""

    for arg in myHostList, myModuleName, myModuleArgs, myPattern, myRemoteUser, myRemotePass:
        if ( arg ):
            runString = runString + arg
    
    results = ansible.runner.Runner(
        pattern=myPattern,
        forks=10,
        module_name=myModuleName,
        module_args=myModuleArgs,
        remote_user=myRemoteUser,
        remote_pass=myRemotePass,
        host_list=myHostList,
    ).run()
    # run the ansible stuffs
    #results = ansible.runner.Runner(
    #    pattern=myHost, forks=10,
    #    module_name='command', module_args=myCommand,
    #).run()    

    # get it to a good format
    #data = json.loads(results)
    #data = json.dumps(results)

    # set status to COMPLETE
    myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))
    
    if type(results) == dict:
        results = utils.jsonify(results)
    
    # post results to firebase
    myExternalData.post(job_id + '/returns', results)
    #returns.patch(job_id + '/returns', json.dumps(results))
    return results



@task()
def ansible_command_run(job_id, user_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + user_id
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/external_data/'
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myExternalData.get(URL, job_id)

    myHost = job['host']
    myCommand = job['command']

    # run the ansible stuffs
    results = ansible.runner.Runner(
        pattern=myHost, forks=10,
        module_name='command', module_args=myCommand,
    ).run()    

    # get it to a good format
    #data = json.loads(results)
    #data = json.dumps(results)

    # set status to COMPLETE
    myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))
    
    # post results to firebase
    myExternalData.post(job_id + '/returns', json.dumps(results))
    #returns.patch(job_id + '/returns', json.dumps(results))

    return results

@task()
def ansible_ping(job_id, user_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + user_id
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/external_data/'
    myExternalData = FirebaseApplication(URL, authentication)
    
    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myExternalData.get(URL, job_id)

    # get host from job
    # NEEDS UPDATING FOR SPECIFICS
    myHost = job['host']

    # run the ansible stuffs
    results = ansible.runner.Runner(
        module_name='ping',
        module_args='',
        pattern=myHost,
        forks=10
    ).run()    

    # get it to a good format
    #data = json.loads(results)
    #data = json.dumps(results)

    # set status to COMPLETE
    other_result = myExternalData.patch(job_id, json.loads('{"status":"COMPLETE"}'))
    
    # post results to firebase
    #returns = FirebaseApplication('https://deploynebula.firebaseio.com/external_data/', authentication)
    myExternalData.post(job_id + '/returns', json.dumps(results))
    #returns.patch(job_id + '/returns', json.dumps(results))

    return results
    
