import pandas as pd

def rank_schools(df, tWeight, gWeight, eWeight):
	total_weight = tWeight + gWeight + eWeight
	df['Score'] = (
		(
			( tWeight * df['Rank_Tuition'] ) +
			( gWeight * df['Rank_Grad_Rate'] ) +
			( eWeight * df['Rank_Employment_Rate'] )
		) / total_weight
	)
	df['Grand_Rank'] = df['Score'].rank(ascending=True)
	return df.sort_values(by='Grand_Rank', ascending=False)