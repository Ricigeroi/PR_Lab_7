import json_writer
import homework
import in_class


url = "https://999.md/ru/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"

# Function call
links = in_class.parse(url, 1)
json_writer.write(links, "links.json")

info = homework.extract_info(links)
json_writer.write(info, "info.json")



