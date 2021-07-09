import json

def get_json_from_file(json_file):
    file_path = "data/raw/" + json_file + ".json"
    with open(file_path, "r") as r_file:
        json_content = json.load(r_file)
    return json_content # returns a list of dictionarys

def remove_excess_parts(raw_list_of_dict):
    har_list_of_dict = []
    keys_to_include = ["started_at", "ended_at", "start_station_id", "end_station_id"]
    for dict in raw_list_of_dict:
        new_dict = {}
        for key in dict.keys():
            if key in keys_to_include:
                new_dict[key] = dict[key]
        har_list_of_dict.append(new_dict)
    return har_list_of_dict

def reduce_timestamps(list_of_dict):
    for dict in list_of_dict:
        dict["started_at"] = dict["started_at"].split(".")[0]
        dict["ended_at"] = dict["ended_at"].split(".")[0]
    return list_of_dict

def save_harmonized(filename, harmonized_data):
    file_path = "data/harmonized/" + filename + ".json"
    with open(file_path, "w") as r_file:
        json.dump(harmonized_data, r_file)

def main():
    filename = "obs_2020-03"
    raw_data = get_json_from_file(filename)
    harmonized_data = reduce_timestamps(remove_excess_parts(raw_data))
    save_harmonized(filename, harmonized_data)

main()
