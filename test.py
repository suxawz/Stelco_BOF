import json
import math
 
def replace_nan_with_none(obj):
    if isinstance(obj, dict):
        return {k: replace_nan_with_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none(item) for item in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj
 
# 示例JSON字符串
json_str = '{"a": 1, "b": null, "c": {"d": NaN, "e": 2}, "f": [3, NaN, 5]}'

 
# 解析JSON字符串
data = json.loads(json_str)
 
# 替换NaN为None
data = replace_nan_with_none(data)
 
# 将修改后的对象转换回JSON字符串
new_json_str = json.dumps(data)
 
print(new_json_str)