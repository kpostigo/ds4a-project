import pandas as pd

df = pd.read_csv('final_csv.csv',sep=',',low_memory=False)


#inputs
school_name = 'Brown University'
tuition_weight = 9
graduation_weight = 8
employment_weight = 3

total_weight = tuition_weight+graduation_weight+employment_weight

# not sure about the syntax for the score column but wanted to include the code
df['Score'] = (
    (
      ((tuition_weight)*(df['Rank_Tuition']))
    + ((graduation_weight)*(df'Rank_Grad_Rate']))
    + ((employment_weight)*(df['Rank_Employment_Rate']))
    )/total_weight)

# grand rank column will provide definitive ranking based on weights
df['Grand_Rank'] = df['Score'].rank(ascending=True)
df.sort_values(by='Grand_Rank', ascending = False)
