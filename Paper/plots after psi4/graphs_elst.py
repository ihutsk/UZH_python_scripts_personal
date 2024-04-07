#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook')
el = pd.read_excel('combined_ionic_bond.xlsx')


# In[9]:


pc = pd.read_excel('point_charges.xlsx')


# In[37]:


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
#pc
sns.lineplot(data=pc, x='d', y='E, kcal/mol', color='#ffa356', zorder=7, lw=1.5)
arrowprops={'arrowstyle': '-',
            'alpha': 1,
            'lw': 1,
            'color': '#000000',
            'shrinkB': 5}
label_pars = {'fontsize': 12, 'clip_on': False}
plt.annotate('E$_{\itcoul}$', (4.7, -72.65), xytext=(4.5, -55), ha='center', arrowprops=arrowprops,
            bbox=dict(boxstyle='square,pad=0.0', lw=0, alpha=0), **label_pars)

ax.grid(visible=True, which='major', axis='both', lw=1, c='#d9e2e6')

#Limits
plt.xlim(4, 9)

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

plt.xlabel(r'N$\cdots$S distance, $\AA$', labelpad=1, **label_fonts)
plt.ylabel('Energy, kcal/mol', **label_fonts)


plt.savefig('elst_pc.svg', dpi=600, format='svg', bbox_inches='tight')

plt.show()


# In[7]:


pc[pc['d'] >4.5]

