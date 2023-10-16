import json


def write(input, fileName):

    json_data = json.dumps(input, indent=2, ensure_ascii=False)

    try:
        with open(fileName, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
            print(f"Links saved to {fileName}")

    except IOError as e:
        print(f"Error writing to {fileName}: {e}")
