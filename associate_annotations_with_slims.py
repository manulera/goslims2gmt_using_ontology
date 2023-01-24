import pandas
import pronto

go = pronto.Ontology('data/go.obo')
# Load the annotations (you might want to filter on relationship?)
annotations = pandas.read_csv('data/gene_association.pombase',comment='!', sep='\t', na_filter=False, usecols=[1,3,4, 6, 8, 11], names=['systematic_id','relationship','go_term_id', 'evidence', 'aspect', 'product_type'])
annotations['go_term_name'] = annotations['go_term_id'].apply(lambda x : go[x].name)

go_slim = pandas.read_csv('results/mf_mappings.tsv', sep='\t', na_filter=False, usecols=[0,1,2], names= ['go_slim_term','go_slim_description', 'go_term_id'])

out_data = go_slim.merge(annotations, on='go_term_id')
out_data = out_data[['go_slim_term','go_slim_description', 'go_term_id', 'go_term_name',  'systematic_id', 'relationship', 'evidence', 'aspect', 'product_type']]
out_data.to_csv('results/annotations_linked_to_slims.tsv', sep='\t', index=False)