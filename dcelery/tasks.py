from firebase import FirebaseApplication, FirebaseAuthentication
from celery.decorators import task
import ansible.runner, json, os

@task()
def ansible_command_run(job_id, user_id):
    
    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + user_id
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/external_data/'
    myJob = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    other_result = myJob.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myJob.get(URL, job_id)

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
    other_result = myJob.patch(job_id, json.loads('{"status":"COMPLETE"}'))
    
    # post results to firebase
    myJob.post(job_id + '/returns', json.dumps(results))
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
    myJob = FirebaseApplication(URL, authentication)
    
    # update status to RUNNING in firebase
    other_result = myJob.patch(job_id, json.loads('{"status":"RUNNING"}'))
    
    # finally, get the actual job
    job = myJob.get(URL, job_id)

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
    other_result = myJob.patch(job_id, json.loads('{"status":"COMPLETE"}'))
    
    # post results to firebase
    #returns = FirebaseApplication('https://deploynebula.firebaseio.com/external_data/', authentication)
    myJob.post(job_id + '/returns', json.dumps(results))
    #returns.patch(job_id + '/returns', json.dumps(results))

    return results
    
