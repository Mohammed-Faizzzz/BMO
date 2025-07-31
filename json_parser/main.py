
def parse(json_obj_path):
    json_obj = open(json_obj_path, "r")
    json_obj = json_obj.read()
    
    # check if it's a valid json_obj first
    if len(json_obj) < 2:
        print("Not a valid json object.")
        return
    start, end = json_obj[0], json_obj[len(json_obj)-1]
    if start != "{" or end != "}":
        print("Not a valid json object.")
        return
    

parse('./tests/step1/invalid.json')