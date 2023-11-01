import json


def write(input, filename):

    json_data = json.dumps(input, indent=2, ensure_ascii=False)

    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
            print(f"Data saved to {filename}")

    except IOError as e:
        print(f"Error writing to {filename}: {e}")
