# For step by step instructions, view the README.md file in the root directory

import pandas as pd
import numpy as np

y1 = pd.read_csv(r'supporting.files\Bdistachyon_314_v3.1.annotation_info.txt', sep="\t", header=0)
pd.set_option('display.max_columns', None)
len(y1.index)

y2 = y1[['locusName', 'GO']].copy()
len(y2.index)

y2.dropna(inplace=True)
y2.reset_index(drop=True, inplace=True)
y2['GO'] = y2.groupby('locusName')['GO'].transform(lambda x : ','.join(x))
len(y2.index)
len(pd.unique(y2['locusName']))

y2.loc[y2['locusName'] =='Bradi1g00517']

y2 = y2.drop_duplicates(inplace=False, ignore_index=True)
y2.loc[y2['locusName'] =='Bradi1g00517']

len(y2.index)

len(pd.unique(y2['locusName']))

y2['GO'] = y2['GO'].str.split(',').apply(lambda x: pd.unique(x))
y2.loc[y2['locusName'] =='Bradi1g00517']

y2['GO'] = [','.join(map(str, x)) for x in y2['GO']]
y2.loc[y2['locusName'] =='Bradi1g00517']

z1 = pd.read_csv(r'supporting.files\go.obo.txt', sep="\t", header=0)
pd.set_option('display.max_columns', None)

z1.rename(columns={'ID':'GO'}, inplace=True)

# Brining it all together
gene_go = y2.copy()
gene_go.GO = gene_go.GO.str.split(',')

gene_go = gene_go.explode('GO')

# Columns that I intend to use from the gene annotation file
cols_to_use = list(['GO', 'Namespace', 'Name', 'Def'])
# Make a join
gene_go = pd.merge(gene_go, z1[cols_to_use], on='GO', how='left')

gene_go.GO = gene_go[cols_to_use].apply(lambda x: ','.join(x[x.notnull()]), axis=1)
# Removing now redundant columns
gene_go.drop(['Namespace', 'Name', 'Def'], axis=1, inplace=True)
gene_go = gene_go.sort_values('locusName', ascending=True)

gene_go['Var'] = gene_go.groupby('locusName').cumcount()+1

gene_go_pivoted = gene_go.pivot(index='locusName', columns='Var', values='GO')

yFinal = pd.merge(y1, gene_go_pivoted, on='locusName', how='left')

pd.DataFrame.head(yFinal, 5)