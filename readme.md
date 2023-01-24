
Generates gmt-like files for each go-slim (first and second column go slim name and description, rest of the columns the systematic_ids of associated genes). It does it
using the ontology json file and the go-slim lists from pombase (see `get_data.sh`)

## Install dependencies

```
poetry install
npm install
```

## Run

```
poetry shell
bash get_data.sh
bash run_all
```