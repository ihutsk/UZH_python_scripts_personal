#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook')



df = pd.read_excel('pair3_overview.xlsx')



df = df.T



df.reset_index(inplace=True)


df.columns = df.iloc[0]



df=df.drop(0, axis=0)


fig, ax = plt.subplots(figsize=(2,5), dpi=100)
cc = {'Elst': '#fe6156', 'Exch': '#000000', 'Disp': '#bdbdbd', 'Ind': '#ffffff', 'Total': '#1572A1'}
a = '4a_naked' # change the name here according to the excel
sns.barplot(x=df['Name'], y=df[a],
            order=['Disp', 'Ind', 'Exch', 'Elst', 'Total'],
            palette=cc,
            edgecolor='black',
            linewidth=1.5,
            ax=ax,
            dodge=False)

ax.margins(0.04)
# labels
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "arial"
plt.rcParams["mathtext.fontset"] = 'custom'
plt.rcParams["mathtext.default"] = 'rm'
plt.rcParams["mathtext.bf"] = 'sans:bold'
plt.rcParams["mathtext.rm"] = 'sans'
plt.rcParams["ytick.labelsize"] = 12
label_fonts = {'fontsize': 14}
plt.xlabel('')
plt.xticks([])
plt.ylabel('')


#spines

ax.spines['left'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)


ax.axhline(y=0, c='black', lw=1.5)
#limits

plt.ylim(-110, 90)


# annotation
font_dict = {'fontsize': 10}
ax.text(-.5, df.loc[4, a]-10, round(df.loc[4, a], 1), **font_dict)
ax.text(0.55, df.loc[2, a]-10, round(df.loc[2, a], 1), **font_dict)
ax.text(1.55, df.loc[3, a]+5, round(df.loc[3, a], 1), **font_dict)
ax.text(2.35, df.loc[1, a]-10, round(df.loc[1, a], 1), **font_dict)
ax.text(3.45, df.loc[5, a]-10, round(df.loc[5, a], 1), **font_dict)

plt.savefig(f'pair_{a}.svg', format='svg', dpi=600, bbox_inches='tight')
plt.show()



df


# In[ ]:




