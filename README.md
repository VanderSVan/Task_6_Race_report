# Package - Report of racing
## Description

**"reporting"** is a package for preparing a race report.
This is package has command line interface.
**"reporting"** package requires ***three files to work***: 'abbreviations.txt', 'start.log' and 'end.log'.
This package is compatible with python version ***3.9*** and higher (maybe).
Package "reporting" only works with os ***Windows***

## Quick Start Guide

The examples shown in this guide were performed in IDE Pycharm and os Windows.

To get a race report you will need a folder with the following files:
1) 'abbreviations.txt'
2) 'start.log'
3) 'end.log'

### 'abbreviations.txt' must contain:
* driver abbreviation
* driver's full name
* driver car model

The above information should be in the form:
```
DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES
```

### 'start.log' must contain:
* driver abbreviation
* date and time of the race start for the driver

The above information should be in the form:
```
DRR2018-05-24_12:14:12.054
SVF2018-05-24_12:02:58.917
LHM2018-05-24_12:18:20.125
```

### 'end.log' must contain:
* driver abbreviation
* date and time of race end for driver

The above information should be in the form:
```
DRR2018-05-24_1:11:24.067
SVF2018-05-24_1:04:03.332
LHM2018-05-24_1:11:32.585
```

### Use 'reporting' with command line interface
When will you have folder with the following structure:
```console
data_files/
├── abbreviations.txt
├── start.log
└── end.log
```
Just write in your terminal
```commandline
py -m reporting -f data_files
```
The terminal will output the following:
```
 1. Lewis Hamilton   | MERCEDES                  | 0:53:12.460
 2. Daniel Ricciardo | RED BULL RACING TAG HEUER | 0:57:12.013
 3. Sebastian Vettel | FERRARI                   | 1:01:04.415
```
By default, drivers are sorted in ascending order based on their final race time.
If you want descending order, then write:
```commandline
py -m reporting -f data_files --desc
```
Terminal output:
```
 1. Sebastian Vettel | FERRARI                   | 1:01:04.415
 2. Daniel Ricciardo | RED BULL RACING TAG HEUER | 0:57:12.013
 3. Lewis Hamilton   | MERCEDES                  | 0:53:12.460
```
If you want to see full statistics for only one driver, then write:
```commandline
 py -m reporting -f data_files -d "SVF"
```
Terminal output:
```
Sebastian Vettel | FERRARI | 1:01:04.415
```
If you need more information, use:
```commandline
py -m reporting -h
```