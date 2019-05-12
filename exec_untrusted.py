# This module might need change based on finalized requirements.

# Zope security imports
from AccessControl.ZopeGuards import get_safe_globals, safe_builtins
# Restricted Python imports
from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector
from stdio import stdoutIO


def _exec_untrusted(code_body, **kwargs):
    """ Sets up a sandboxed Python environment with Zope security in place.

    Calls func() in an sandboxed environment. The security mechanism
    should catch all unauthorized function calls (declared
    with a class SecurityManager).

    Security is effective only inside the function itself -
    The function security declarations themselves are ignored.

    @param code_body: Code String
    @param kwargs: Parameters delivered to func
    @return: Function return value
    """

    # Create global variable environment for the sandbox
    globals = get_safe_globals()
    globals['__builtins__'] = safe_builtins

    # Zope seems to have some hacks with guaded_getattr.
    # guarded_getattr is used to check the permission when the
    # object is being traversed in the restricted code.
    # E.g. this controls function call permissions.
    from AccessControl.ImplPython import guarded_getattr as guarded_getattr_safe

    globals['_getattr_'] = guarded_getattr_safe
    # globals['getattr'] = guarded_getattr_safe
    # globals['guarded_getattr'] = guarded_getattr_safe

    globals.update(kwargs)

    # Our magic code
    # The following will compile the parsed Python code
    # and applies a special AST mutator
    # which will proxy __getattr__ and function calls
    # through guarded_getattr

    # Here is a good place to break in
    # if you need to do some ugly permission debugging
    # if debug:
    #   pass # go pdb here

    with stdoutIO() as s:
        try:
            code = compile_restricted(code_body, "<string>", "exec")
            loc = {'_print_': PrintCollector, '_getattr_': getattr}
            exec(code, globals, loc)
            print(loc['_print']())
            result_text = s.getvalue()
        except Exception as e:
            result_text = 'Code does not work! Error is : ', e

    return result_text


def exec_untrusted(code_body, **kwargs):
    """ Sets up a sandboxed Python environment with Zope security in place. """
    return _exec_untrusted(code_body, **kwargs)

