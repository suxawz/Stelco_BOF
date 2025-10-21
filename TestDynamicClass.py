import pandas as pd

from Helper import *

from pathlib import Path
import json
import os

class MyClass:
    def __init__(self, **kwargs):
        #self.attributes = {}
        for key, value in kwargs.items():
            setattr(self, key, value)  # 使用setattr动态设置属性
            #self.attributes[key] = value  # 也可以存储在一个字典中
    def Add(self, **kwargs):
        #self.attributes = {}
        for key, value in kwargs.items():
            setattr(self, key, value)  # 使用setattr动态设置属性
            #self.attributes[key] = value  # 也可以存储在一个字典中
analysis = ["Al",6,"As",2]           

a = MyClass(C=1,AL=2,k=3)
a.Add(s=2,f=5,k=5)
json_data = json.dumps(a, default=lambda o: o.__dict__, indent=4)
print(json_data)