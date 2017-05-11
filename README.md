# Code Smells Prioritizer (CSP) tool #

### How to use ###
#### Usage: ####
```
 python CSP.py code_smell_file_name impact_analysis_file_name [alpha]  
```

#### Example: ####
```
python CSP.py Smells.csv IA.csv 1
```
  
Output: Results.csv

### Input Files Format ###
#### Code smell file: ####

| Id	| Severity	| Entity Name	| Package Name	| Smell Type |
| --- | ------- |  ---------- |  ----------- |  --------- | 
| 1  | 7        |  ClassA     |  com.package.ui |  God | 
| 2  | 8        |  ClassB     |  com.package.model |  Blob | 
| .  | .        | .           | .            | .          |

Example: Smells.csv

#### Impact analysis file: ####

| Issue ID  | Entity Name | Score |
| --------- | ----------- | ----- |
| 1001      | ClassA      | 0.321 |
| 1001      | ClassB      | 0.211 |
| .         | .           | .     |

Example: IA.csv
