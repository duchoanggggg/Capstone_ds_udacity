# MBTI_based-Movie-Recommendation Testing Instruction
## Project Scope
  - In this project, I propose to use Myer-Briggs Type Indicator (MBTI) in movie recommendation system to individualize recommendations by user-user collaborative filtering. In personality typology, MBTI is an introspective self-report questionnaire indicating differing psychological preferences in how people perceive the world and make decisions. The test attempts to assign 4 categories: Introverted vs Extroverted, Sensing vs INtuition, Thinking vs Feeling, Judging vs Perceiving. One letter from each category is taken to produce a for letter list such as INFP. 
  - Metrics: In this project, I use MAE score and RMSE score to evaluate the recommendation.

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

## Results
  - For historical watching users, there is an outstanding result from Info+ Rating input, the reason is having more data the models would predict better, this input together with Info Only result is far more better than Rating Only. However, the most significant result is Cold-start. 
