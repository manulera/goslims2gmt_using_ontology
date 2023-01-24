# Prepare directory structure
mkdir -p data
mkdir -p results

# Download GO-slims
curl -o data/mf_goslim_pombe_ids_and_names.tsv https://www.pombase.org/data/releases/latest/misc/mf_goslim_pombe_ids_and_names.tsv
curl -o data/cc_goslim_pombe_ids_and_names.tsv https://www.pombase.org/data/releases/latest/misc/cc_goslim_pombe_ids_and_names.tsv
curl -o data/bp_goslim_pombe_ids_and_names.tsv https://www.pombase.org/data/releases/latest/misc/bp_goslim_pombe_ids_and_names.tsv

# Download GO annotations
curl -o data/gene_association.pombase.gz https://www.pombase.org/data/annotations/Gene_ontology/gene_association.pombase.gz
gzip -fd data/gene_association.pombase.gz

# Download the results from PomBase API to compare
curl -o data/bp_goslim.gmt https://raw.githubusercontent.com/pombase/goslims2gmt/master/results/bp_goslim.gmt
curl -o data/mf_goslim.gmt https://raw.githubusercontent.com/pombase/goslims2gmt/master/results/mf_goslim.gmt
curl -o data/cc_goslim.gmt https://raw.githubusercontent.com/pombase/goslims2gmt/master/results/cc_goslim.gmt

# Download GO Ontology
curl -o data/go.json http://current.geneontology.org/ontology/go.json
curl -o data/go.obo http://purl.obolibrary.org/obo/go.obo

date > data/timestamp.txt