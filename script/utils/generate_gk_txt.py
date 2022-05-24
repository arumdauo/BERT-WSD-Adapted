from pathlib import Path
import argparse

'''
    Generates a .txt file (corresponding to gold keys of the sense-annotated data 
    in corpus_dir_xml.) for the corpus_dir folder (input for “prepare_dataset” function).
    
        - corpus_dir_xml:   absolute path to .xml file generated in 
                            "generate_xml_adding_pos".
        
        - gold_keys_txt:    absolute path to .txt file to generate.
'''
def main():
    
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument(
        "--corpus_dir_xml_file",
        type = str,
        required = True,
        help = "Path to .xml file to generated"
               "in generate_xml_adding_pos.py"
    )
    parser.add_argument(
        "--gold_keys_txt_file",
        type = str,
        required = True,
        help = "Path to .txt file to generate"
    )
    args = parser.parse_args()
    corpus_dir_xml = Path(args.corpus_dir_xml_file)
    gold_keys_txt = Path(args.gold_keys_txt_file)
    
    id_list = []
    lemmas_list = []
    with open(corpus_dir_xml, "r") as file:
        text = file.read()
        lines_list = text.split("\n")
        for line in lines_list:
            if "instance id" in line:
                token_list = line.split()
                for w in token_list:
                    if "id=" in w:
                        word = w.replace("id=\"", "")
                        word = word.replace("\"", "")
                        id_list.append(word)
                    if "lemma" in w:
                        word = w.replace("lemma=", "")
                        word = word.replace("\"", "")
                        lemmas_list.append(word)
    with open(gold_keys_txt, "w") as file:
        text = ""
        for l_id, l_lemma in zip(id_list, lemmas_list):
            text += l_id + " " + l_lemma + "%" + "\n"
        file.write(text)
        
if __name__ == '__main__':
    main()
            
