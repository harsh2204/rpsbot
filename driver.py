class Bot:
    """Basic bot class to wrap bot functions"""
    def __init__(self, name, code=None):
        """
name should be a unique identifier and must be a readable
filename if code is not specified
"""
        self.name = name
        if code is None:
            self.load_code()
        else:
            self.code = code

        self.reset()

    def __eq__(self, other):
        return self.name == other.name

    def get_move(self, input):
        """Get the next move for the bot given input
input must be "R", "P", "S" or ""
"""
        self.scope["input"] = input
        # self.scope["output"] = ''
        if self._code is None:
            self.compile_code()        
        exec(self._code, self.scope)        
        self.output = self.scope["output"]
        return self.output

    def compile_code(self):
        self._code = compile(self.code, '<string>', 'exec')

    def reset(self):
        """Resets bot for another round.  This must be called before trying
to pass the bot between workers, or you may see obscure errors from failures
to pickle the bots scope dictionary."""
        self.scope = dict()

        # this will hold compiled code, but it apparently can't be
        # pickled? so we'll have to do it later.  XXX check into this
        self._code = None

    def load_code(self):
        """Load bot code from the file specified by the name attribute"""
        f = open(self.name, "r")
        self.code = f.read()
        f.close()