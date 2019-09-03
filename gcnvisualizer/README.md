# GCNVisualizer

This library is for visualizing for most effective input features.

## Requirements

* python >= 3.6.5
* matplotlib >= 2.0.0
* bioplot >= 0.0.2

## Installation

```shell
$ pip install -r requirements.txt
$ pip install -e .
```

## How to prepare input files

```shell
$ cd sample_chem/multimodal/
$ sh ./get_dataset.sh
$ sh init_sdf_profeat.sh
$ cd -
$ sh sample_chem/run_multimodal.sh
$ # or you can specify a task you want to run.
$ # python gcn.py --config ./sample_chem/multimodal/sample_config/multimodal_sdf_profeat.json train_cv
```

## How to use

```shell
$ gcnv -i hoge.pkl
```

# Reference

### Axiomatic Attribution for Deep Networks(2017)

* http://proceedings.mlr.press/v70/sundararajan17a/sundararajan17a.pdf

### An Investigation of Uncertainty and Sensitivity Analysis Techniques for Computer Models

* http://mycourses.ntua.gr/courses/CIVIL1086/document/WRM_Part_B_Makropoulos/iman1988.pdf~

### "Why Should I Trust You?": Explaining the Predictions of Any Classifier

* https://arxiv.org/pdf/1602.04938
* https://github.com/marcotcr/lime