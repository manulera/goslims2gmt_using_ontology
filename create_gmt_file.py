"""
From a mappings file, convert to gmt-like file

Usage:
    python create_gmt_file.py results/mf_mappings.tsv results/mf_results.tsv

"""

import pandas
import sys

def main(input_file, output_file):

    # Load the annotations (you might want to filter on relationship?)
    annotations = pandas.read_csv('data/gene_association.pombase',comment='!', sep='\t', na_filter=False, usecols=[1,3,4,6], names=['systematic_id','relationship','go_term_id', 'evidence'])
    # Remove negative annotations
    annotations = annotations[~annotations['relationship'].str.contains('NOT|', regex=False)].copy()

    # Load the go_slim_mappings
    go_slim = pandas.read_csv(input_file, sep='\t', na_filter=False)

    # Drop the unnecessary columns
    go_slim.drop(columns=['object_id', 'relationship'], inplace=True)
    go_slim.drop_duplicates(inplace=True)

    # Aggregate all go child terms in a comma-separated column
    go_slim = go_slim.groupby(['go_slim_term', 'go_slim_description'], as_index=False).agg({'subject_id': ','.join})

    # Rename the new column to children
    go_slim.rename(columns={'subject_id': 'children'}, inplace=True)

    # go_slim.to_csv('a.tsv', sep='\t')


    # Function to be ran at each row of the mapping file to find annotations
    def all_genes_annotated_to_go_term_and_children(row):

        terms2find = set(row['children'].split(','))

        # Include also the parent
        terms2find.add(row['go_slim_term'])

        return list(set(annotations.loc[annotations.go_term_id.isin(terms2find), 'systematic_id']))

    # We add an extra column to store the systematic ids of linked genes
    go_slim['associated_genes'] = go_slim.apply(all_genes_annotated_to_go_term_and_children, axis=1)
    go_slim['count'] = go_slim['associated_genes'].apply(len)

    # We drop the children column
    go_slim.drop(columns='children', inplace=True)

    # re-order
    go_slim = go_slim[['go_slim_term', 'go_slim_description', 'count', 'associated_genes']]
    go_slim.sort_values('go_slim_description', inplace=True, key=lambda col: col.str.lower())
    go_slim.associated_genes = go_slim.associated_genes.apply(','.join)

    go_slim.to_csv(output_file,sep='\t', index=False)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])