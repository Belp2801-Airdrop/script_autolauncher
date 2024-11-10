## Description
<h3 align="center"> Scripts Autolauncher</h3>
<p align="center">
  <picture align="center">
    <img src="https://github.com/user-attachments/assets/ff0e06f9-1f0b-48b6-9c79-dea73d5579d0"</img>
  </picture>
</p>

## Installation
### Prerequisites
- Python 3 
### Setup
- Install libs
```
pip install -r requirements.txt
```
- Setup **scripts.csv**
1. Create **scripts.csv** based on format of **scripts_sample.csv**
   
     + ***no***: index
     + ***name***: script's name (unique)
     + ***command***: command type to run script (example: **py**, **python**, **node**, **npm**,...)
     + ***file***: path to your script
     + ***cycle***: 1 cycle time waiting until next run (unit: hour, datatype: float)
     + ***is_end***: is scripts end? (0 or 1)
      
2. Add scripts you want to launch
3. Run **scripts_autolauncher.py**

