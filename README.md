# OKE Dataset Analysis
This repository provides four different analyses for the OKE Dataset introduced in Tufek Ozkaya et al. (2023). 

# The Dataset
The OPC UA Knowledge Extraction (OKE) Dataset is a dataset specifically created for sentence classification, named entity recognition and disambiguation (NERD), and entity linking. To learn more about the dataset and download it, please visit this [link](https://zenodo.org/records/10284578) and get the latest version of it. After downloading the dataset, please make sure to place the files in the "./oke_dataset/excel/" directory before running the analysis scripts.

The files should appear in the following hierarchy:

```.
└── oke-dataset-analysis/
    ├── oke_dataset/
    │   ├── csv/
    │   │   ├── AutoId.csv
    │   │   └── ...
    │   └── excel/
    │       ├── AutoId.xlsx
    │       └── ...
    ├── output
    └── ...
```

# Usage

Make sure that you have `python >= 3.9` and install the `requirements.txt`. 

```
pip install -r requirements.txt
```

## 1. Specification Analysis
This analysis will produce a single file that contains a heatmap indicating the similarities of specifications based on some columns in the dataset. There are different running options:

- all sentences (unfiltered): ```python spec_analysis.py```

- only rule sentences: ```python spec_analysis.py -f --only_rule_sentences```

- only non-rule sentences: ```python spec_analysis.py -f --only_non_rule_sentences```

- overriding inclusion threshold for keywords (default=0.9)*: ```python spec_analysis.py -f --only_rule_sentences --threshold 0.8```

*decreasing threshold will likely to lead to less keywords to be used during computation


## 2. Keyword Analysis
This analysis will produce 4 different files of charts.
* most used keywords
* most used keywords, filtered by inclusion*
* keywords assigned to more than 2 categories
* most conflicting keyword**

*inclusion: Given a keyword, assume that it is seen `n` times in the specification. if it is annotated only a few times, and not annotated for the remaining. it will be discarded. this margin is determined by the `threshold` parameter.

**Here, most conflicting means that if keyword is assinged to more than 2 categories and those categories' rate is close to each other. for example, for a keyword annotated 10 times, if it is annotated 5 times as `runtime-only`, and 5 times as `information model keyword`. this is one of the most conflicting situations.

### How to Run

- IMPORTANT: Run the helper script as: ```python merge_all_specs.py``` which will combine all the samples in all the files into one file. Afterwards one is free to run any experiment described below.

- all sentences (unfiltered): ```python keyword_analysis.py``` --> this will take some time (up to 5 mins depending on the hardware).

* select a specification (default = all): ```python keyword_analysis.py -s autoid```  
        specification options: "all", "autoid", "iolink", "isa95", "machinetools", "machinevision1", "machinevision2", "packml", "padim", "profinet", "robotics", "uafx", and "weihenstephan"


* #### filter sentences given a selected specification
    * only rules: ```python keyword_analysis.py -s autoid -f --only_rule_sentences```

    * only non-rules: ```python keyword_analysis.py -s autoid -f --only_non_rule_sentences```

* overriding inclusion threshold for keywords (default=0.9)*: ```python keyword_analysis.py -s autoid -f --only_non_rule_sentences --threshold 0.8```

* set output path: ```python keyword_analysis.py -s autoid -o test_output/```

*decreasing threshold will likely to lead to less keywords to be used during computation

## 3. Entity Analysis
There are two aims of antity analysis:
(i) to determine the distribution of entity counts in sentences for each entity category in each companion specification (datasheet); (ii) to find the correlation between different companion specifications in terms of entity distribution.

In order to run entity analysis, the following command can be called. 

* extraction the both distributions for all (or selected) entity categories in each companion specification and the heatmaps for rule sentences and non-rule sentences ```python entity_analysis.py --entity_name <entity_name>```

  <entity_name> options: "information_model", "relation", "constraint", "quotes", "number", and "all". the default is "all".

There will be two output folders for this purpose: 
1.  `output/entity_analysis/distribution_barchart/`
this shows the distribution charts of each entity of each datasheet
2. `output/entity_analysis/distribution_heatmap/`
this involves the heatmaps of the distribution correlation of each datasheet based on different entity categories. 

## 4. Feature Analysis
This analysis will produce four files, each of which contains a heatmap indicating the similarities of specifications based on each of the four following columns in the dataset. The columns are: "Information Model Keywords", "Constraint Keywords", "Relation Keywords" and "Runtime only".
#### Computation Steps:
1. Collect all the keywords from specified column across all the companion specs.
2. For each comp spec, calculate a keyword frequency histogram over the set obtained in step #1.
3. Normalize these histogram vectors to have unit length.
4. Take cosine similarity (dot product) between these vectors.
5. Collect the pair-wise cosine similarities in a heatmap.
#### Running commands:
- all sentences (unfiltered): ```python feature_analysis.py```

- only rule sentences: ```python feature_analysis.py -f --only_rule_sentences```

- only non-rule sentences: ```python feature_analysis.py -f --only_non_rule_sentences```


# Dataset Citation

    @dataset{tufek_ozkaya_2023_10284578,
        author       = {Tufek Ozkaya, Nilay},
        title        = {OPC UA Knowledge Extraction (OKE) Dataset},
        month        = dec,
        year         = 2023,
        publisher    = {Zenodo},
        doi          = {10.5281/zenodo.10284578},
        url          = {https://doi.org/10.5281/zenodo.10284578}
    }
