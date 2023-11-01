import json_writer
import homework
import in_class


url = "https://999.md/ro/list/real-estate/apartments-and-rooms"

# Function call
links = in_class.parse(url, 1)
json_writer.write(links, "links.json")

links = ['https://999.md/ro/83437037']
info = homework.extract_info(links)
json_writer.write(info, "info.json")
