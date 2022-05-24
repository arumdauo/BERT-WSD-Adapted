# BERT-WSD-Adapted

Project adapted from [EMNLP-Findings 2020] Adapting BERT for Word Sense Disambiguation with Gloss Selection Objective and Example Sentences

## Arco, GVP datasets and pre-trained models

Arco, GVP datasets are available [here](https://1drv.ms/u/s!AgP7ssohTT10axaQj8vHg832WSk?e=a3mkRC). <br />
Pre-trained model is available [here](https://1drv.ms/u/s!AgP7ssohTT10gR3TDqI6_9dNltlu?e=ySZ0B1).

## Dataset generation

### Arco entities encoding in .xml file

Usage:
```
python script/utils/generate_xml_adding_pos.py --arco_concepts_instances_txt ARCO_CONCEPTS_INSTANCES_TXT
                                               --corpus_dir_xml_file CORPUS_DIR_XML_FILE
                                               --random_number RANDOM_NUMBER
arguments:
 --arco_concepts_instances_txt ARCO_CONCEPTS_INSTANCES_TXT
                                                            Path to the file "arco_getty_aat_3.txt" (available in data folder),
                                                            containing all the ArCo entities generating ambiguos links to AAT concepts.
 --corpus_dir_xml_file CORPUS_DIR_XML_FILE
                                                            Path to .xml file to generate.
 --random_number RANDOM_NUMBER
                                                            Number of ArCo entities to encode.
```

### Gold keys .txt file

Usage:
```
python script/utils/generate_gk_txt.py --corpus_dir_xml_file CORPUS_DIR_XML_FILE
                                       --random_number RANDOM_NUMBER
arguments:
 --corpus_dir_xml_file CORPUS_DIR_XML_FILE
                                            Path to .xml file generated in previous step generate_xml_adding_pos.py                             
 --gold_keys_txt_file GOLD_KEYS_TXT_FIle
                                            Path to .txt gold keys file to generate                                                         
```

## Dataset preparation

### Training dataset

Usage:
```
python script/prepare_dataset.py --corpus_dir CORPUS_DIR 
                                 --output_dir OUTPUT_DIR
                                 --AAT_dataset_path AAT_DATASET_PATH
arguments:
 --corpus_dir CORPUS_DIR 
                                      Path to directory consisting of one .xml file and one .txt
                                      file, corresponding to the sense-annotated data and its
                                      gold keys respectively.                             
 --output_dir OUTPUT_DIR
                                      Path to output directory where the .csv file will be written.    
 --AAT_dataset_path AAT_DATASET_PATH 
                                      Path to the file "aat_dataset.xlsx" (available in data folder),
                                      containing AAT concepts dataset.
```

Example:
```
python script/prepare_dataset.py \
    --corpus_dir "data/corpus/corpus_dir_random" \
    --output_dir "data/train" \
```

### Test dataset

Usage:
```
python script/prepare_dataset.py --corpus_dir CORPUS_DIR 
                                 --output_dir OUTPUT_DIR
                                 --AAT_dataset_path AAT_DATASET_PATH
arguments:
 --corpus_dir CORPUS_DIR 
                                      Path to directory consisting of one .xml file and one .txt
                                      file, corresponding to the sense-annotated data and its
                                      gold keys respectively.                             
 --output_dir OUTPUT_DIR
                                      Path to output directory where the .csv file will be written.    
 --AAT_dataset_path AAT_DATASET_PATH 
                                      Path to the file "aat_dataset.xlsx" (available in data folder),
                                      containing AAT concepts dataset.
```

Example:
```
python script/prepare_dataset.py \
    --corpus_dir "data/corpus/corpus_dir_for_test_1" \
    --output_dir "data/data_for_test" \
```

## Fine-tuning BERT

### Training

Usage:
```
python script/run_model.py --do_train --train_path TRAIN_PATH
                           --model_name_or_path MODEL_NAME_OR_PATH
                           --overwrite_output_dir
                           --output_dir OUTPUT_DIR
                           [--evaluate_during_training]
                           [--eval_path EVAL_PATH]
                           [--per_gpu_train_batch_size PER_GPU_TRAIN_BATCH_SIZE]
                           [--gradient_accumulation_steps GRADIENT_ACCUMULATION_STEPS]
                           [--learning_rate LEARNING_RATE]
                           [--num_train_epochs NUM_TRAIN_EPOCHS]
                           [--logging_steps LOGGING_STEPS] 
                           [--save_steps SAVE_STEPS]

arguments:
  --do_train                              Whether to run training on train set.
  --train_path TRAIN_PATH
                                          Path to training dataset (.csv file).
  --model_name_or_path MODEL_NAME_OR_PATH
                                          Path to pre-trained model.
  --overwrite_output_dir 
                                          Wheter to overwrite output_dir.
  --output_dir OUTPUT_DIR
                                          The output directory where the model predictions and
                                          checkpoints will be written.
  --evaluate_during_training
                                          Run evaluation during training at each logging step.
  --eval_path EVAL_PATH
                                          Path to evaluation dataset (.csv file).
  --per_gpu_train_batch_size PER_GPU_TRAIN_BATCH_SIZE
                                          Batch size per GPU/CPU for training.
  --gradient_accumulation_steps GRADIENT_ACCUMULATION_STEPS
                                          Number of updates steps to accumulate before
                                          performing a backward/update pass.
  --learning_rate LEARNING_RATE
                                          The initial learning rate for Adam.
  --num_train_epochs NUM_TRAIN_EPOCHS
                                          Total number of training epochs to perform.
  --logging_steps LOGGING_STEPS
                                          Log every X updates steps.
  --save_steps SAVE_STEPS
                                          Save checkpoint every X updates steps.
```

Example:
```
python script/run_model.py \
    --do_train \
    --train_path "data/test/test1train/train2-3-4-5-6.csv" \
    --model_name_or_path "data/model_italian_xxl" \
    --overwrite_output_dir \
    --output_dir "data/model_italian_xxl" \
    --per_gpu_train_batch_size 8 \
    --gradient_accumulation_steps 16 \
    --learning_rate 2e-5 \
    --num_train_epochs 4 \
    --logging_steps 1000 \
    --save_steps 1000
```


## Evaluation

### Generate predictions

Usage:
```
python script/run_model.py --do_eval --eval_path EVAL_PATH
                           --model_name_or_path MODEL_NAME_OR_PATH
                           --overwrite_output_dir
                           --output_dir OUTPUT_DIR
                           
arguments:
  --do_eval                               Whether to run test on test set.
  --train_path TRAIN_PATH
                                          Path to test dataset (.csv file).
  --model_name_or_path MODEL_NAME_OR_PATH
                                          Path to pre-trained model.
  --overwrite_output_dir 
                                          Wheter to overwrite output_dir.
  --output_dir OUTPUT_DIR
                                          The output directory where the model predictions and
                                          checkpoints will be written.
```

Example:
```
python script/run_model.py \
    --do_eval \
    --eval_path "data/test/test1train/test1.csv" \
    --model_name_or_path "data/model_italian_xxl" \
    --overwrite_output_dir \
    --output_dir "data/model_italian_xxl" \
```

## Scoring

Usage:
```
java Scorer GOLD_KEYS PREDICTIONS

arguments:
            GOLD_KEYS    Path to gold key file
            PREDICTIONS  Path to predictions file
```

Example:
```
java Scorer data/corpus/corpus_dir_1_sample/corpus_dir_1_sample.gold.key.txt \
            data/model_italian_xxl/corpus_dir_1_sample_predictions_100.txt
```

## References

Yap et al. "Adapting BERT for Word Sense Disambiguation with Gloss Selection Objective and Example Sentences" [EMNLP-Findings 2020]


