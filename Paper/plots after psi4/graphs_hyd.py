#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook')
el = pd.read_excel('combined_hydrogen_bond.xlsx')


# In[8]:


fig, ax = plt.subplots(figsize=(4, 4), dpi=600)

cc = {'Elst': '#fe6156', 'Exch': '#000000', 'Disp': '#bdbdbd', 'Ind': 'white', 'Total': '#1572A1'}
pars_line = {'lw': 0}
pars_marker = {'s': 20, 'edgecolor': 'black', 'linewidth': 0.5}
#electrostatic
sns.lineplot(data=el, x='Distance', y='Elst', color=cc['Elst'], zorder=2, **pars_line)
sns.scatterplot(data=el, x='Distance', y='Elst', zorder=5, color=cc['Elst'], **pars_marker)

#steric
sns.lineplot(data=el, x='Distance', y='Exch', color=cc['Exch'], zorder=2, **pars_line)
sns.scatterplot(data=el, x='Distance', y='Exch', zorder=3, color=cc['Exch'], **pars_marker)

#total
sns.lineplot(data=el, x='Distance', y='Total', color=cc['Total'], zorder=2, **pars_line)
sns.scatterplot(data=el, x='Distance', y='Total', zorder=6, color=cc['Total'], **pars_marker)

#induction
sns.lineplot(data=el, x='Distance', y='Ind', color=cc['Ind'], zorder=2, **pars_line)
sns.scatterplot(data=el, x='Distance', y='Ind', zorder=3, color=cc['Ind'], **pars_marker)

#dispersion
sns.lineplot(data=el, x='Distance', y='Disp', color=cc['Disp'], zorder=2, **pars_line)
sns.scatterplot(data=el, x='Distance', y='Disp', zorder=4, color=cc['Disp'], **pars_marker)


ax.grid(visible=True, which='major', axis='both', lw=1, c='#d9e2e6')

#Limits
plt.xlim(1.7, 6.7)

plt.ylim(-90, 30)

#Labels
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "arial"
plt.rcParams["mathtext.fontset"] = 'custom'
plt.rcParams["mathtext.default"] = 'rm'
plt.rcParams["mathtext.bf"] = 'sans:bold'
plt.rcParams["mathtext.rm"] = 'sans'
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 12
label_fonts = {'fontsize': 14}

plt.xlabel(r'N$\cdots$H$\mathrm{-}$O distance, $\AA$', labelpad=1, **label_fonts)
plt.ylabel('')

#________________________inset___________________________

from mpl_toolkits.axes_grid1.inset_locator import mark_inset

axins = ax.inset_axes((0.35,0.1,.6,.6))

axins.axis([1.8, 2.8, -20, 20])
sns.scatterplot(data=el, x='Distance', y='Elst', zorder=5, color=cc['Elst'], **pars_marker, ax=axins)
sns.scatterplot(data=el, x='Distance', y='Exch', zorder=3, color=cc['Exch'], **pars_marker, ax=axins)
sns.scatterplot(data=el, x='Distance', y='Total', zorder=6, color=cc['Total'], **pars_marker, ax=axins)
sns.scatterplot(data=el, x='Distance', y='Ind', zorder=3, color=cc['Ind'], **pars_marker, ax=axins)
sns.scatterplot(data=el, x='Distance', y='Disp', zorder=4, color=cc['Disp'], **pars_marker, ax=axins)

#labels for inset

axins.tick_params(left=True,
                  bottom=True,
                  labelleft=True,
                  labelbottom=True,
                  )
axins.set_xlabel('')
axins.set_ylabel('')

axins.set_xticks([2, 2.5])
axins.set_yticks([-20, 0, 15])

# zoom

mark_inset(ax, axins, loc1=1, loc2=3, fc='none', ec='#414141', ls='--', lw=1, zorder=2)

axins.grid(visible=True, which='major', axis='both', lw=1, c='#d9e2e6')

plt.savefig('hyd_v9_final_ins.svg', dpi=600, format='svg')

plt.show()


# In[3]:


el


# In[ ]:




