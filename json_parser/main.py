
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
    # get the indices of the colons
    
    # possible errors:
        # trailing commas
    if content[-1] == ",":
        print("Invalid JSON: Trailing Comma")
        return
        # missing commas --> will automatically fail when parsing strings bc you have 2 back to back
        # newlines
        # no quotes for keys
        # parsing strings
        # assume colon is not problematic here
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
        if not (val.startswith('"') and val.endswith('"')):
            print("Invalid JSON: Val is not a string")
            return
        key = key[1:-1]
        val = val[1:-1]
        res[key] = val
    return res
        
    

parse('./tests/step2/valid.json')
# {"key": "value"}
parse('./tests/step2/valid2.json')
# {
#   "key": "value",
#   "key2": "value"
# }
parse('./tests/step2/invalid.json')
# {"key": "value",}
parse('./tests/step2/invalid2.json')
# {
#   "key": "value",
#   key2: "value"
# }