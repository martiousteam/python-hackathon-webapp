
from hackathon.mod_codesubmission.stdio import stdoutIO
import os

def validate_code(code_body, **kwargs):
    if len(code_body) > 4000:
        return {'outcome': False, 'result': 'Code too long - limit to 4000 characters'}
    
    # check if code only contains allowed libraries
    
    return {'outcome': True, 'result': 'Success'}

def _exec_untrusted(code_body, **kwargs):

    with stdoutIO() as s:
        try:
            code = compile(code_body, "<string>", "exec")
            # os.chdir("/var/www/python/run/") # directory in which python code should run
            exec(code)
            # os.chdir("/var/www/python/run/") # directory in which python code should run
            result_text = {'outcome': True, 'result': s.getvalue().strip()}
        except Exception as e:
            result_text = {'outcome': False, 'result': 'Code does not work! Error is : ' + str(e).strip()}

    return result_text


def exec_untrusted(code_body, **kwargs):
    validation_result = validate_code(code_body, **kwargs)
    
    if validation_result['outcome'] == False:
        return validation_result
    
    return _exec_untrusted(code_body, **kwargs)

