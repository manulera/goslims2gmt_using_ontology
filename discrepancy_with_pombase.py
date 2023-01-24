import pandas
import sys

def main(script_results, api_results, output_file):

    annotations = pandas.read_csv('results/annotations_linked_to_slims.tsv', sep='\t', na_filter=False)

    found = pandas.read_csv(script_results, sep='\t', na_filter=False)
    found['associated_genes'] = found['associated_genes'].apply(lambda x : x.split(','))

    api_data = list()
    with open(api_results) as ins:
        for line in ins:
            ls = line.strip().split('\t')
            api_data.append([ls[0],ls[1], ls[2:]])
    api_data = pandas.DataFrame(api_data, columns=['go_slim_term','go_slim_description','associated_genes'])

    api_data = api_data.explode('associated_genes')
    api_data['in_api'] = True

    found = found.explode('associated_genes')

    data2compare = found.merge(api_data[['go_slim_term','associated_genes','in_api']], on=['go_slim_term','associated_genes'], how='outer')

    not_in_api = data2compare[data2compare.in_api != True].copy()
    not_in_api.rename(columns= {'associated_genes': 'systematic_id'}, inplace=True)

    annotation_to_print = annotations.merge(not_in_api[['go_slim_term', 'systematic_id']], on=['go_slim_term', 'systematic_id'])
    annotation_to_print.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])