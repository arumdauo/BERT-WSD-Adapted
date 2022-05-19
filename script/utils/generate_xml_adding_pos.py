
from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
import random

'''
    Generates an .xml file (corresponding to the sense-annotated data) 
    for the corpus_dir folder (input for “prepare_dataset” function).
    
        - arco_concepts_instances_txt:    absolute path to the file "arco_getty_aat_3.txt",
                                          containing all the ArCo entities generating 
                                          ambiguos links to AAT concepts.
         
        - corpus_dir_xml:                 absolute path to .xml file to generate.
        
        - random_num:                     the number of ArCo instances to encode in the .xml file.
'''
def generate_xml_adding_pos(arco_concepts_instances_txt, corpus_dir_xml, random_num): 
    
    arco_concepts_list = create_random_concepts_list(arco_concepts_instances_txt, random_num)
    arco_titles_list = create_arco_titles_list(arco_concepts_list)
    arco_concepts_for_output_list = create_arco_concepts_for_output_list(arco_concepts_list)
    initial_text = write_initial_text()
    concepts_text_list = []
    for a_t, a_c in zip(arco_titles_list, arco_concepts_for_output_list):
        if "Empty" in a_t:
            continue
        concept_text = write_concept(a_t, a_c, arco_concepts_instances_txt)
        concepts_text_list.append(concept_text)
    write_xml(initial_text, concepts_text_list, corpus_dir_xml)
    

'''
    Creates a list containing ArCo entities titles.
'''
def create_arco_titles_list(arco_concepts_list):
    arco_titles_list = []
    for a_c in arco_concepts_list:
        html_lines_count = 0
        html = urlopen(a_c)
        arco_html = html.read()
        soup = BeautifulSoup(arco_html, "html.parser") 
        text = soup.get_text().splitlines()
        for i, line in enumerate(text):
            if "rdfs:label" in line:
                titolo = text[i+1]
                arco_titles_list.append(titolo)
            if "Empty" in line:
                arco_titles_list.append("Empty")
            html_lines_count += 1
        if 4 < html_lines_count < 100:
            arco_titles_list.append("Empty")
    return arco_titles_list


'''
    Creates a list of random_num random concepts.
'''
def create_random_concepts_list(file, random_num):
    concepts_list = []
    concepts_list_random = []
    arco_concepts_list_random = []
    with open(file, 'r') as f:
        for line in f:
            if "MINING" in line:
                line = line.replace("MINING FROM:", "")
                line = line.replace("\n", "")
                line = "<" + line + ">"
                concepts_list.append(line)
    for i in range(random_num):
        random_concept = random.choice(concepts_list)
        concepts_list_random.append(random_concept)
    for el in concepts_list_random:
        el = 'http://dati.beniculturali.it/sparql?output=text%2Fhtml&query=DESCRIBE+'+el
        arco_concepts_list_random.append(el)
    return arco_concepts_list_random


'''
    Creates a list containing ArCo titles in the desired format.
'''
def create_arco_concepts_for_output_list(arco_concepts_list):
    arco_concepts_for_output_list = []
    for a_c in arco_concepts_list:
        a_c = a_c.replace('http://dati.beniculturali.it/sparql?output=text%2Fhtml&query=DESCRIBE+', '')
        a_c = a_c.replace('<', '')
        a_c = a_c.replace('>', '')
        arco_concepts_for_output_list.append(a_c)
    return arco_concepts_for_output_list


'''
    Writes the .xml file first part.
'''
def write_initial_text():
    text = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" + "\n" + "<corpus lang=\"it\" source=\"\">" + "\n"
    return text


'''
    Writes the .xml file middle part.
'''
def write_concept(arco_title, arco_concept, arco_concepts_instances_txt):
    c = -1
    instance_term_list = create_instance_terms_list(arco_concept, arco_concepts_instances_txt)
    
    arco_title_with_articles = add_articles(arco_title)
    nlp = spacy.load('it_core_news_sm')
    doc = nlp(arco_title_with_articles)
    title_token_pos_list = []
    for token in doc:
        title_token_pos_list.append(str(token))
        title_token_pos_list.append(token.pos_)
        title_token_pos_list.append(token.lemma_)
    lemmas_list = []
    arco_id = "<arco id=\"" + arco_concept + "\">"
    sentence_id = "<sentence id=\"" + arco_concept + "\">"
    
    tokens = arco_title.split()
    arco_title_mod = []
    for t in tokens:
        t = t.replace("(", "( ")
        t = t.replace(")", " )")
        t = t.replace(".", " .")
        t = t.replace(",", " ,")
        t = t.replace("\"", " \"")
        t = t.replace("<", " <")
        t = t.preplace(">", " >")
        if " " in t:
            t = t.split()
            for r in t:
                arco_title_mod.append(r)
        else:
            arco_title_mod.append(t)
    
    for t in arco_title_mod:
        if t.lower() in instance_term_list:
            c = c+1
            index = title_token_pos_list.index(t)
            pos = title_token_pos_list[index + 1]
            lemma_t = title_token_pos_list[index + 2]
            lemma = ("<instance id=\"" + arco_concept + "." + str(c) + "\" lemma=\"" + lemma_t +
                     "\" pos=\"" + pos + "\">" + t + "</instance>")
        else:
            if t in title_token_pos_list:
                index = title_token_pos_list.index(t)
                pos = title_token_pos_list[index + 1]
                lemma_t = title_token_pos_list[index + 2]
                lemma = "<wf lemma=\"" + lemma_t + "\" pos=\"" + pos + "\">" + t + "</wf>"
            else: # cases such as "d'altare"
               lemma = "<wf lemma=\"" + t + "\" pos=\"\">" + t + "</wf>"
        lemmas_list.append(lemma)
    text = arco_id + "\n" + sentence_id + "\n"
    for l in lemmas_list:
        text += l + "\n"
    text += "</sentence>" + "\n"
    text += "</arco>"
    return text

 
'''
    Writes the .xml file last part.
'''   
def write_xml(initial_text, concepts_text_list, corpus_dir_xml):
    with open(corpus_dir_xml, "w") as file:
        text = initial_text
        for t in concepts_text_list:
            text += t + "\n"
        text += "</corpus>"
        file.write(text)
        

'''
    Creates a list containing the terms in the instance (the ones getting ambiguous links).
'''        
def create_instance_terms_list(arco_concept, txt):
    instance_term_list = []
    text = open(txt, "r")
    text1 = text.read()
    lines_list = text1.split()
    for i, line in enumerate(lines_list):
        if arco_concept in line:
            index = i+1
            line = lines_list[index]
            while line != "*****************":
                index = index + 1
                line = lines_list[index]
                if line == "Term:":
                    parola = lines_list[index + 1]
                    if parola not in instance_term_list:
                        instance_term_list.append(parola)
    return instance_term_list


'''
    Adds articles before nouns placed at the beginning of the sentence.
'''
def add_articles(input_string):
    input_string = input_string.split()
    if len(input_string) > 1:
        first_word = input_string[0]
        if len(first_word) >= 3 and first_word[0].islower():
            if first_word[-1] == "a":
                input_string.insert(0, "la")
                input_string = add_articles_after_dash(input_string)
                input_string_txt = ' '.join(input_string)
            elif first_word[-1] == "o":
                input_string.insert(0, "il")
                input_string = add_articles_after_dash(input_string)
                input_string_txt = ' '.join(input_string)
            elif first_word[-1] == "e":
                input_string.insert(0, "le")
                input_string = add_articles_after_dash(input_string)
                input_string_txt = ' '.join(input_string)
            elif first_word[-1] == "i":
                input_string.insert(0, "i")
                input_string = add_articles_after_dash(input_string)
                input_string_txt = ' '.join(input_string)
            else:
                input_string = add_articles_after_dash(input_string)
                input_string_txt = ' '.join(input_string)
        else:
            input_string = add_articles_after_dash(input_string)
            input_string_txt = ' '.join(input_string)
    else:
        input_string_txt = ""
    return input_string_txt


'''
    Adds articles before nouns placed after a dash.
'''                       
def add_articles_after_dash(input_string):
    for i in range(len(input_string)):
        if input_string[i] == "-":
            word_after_dash = input_string[i+1]
            if len(word_after_dash) >= 3 and word_after_dash[0].islower():
                if word_after_dash[-1] == "a":
                    input_string.insert(i+1, "la")
                elif word_after_dash[-1] == "o":
                    input_string.insert(i+1, "il")
                elif word_after_dash[-1] == "e":
                    input_string.insert(i+1, "le")
                elif word_after_dash[-1] == "i":
                    input_string.insert(i+1, "i")
    return input_string   
    
    
