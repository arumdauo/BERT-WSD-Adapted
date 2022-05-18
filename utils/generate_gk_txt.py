
'''
    Generates a .txt file (corresponding to gold keys of the sense-annotated data 
    in corpus_dir_xml.) for the corpus_dir folder (input for “prepare_dataset” function).
    
        - corpus_dir_xml:   absolute path to .xml file generated in 
                            "generate_xml_adding_pos".
        
        - gold_keys_txt:    absolute path to .txt file to generate.
'''
def generate_gk_file(corpus_dir_xml, gold_keys_txt):
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
            
                