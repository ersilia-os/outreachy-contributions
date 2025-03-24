# The Blood Brain Barrier Permeability Prediction Project (BBBP)
This Project aims to predict the ability of chemical compounds to cross the blood brain barrier based on their structural components using machine learning techniques.

## Table of Contents  
- [Project Overview](#project-overview)  
- [Dataset Information](#dataset-information)  
- [Setup Instructions](#setup-instructions)  
  - [Prerequisites](#prerequisites)  
  - [Download and Installation](#download-and-installation)  
- [Featurization](#featurization)  
- [Model Building](#model-building)  
- [Model Evaluation](#model-evaluation)  
- [Results and Analysis](#results-and-analysis)  
- [References](#references)

---

## Project Overview

The Blood brain barrier is a selective, semi-permeable membrane that protects the brain and the central nervous system (CNS) from harmful materials in the blood stream. The blood brain barrier permeability of molecules is very important in drug discovery and research, especially in the development of drugs that act on the CNS and also in identifying neurotoxic drugs.
This project is a binary classification machine learning model that will accept the smiles notation of a compound as input and predict the bbb permeability based on the chemical and molecular properties represented in the model. Permeable drugs as predicted are labelled 1 and impermeaple drugs are labelled 0. 

## Dataset Information  

This project uses the **Blood-Brain Barrier Permeability (BBBP) dataset** from [Therapeutics Data Commons (TDC)](https://tdcommons.ai/).  

- **Dataset Name**: BBBP (Martins et al., 2012)  
- **Source**: [TDC BBBP Dataset](https://tdcommons.ai/single_pred_tasks/adme/#bbbp)  
- **Original Research Paper**:  
  Martins, I. F., et al. (2012). A Bayesian approach to in silico blood–brain barrier penetration modeling. *Journal of Chemical Information and Modeling, 52*(6), 1686-1697. [DOI:10.1021/ci300124c](https://doi.org/10.1021/ci300124c)  

This dataset consists of **1975 molecules**, labeled as **BBB+ (permeable) or BBB- (non-permeable)** based on experimental permeability measurements.

## Setup Instructions

### Prerequisities

To successfully run this project, the following should be installed:
- Python 3.9 or later
- Ubuntu OS or WSL (If sysyem os is windows)
- Miniconda/Anaconda
- Docker

### Download and Installation: 

To recreate this project, follow these steps:
- Create a fork of this repository
- Copy the link to the forked project from the green drop down button labelled code in your repository 
  
 
