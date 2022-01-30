from typing import NamedTuple

def annotate(namespace):
    namespace["__annotations__"] = {"stda": int}

import types
x = types.new_class("El", (NamedTuple,), exec_body=annotate)
