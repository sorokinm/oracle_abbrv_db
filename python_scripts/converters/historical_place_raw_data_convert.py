

def get_list_from_csv(csv):
    return csv.strip()[:-1].split(',')

raw_data = open("../../csvs/historical_places.raw.text.data", encoding="utf-8")
csv_history_places_file = open("../../csvs/historical_places.csv", "a+")
current_tag = ''
for line in raw_data:
    csv_items = get_list_from_csv(line)
    if len(csv_items) == 1:
        current_tag = csv_items[0]
        continue
    tagged_csv = ','.join(csv_items) + "," + current_tag + ",\n"
    csv_history_places_file.write(tagged_csv)
raw_data.close()
csv_history_places_file.close()


