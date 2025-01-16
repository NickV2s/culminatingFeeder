import json

# list of integer & string
list_1 = [1, 2, 3, "four", "five"]
print(type(list_1))
print("Real List:", list_1)

# convert to Json
json_str = json.dumps(list_1)
# displaying
print(type(json_str))
print("Json List:", json_str)