# OKE Dataset Analysis
This repository provides four different analyses for the OKE Dataset introduced in Tufek Ozkaya et al. (2023). 

# Motivation
The motivation of the analyses described below is to:
1. Detect inconsistencies among annotators of the dataset and highlight consistency of the keywords in [consistency analysis](#1-consistency-analysis)
2. See the distributions of the annotated entities among the companion specifications of OPC UA and extract correlation between these specifications in [entity distribution analysis](#2-entity-distribution-analysis)
3. Just by using the annotated entities, and their frequencies, generating heatmap(s) to compute similarity score between companion specifications in [common entity analysis](#3-common-entity-analysis)


# [Dataset](#dataset)
The OPC UA Knowledge Extraction (OKE) Dataset is a dataset specifically created for sentence classification, named entity recognition and disambiguation (NERD), and entity linking. To learn more about the dataset and download it, please visit this [link](https://doi.org/10.5281/zenodo.10284577) and get the latest version of it. After downloading the dataset, please make sure to place the files in the `/oke_dataset/excel/` directory before running the analysis scripts.

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

## Prerequisites

Make sure that you have `python >= 3.9` and install the `requirements.txt`:

```
pip install -r requirements.txt
```

> Make sure that you downloaded the data in put in the correct folder. For more details check [here](#dataset).


## [1. Consistency Analysis](#1-consistency-analysis)

#### Purpose
The aim of this analysis is to highlight keywords in 4 different categories and detect the consistency level. For the most conflicting keywords analysis: on one hand this would sheld light on patterns, or mistakes on annotations to help annotators improve the annotations; on the other hand, assuming annotations are correct, this results would indicate that annotation cannot be done on word-level and context must be considered as well.

* most used keywords
* most used keywords, filtered by inclusion threshold*
* keywords assigned to more than 2 categories
* most conflicting keyword**

***inclusion threshold**: Given a keyword, assume that it is seen `n` times in the specification. if it is annotated only a few times, and not annotated for the remaining, it will be discarded. This margin is determined by the `threshold` parameter.

**Here, most conflicting means that if keyword is assinged to more than 2 categories and those categories' rate is close to each other. for example, for a keyword annotated 10 times, if it is annotated 5 times as `runtime-only`, and 5 times as `information model keyword`. this is one of the most conflicting situations.


### Prerequisites to run this analysis
- **IMPORTANT**: Run the helper script as: ```python merge_all_specs.py``` which will combine all the samples in all the files into one file. Afterwards one is free to run any experiment described below.

### Running Options

1. Using all sentences in the dataset (unfiltered): ```python consistency_analysis.py```

2. Using single specification (default = all):  ```python consistency_analysis.py -s <specification>```  
    ```
    <specification> options: "all", "autoid", "iolink", "isa95", "machinetools", "machinevision1", "machinevision2", "packml", "padim", "profinet", "robotics", "uafx", "weihenstephan"
    ```


3. Using either only rule or non-rule sentences
    * only rules: ```python consistency_analysis.py -s autoid -f --only_rule_sentences```

    * only non-rules: ```python consistency_analysis.py -s autoid -f --only_non_rule_sentences```

4. Deciding on the threshold for the inclusion (default=0.9)*: ```python consistency_analysis.py -s autoid -f --only_non_rule_sentences --threshold 0.8```

* set output path: ```python consistency_analysis.py -s autoid -o test_output/```

*decreasing threshold is likely to lead to less keywords to be used during computation

### Outputs
`output/consistency_analysis/` contains the generated charts with a reasonable file naming strategy. (e.g., `all_mostcommonkeywords_unfiltered_threshold0.9_top20words.png`)

## [2. Entity Distribution Analysis](#2-entity-distribution-analysis)
#### Purpose
The aim of the entity distribution analysis:
1. to determine the distribution of entity counts in sentences for each entity category in each companion specification (datasheet)
2. to find the correlation between different companion specifications in terms of entity distribution.

### Prerequisites to run this analysis
None

### Running Options

1. Extraction the both distributions for all (or selected) entity categories in each companion specification and the heatmaps for rule sentences and non-rule sentences ```python entity_distribution_analysis.py --entity_name <entity_name>```

    ```
    <entity_name> options: "information_model", "relation", "constraint", "quotes", "number", "all"
    ```
  

### Outputs
- `output/entity_distribution_analysis/distribution_barchart/` contains the distribution charts of each entity of each datasheet where eah filename represents the datasheet (e.g., Robotics)
- `output/entity_distribution_analysis/distribution_heatmap/`
contains the heatmaps of the distribution correlation of each datasheet based on different entity categories where naming is as explicit as possible (e.g., `constraint_rule_sentence_heatmap.png`)

## [3. Common Entity Analysis](#3-common-entity-analysis)
#### Purpose

This analysis will produce four files, each of which contains a heatmap indicating the similarities of specifications based on each of the four following columns in the dataset. The columns are: "Information Model Keywords", "Constraint Keywords", "Relation Keywords" and "Runtime only".
#### Computation Steps:
1. Collect all the keywords from specified column across all the companion specifications.
2. For each comp specification, calculate a keyword frequency histogram over the set obtained in step #1.
3. Normalize these histogram vectors to have unit length.
4. Take cosine similarity (dot product) between these vectors.
5. Collect the pair-wise cosine similarities in a heatmap.

### Prerequisites to run this analysis
None

### Running Options
1. Using all sentences (unfiltered): ```python common_entity_analysis.py```

2. Using only rule sentences: ```python common_entity_analysis.py -f --only_rule_sentences```

3. Using only non-rule sentences: ```python common_entity_analysis.py -f --only_non_rule_sentences```

### Outputs

`output/common_entity_analysis/` contains the generated charts with a reasonable file naming strategy. (e.g., `common_entity_analysis_filtered_rules_const_keyword.png`)

## [4. Specification Analysis](#4-specification-analysis)

#### Purpose
This analysis will produce a single file that contains a heatmap indicating the similarities of specifications based on some columns (constraint keywords, relation keywords, runtime-only keywords) in the dataset. In the end, ideally, this analysis would help one with understanding the similarity based on the word occurrences.

### Prerequisites to run this analysis
None

### Running Options

1. Using all sentences (unfiltered): ```python specification_analysis.py```

2. Using only rule sentences: ```python specification_analysis.py -f --only_rule_sentences```

3. Using only non-rule sentences: ```python specification_analysis.py -f --only_non_rule_sentences```

4. overriding inclusion threshold for keywords (default=0.9)*: ```python specification_analysis.py -f --only_rule_sentences --threshold 0.8```

*for the definition of inclusion threshold, please check [consistency analysis](#1-consistency-analysis). decreasing threshold will likely to lead to less keywords to be used during computation

### Outputs

`output/specification_analysis/` contains the generated charts with a reasonable file naming strategy. (e.g., `specification_analysis_filtered_rules_threshold_0.9`)
# Dataset Citation

    @dataset{tufek_ozkaya_2023_10284578,
        author       = {Tufek Ozkaya, Nilay},
        title        = {OPC UA Knowledge Extraction (OKE) Dataset},
        month        = dec,
        year         = 2023,
        publisher    = {Zenodo},
        doi          = {10.5281/zenodo.10284577},
        url          = {https://doi.org/10.5281/zenodo.10284577}
    }
