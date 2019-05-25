
from hackathon.mod_codesubmission.stdio import stdoutIO


def _exec_untrusted(code_body, **kwargs):

    with stdoutIO() as s:
        try:
            code = compile(code_body, "<string>", "exec")
            exec(code)
            result_text = s.getvalue()
        except Exception as e:
            result_text = 'Code does not work! Error is : ', e

    return result_text


def exec_untrusted(code_body, **kwargs):
    return _exec_untrusted(code_body, **kwargs)
