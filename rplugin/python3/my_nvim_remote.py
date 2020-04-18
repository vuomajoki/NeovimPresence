# this configures logging
# import presence_logging

import logging
import importlib
import presence_test
import presence_editor
import pynvim

log = logging.getLogger("presence")

@pynvim.plugin
class MyNvimRemote(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.editor = presence_editor.PresenceNvimEditor(self.nvim)

    @pynvim.function('MyRemoteFunction', sync=True)
    def remote_function(self, args):
        var = self.editor.nvim_function(args)
        return var
    
    @pynvim.function('MyRemoteFunctionAsync', sync=False)
    def remote_function_async(self, args):
        self.editor.nvim_async_function(args)
    
    @pynvim.function('MyRemoteFunctionTest', sync=True)
    def remote_function_test(self, args):
        return presence_editor.hello_editor()

    @pynvim.command('MyRemoteCommand', nargs='*', range='')
    def remote_command(self, args, range):
        buf = self.nvim.current.buffer
        length = self.nvim.request("nvim_buf_line_count", buf)
        log.info("length "+str(length))
        log.info(str(self.nvim.funcs.Tadaa()))
        log.info("and")
        log.info(str(self.nvim.request("nvim_call_function","Tadaa",[])))
        # self.nvim.current.line = ('Command with args: {}, range: {}'
        #                           .format(args, range))
        log.info("moi {}".format(self.nvim.current.line))
        return "hei"

    @pynvim.command('MyRemoteTest', nargs='*', range='')
    def remote_test(self, args, range):
        log.info("test works tadaa")
        log.info(presence_test.hello_presence())
        return presence_test.hello_presence()
   
    # This is important for initializing remote plugin
    @pynvim.command('MyRemoteInit', nargs='*', range='')
    def remote_init(self, args, range):
        log.info("Remote init")
    
    @pynvim.command('MyRemoteReload', nargs='*', range='')
    def remote_reload(self, args, range):
        log.info("reload")
        importlib.reload(presence_test)
        importlib.reload(presence_editor)

        # old neovim needs to be changes
        self.__init__(self.nvim)
    
    # @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    # def on_bufenter(self, filename):
    #     self.nvim.out_write('testplugin is in ' + filename + '\n')





