
"""
    Useful for comparing results (predictions) obtained in the last step.
    
    Assigns random gold keys to the gold keys .txt file.
       - csv_file:       absolute path to .csv file obtained from the “prepare_dataset” step.
       
       - output_file:    absolute path to gold keys .txt file with no annotated sense.
"""

import csv
import random

def generate_random_gk_assignement(csv_file, output_file):
    
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        with open(output_file, 'w', encoding='utf-8') as txt_f:
            csv_reader = csv.reader(csv_f)
            for row in csv_reader:
                if "id" not in row:
                    txt_f.write(row[0] + " ")
                    gold_keys = row[2]
                    gold_keys = gold_keys.replace("[", "")
                    gold_keys = gold_keys.replace("]", "")
                    gold_keys = gold_keys.replace(",", "")
                    gold_keys = gold_keys.replace("\'", "")
                    gold_keys_list = gold_keys.split()
                    random_gold_key = random.choices(gold_keys_list, k=1)
                    random_gold_key = str(random_gold_key)
                    random_gold_key = random_gold_key.replace("[", "")
                    random_gold_key = random_gold_key.replace("]", "")
                    random_gold_key = random_gold_key.replace("\'", "")
                    txt_f.write(random_gold_key)
                    txt_f.write("\n")