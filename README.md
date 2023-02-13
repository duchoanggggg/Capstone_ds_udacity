# MBTI_based-Movie-Recommendation Testing Instruction
## Folder description
- data: contains raw and cleaned data for project
  + Questionaires.xlsx: survey raw data
  + user_MBTI.csv: cleaned data for recommendation
  + cold_start_train/test.csv: data test for cold start from cleaned data for system evaluation
  + train/test_historical_data.csv: data test for cold start from cleaned data for system evaluation
- code_preprocessing_data.ipynb: contains description and code for preprocessing raw data
- code.ipynb: contains evaluation score for the recommendation methodologies used in the project.
- project_description.pdf: describes the project
- Movies_recommendation.py: run demo Recommendation System
- requirements.txt: libraries needed to run the demo
## System demo
1. Install libraries from 'pip install -r requirements.txt'
2. Run demo 'python Movies_recommendation.py' and follow the link to local web and fill out the survey to get the recommendation.
