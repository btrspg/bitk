# AUTOGENERATED! DO NOT EDIT! File to edit: 11_plots.ipynb (unless otherwise specified).

__all__ = ['compare_plots']

# Cell

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Cell

def compare_plots(df,column1,column2,name1,name2,value_name,output,hue):
    '''

    :param df:
    :param column1:
    :param column2:
    :param name1:
    :param name2:
    :param output:
    :param hue:
    :return:
    '''
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), tight_layout=True)
    jp = sns.scatterplot(x=column1, y=column2, data=df,ax=ax1,hue=hue)
    cor,p = stats.pearsonr(df[column1],df[column2])
    jp.annotate(text='COR=%.2f,p=%.2f' % (cor,p) ,xy=(0,max(df[column2])))
    jp.set_xlabel(name1)
    jp.set_ylabel(name2)
    jp.set_title(f'Scatter plots of {value_name} in {name1} and {name2}')
    tmp=df.rename(columns={column1:name1,column2:name2}).melt(id_vars=None,
                                                              value_vars=[name1,name2],
                                                              var_name='class',
                                        value_name=value_name)
    vp =sns.violinplot(x='class', y=value_name,data=tmp,ax=ax2)
    vp.set_title(f'Violin plot of {value_name} in {name1} and {name2}')

    fig.savefig(output,dpi=1200)