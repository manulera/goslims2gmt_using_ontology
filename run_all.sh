set -e
# Create mapping files
node create_go_slim_term_mappings.js data/cc_goslim_pombe_ids_and_names.tsv > results/cc_mappings.tsv
node create_go_slim_term_mappings.js data/bp_goslim_pombe_ids_and_names.tsv > results/bp_mappings.tsv
node create_go_slim_term_mappings.js data/mf_goslim_pombe_ids_and_names.tsv > results/mf_mappings.tsv

# Create gmt-like files
python create_gmt_file.py results/mf_mappings.tsv results/mf_results.tsv
python create_gmt_file.py results/bp_mappings.tsv results/bp_results.tsv
python create_gmt_file.py results/cc_mappings.tsv results/cc_results.tsv

# Run the controls (print the discrepancy to results/??bp_discrepancy.tsv)
mkdir -p temp
python associate_annotations_with_slims.py

python discrepancy_with_pombase.py results/mf_results.tsv data/mf_goslim.gmt results/mf_discrepancy.tsv
python discrepancy_with_pombase.py results/cc_results.tsv data/cc_goslim.gmt results/cc_discrepancy.tsv
python discrepancy_with_pombase.py results/bp_results.tsv data/bp_goslim.gmt results/bp_discrepancy.tsv

date > results/timestamp.txt