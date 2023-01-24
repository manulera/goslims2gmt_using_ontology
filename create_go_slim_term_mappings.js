import { OboGraphViz } from "obographviz";
import fs from "fs";

// Read the json GO graph
const goJson = JSON.parse(fs.readFileSync("data/go.json"))

// Remove all relationships that are not part_of or is_a (not used in GO slim)
goJson.graphs[0].edges = goJson.graphs[0].edges.filter(
    edge => ['is_a', 'http://purl.obolibrary.org/obo/BFO_0000050'].includes(edge.pred)
)

// Load the graph object
const goGraph = new OboGraphViz(goJson);
const bbopGraph = goGraph.createBbopGraph();

// Print column names
console.log('go_slim_term\tgo_slim_description\tsubject_id\trelationship\tobject_id')

// Read the tsv file, and for each line GO-slim term, print the GO:slim term and all its children, comma separated
fs.readFileSync(process.argv[2], "utf-8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (line.length === 0) {return}
    const goSlimTerm = line.split("\t")[0];
    const goSlimDescription = line.split("\t")[1];
    const termUrl = `http://purl.obolibrary.org/obo/${goSlimTerm.replace(":", "_")}`;
    // Include the term itself as well
    console.log(`${goSlimTerm}\t${goSlimDescription}\t${goSlimTerm}\tis_a\t${goSlimTerm}`)
    // Get all children of a term
    const subgraph = bbopGraph.get_descendent_subgraph(termUrl);
    subgraph.all_edges().forEach((edge) => {
        const subject_id = edge.subject_id().replace("http://purl.obolibrary.org/obo/", "").replace("_", ":")
        const immediate_parent = edge.object_id().replace("http://purl.obolibrary.org/obo/", "").replace("_", ":")
        const relationship = edge.predicate_id()
        console.log(`${goSlimTerm}\t${goSlimDescription}\t${subject_id}\t${relationship}\t${immediate_parent}`)
    });

  });
