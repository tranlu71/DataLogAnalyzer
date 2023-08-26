# DataLogAnalyzer
## Problem definition
At the end of each test treatment (typical 15 minutes long), the system generated a csv file that contains all sensors reading and system states logged every 250ms. Depending on the type of the study, some or all of the following information is needed to fill out the test datasheet: 
* maximum pressure during run
* maximum temperature at the end of the run
* temperature spike at the beginning of the run
* the time it takes for laser interlock to engage
* the time that temperature stablizes before laser is fired
* laser start timestamp
* laser end timestamp
* power level

Need to write a program that enables user to pick the parameter(s) from all of the data files generated that day and generate a summary report. 
## Algorithms
## How to run the program
* Install python3 and clone the repository to your local machine
* In terminal, navigate to the repository, type "GUIReadHTTLog.py" to run the script
* Follow the instructions provided by the script
