import sys

def parse(json_obj_path):
    json_obj = open(json_obj_path, "r")
    json_obj = json_obj.read()
    json_string = json_obj.strip() # remove newline chars and stuff
    
    # Step 1: check if it's a valid json_obj first
    if not (json_string.startswith('{') and json_string.endswith('}')):
        print("Invalid JSON: Does not start with '{' or end with '}'")
        return
    
    # Step 2: simple key value pairs
    # remove braces
    content = json_string[1:-1].strip()
    
    # possible errors:
        # trailing commas
    if content[-1] == ",":
        print("Invalid JSON: Trailing Comma")
        return
    json_arr = content.split(",")
    for i in range(len(json_arr)):
        json_arr[i] = json_arr[i].strip()
    res = parse_kv_pairs(json_arr)
    print(res)

def parse_kv_pairs(arr):
    # each shld be split by colon with length 2
    res = {}
    for pair in arr:
        pair = pair.split(":")
        if len(pair) != 2:
            print("Invalid JSON: no colon")
            return
        key, val = pair[0].strip(), pair[1].strip()
        # both must be strings
        if not (key.startswith('"') and key.endswith('"')):
            print("Invalid JSON: Key is not a string")
            return
        
        val = parse_value(val)
        key = key[1:-1]
        res[key] = val
    return res
        
def parse_value(val):
    if val == "null":
        return None
    elif val == "true":
        return True
    elif val == "false":
        return False
    
    try:
        num = float(val)
        if num.is_integer():
            return int(num)
        return num
    except ValueError:
        pass
    
    if not (val.startswith('"') and val.endswith('"')):
        print("Invalid JSON: Invalid Value format")
        sys.exit(1)
    return val[1:-1]
    

parse('./tests/step3/valid.json')

parse('./tests/step3/invalid.json')
