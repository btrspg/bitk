# AUTOGENERATED! DO NOT EDIT! File to edit: 08_polya_sites.ipynb (unless otherwise specified).

__all__ = ['polya_in_nanopolish', 'polya_length_in_gene', 'polya_length_correlation']

# Cell

import pandas as pd
import pysam
import scipy.stats as stats

from .utils.multirun import parallel_run

# Cell

def polya_in_nanopolish(polya):
    df = pd.read_csv(polya,sep='\t')
    return df[df['qc_tag']=='PASS']


# Cell

def polya_length_in_gene(bam,contig,polya):
    with pysam.AlignmentFile(bam,'rb') as buf:
        polya_df = polya_in_nanopolish(polya)
        contig_b = buf.fetch(contig=contig,multiple_iterators=True)
        query_names= []
        for i in contig_b:
            query_names.append(i.query_name)
        if len(query_names) > 0:
            return contig,polya_df[polya_df['readname'].isin(query_names)]['polya_length'].median()
        else:
            return contig,None


# Cell

def polya_length_correlation(transcriptome_bam,polya,nanocount,outdir,*,contigs=None,thread=10):
    '''

    :param str transcriptome_bam: alignments of reads to transcriptome
    :param str polya: polya results from nanopolish polya
    :param str nanocount: nanocount result
    :param str outdir: outdir
    :param list[str] contigs: contigs
    :param int thread: thread
    '''
    with pysam.AlignmentFile(transcriptome_bam,'rb') as buf:
        if None is contigs:
            genes = buf.references
        else:
            genes = contigs

    paras = [[transcriptome_bam,gene, polya] for gene in genes]
    results = parallel_run(polya_length_in_gene,paras, thread=thread)
    p_df=pd.DataFrame(results,columns=['transcript','polya_length'])
    tpm = pd.read_csv(nanocount,sep='\t')
    m_df=tpm.merge(p_df,how='left',left_on='transcript_name',right_on='transcript',)
    cor_df = m_df.dropna()
    cor,p = stats.pearsonr(cor_df['tpm'],cor_df['polya_length'])
    print(f'Cor:{cor},and P value: {p}')
    m_df.to_csv(f'{outdir}/polya_length_tpm.csv',index=False)