import json
from general import format_multi_line

class AbstractProtocol:

    def __init__(self):
        self.__setCladdName()

    def toJSON(self):
        self.__setCladdName()
        def td(o):
            if type(o) == bytes : 
                return format_multi_line('', o)
            if isinstance(o, AbstractProtocol) :
                o.__setCladdName()
            return o.__dict__

        return json.dumps(self, 
            default=lambda o: td(o), 
            sort_keys=False, indent=4)

    def __setCladdName(self):
        self.className = type(self).__name__