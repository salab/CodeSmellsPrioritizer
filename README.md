# Code Smells Prioritizer (CSP) tool #
This is a tool for prioritizing code smells using developers' context. Please refer to our [publication](#publication) for more details.
## How to use
1. Prepare the input files: code smell file and impact analysis file (see [Input File Format](#input-file-format)).
2. Use the following command to generate the result.
3. The result will be generated as Result.csv (see [Output File Format](#output-file-format)).
#### Usage:
```
 python CSP.py code_smell_file_name impact_analysis_file_name [alpha=1] [cut_point=40] 
```

#### Example:
```
python CSP.py Smells.csv IA.csv 1 40
```

## Input File Format
#### Code smell file:

| Smell ID	| Severity	| Class Name	| Package Name	 | Smell Type |
| --- | ------- |  ---------- |  ----------------- |  --------- | 
| 1  | 7        |  ClassA     |  com.package.ui    |  God       | 
| 2  | 8        |  ClassB     |  com.package.model |  Blob      | 
| .  | .        | .           | .                  | .          |

*Smell ID* = A Unique ID of each smell  
*Severity* = An integer representing the severity of each smell (e.g. 1-10)

Example: Smells.csv

#### Impact analysis file:

| Issue ID  | Class Full Name            | Score |
| --------- | -------------------------- | ----- |
| 1001      | com.package.ui.ClassA      | 0.321 |
| 1001      | com.package.model.ClassB   | 0.211 |
| .         | .                          | .     |

Example: IA.csv

## Output File Format
#### Result file:
| Smell ID |	Ranking	| CRI        	| Severity	| Class Name	       | Package Name |
| -------- | ------- |  ---------- |  ------- |  ---------------- | ------------ |
| 70       | 1.0     |  3.21       |  2       | com.package.ui    |  God         | 
| 25       | 0.9     |  2.13       |  3       | com.package.model |  Blob        | 
| .        | .       | .           | .        | .                 | .            |

*Ranking* = A criterion used for prioritizing code smell  
*CRI* = Context Relevance Index  
For the details on the calculation of *Ranking* and *CRI*, please refer to our [publication](#publication).

Example: Result.csv
## Publication
To be added
