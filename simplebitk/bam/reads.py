# AUTOGENERATED! DO NOT EDIT! File to edit: 12_reads_head.ipynb (unless otherwise specified).

__all__ = ['retreat_upstreams_downstreams_from_read', 'retreat_seq_from_fasta', 'extract_sequences']

# Cell

import pysam
import os


# Cell

def retreat_upstreams_downstreams_from_read(read,reference_o,sequence_length=10):
    '''
    '''
    read_start = 0
    read_end = read.infer_read_length()
    mapped_read_start = read.query_alignment_start
    mapped_read_end = read.query_alignment_end

    read_head = read.seq[0:sequence_length]
    read_tail = read.seq[read_end-sequence_length:read_end]
    if read_end-sequence_length == read_end:
        print(read_end-sequence_length,read_end)
    if read_tail == '':
        print(read)
        print(read_end,read.infer_read_length())
        raise ValueError('tes')
    mapped_read_head = read.seq[mapped_read_start:mapped_read_start+sequence_length]
    mapped_read_tail = read.seq[mapped_read_end-sequence_length:mapped_read_end]


    is_reverse = read.is_reverse


    ref_first = max(0,read.reference_start-sequence_length)
    ref_second = read.reference_start if ref_first !=0 else sequence_length
    ref_forth = min(reference_o.get_reference_length(read.reference_name),read.reference_end+sequence_length)
    ref_third = read.reference_end if ref_forth != reference_o.get_reference_length(read.reference_name) else reference_o.get_reference_length(read.reference_name) - sequence_length

    try:
        if not is_reverse:
            upstream_seq = retreat_seq_from_fasta(reference_o,read.reference_name,ref_first,ref_second,is_reverse)
            downstream_seq = retreat_seq_from_fasta(reference_o,read.reference_name,ref_third,ref_forth,is_reverse)
        else:
            upstream_seq = retreat_seq_from_fasta(reference_o,read.reference_name,ref_third,ref_forth,is_reverse)
            downstream_seq = retreat_seq_from_fasta(reference_o,read.reference_name,ref_first,ref_second,is_reverse)
    except Exception:
        print(read)
        raise ValueError('test')

    return read_head,read_tail,mapped_read_head,mapped_read_tail,upstream_seq,downstream_seq

def retreat_seq_from_fasta(fasta_o,contig,start,end,is_reverse=False):
    try:
        seq = fasta_o.fetch(contig,start,end)
        if is_reverse:
            return seq.translate(str.maketrans('ATCG','TAGC'))[::-1]
        else:
            return seq
    except Exception as e:
        print(contig,start,end,is_reverse)
        raise ValueError(e)





# Cell

def extract_sequences(bam_file,fasta_file,padding=30,prefix='./extract_sequences'):
    '''
    extract sequences for motif identification

    :param str bam_file: bam file path, with bam.bai in the same directory
    :param str fasta_file: reference fasta file path, with fasta.fai in the same directory
    :param int padding: the nucleotides number that retreated
    :param str prefix: output prefix, there will be six output files
    '''
    os.makedirs(os.path.dirname(os.path.abspath(prefix)),exist_ok=True)
    with pysam.AlignmentFile(bam_file,'r') as bam_o,pysam.FastaFile(fasta_file) as fasta_o,\
        open(f'{prefix}_read_head.fasta','w') as rh,\
            open(f'{prefix}_read_tail.fasta','w') as rt, \
                open(f'{prefix}_mread_head.fasta','w') as mrh, \
                    open(f'{prefix}_mread_tail.fasta','w') as mrt, \
                        open(f'{prefix}_upstream.fasta','w') as us, \
                            open(f'{prefix}_downstream.fasta','w') as ds:
        for i, read in enumerate(bam_o):
            if i % 10000 == 0:
                print(f'reading {i}th reads')
            if (not read.is_unmapped) and (not read.is_secondary) and (not read.is_supplementary):
                read_head, read_tail, mread_head, mread_tail, upstream, downstream = retreat_upstreams_downstreams_from_read(read,fasta_o,sequence_length=padding)
                # if len(read_head) != padding:
                #     print(read)
                #     print('read head')
                # if len(read_tail) != padding:
                #     print(read)
                #     print('read tail')
                # if len(mread_head) != padding:
                #     print(read)
                #     print('mread head')
                # if len(mread_tail) != padding:
                #     print(read)
                #     print('nread tail')
                # if len(downstream) != padding:
                #     print(read)
                #     print(downstream)
                #     print('down')
                # if len(upstream) != padding:
                #     print(read)
                #     print(upstream)
                #     print('up')
                rh.write(f'>seq_{i}\n')
                rt.write(f'>seq_{i}\n')
                mrh.write(f'>seq_{i}\n')
                mrt.write(f'>seq_{i}\n')
                us.write(f'>seq_{i}\n')
                ds.write(f'>seq_{i}\n')
                rh.write(read_head+'\n')
                rt.write(read_tail+'\n')
                mrh.write(mread_head+'\n')
                mrt.write(mread_tail+'\n')
                us.write(upstream+'\n')
                ds.write(downstream+'\n')
