# TABMON reports  

This repository contains the necessary to automatically produce reports for communicating to the TABMON stakeholders (e.g. persons who are interested in the project, persons who helped the team to setup the devices etc.)

## Setup the data folder

To produce the TABMON reports, the following files are needed:

Specific to TABMON:

https://tabmon.nina.no/data/index.parquet
https://tabmon.nina.no/data/site_info.csv 
https://tabmon.nina.no/data/merged_predictions_light/

Non-TABMON specific:

[european_red_list.xlsx](https://datazone.birdlife.org/publications/european-red-list-of-birds)
[BirdNET_GLOBAL_6K_V2.4_Labels.txt](https://github.com/birdnet-team/BirdNET-Analyzer)

Place all the above in a `data` folder so that the structure looks:

```
|-data
|-----index.parquet
|-----site_info.csv
|-----merged_predictions_light/
|-----european_red_list.xlsx
|-----BirdNET_GLOBAL_6K_V2.4_Labels.txt
```

## Setup environment

- Pull the repository and install the dependancies.

```
git clone ...
uv sync
```

- Install [pixi](https://pixi.sh/latest/) on your system. `Pixi` is an environment manager  

```
wget -qO- https://pixi.sh/install.sh | sh
```

- Install [Quarto](https://quarto.org/), which is basically like `Rmarkdown` that supports other languages (including Python).

```
pixi add quarto
```

- Create the report

```
pixi run quarto render report/tabmon_reports.qmd --to html
```

- Or create reports for all clusters:

```
./report_for_all_clusters.sh
```

## Contact

- [Corentin Bernard](mailto:corentin.bernard@lis-lab.fr)
- [Benjamin Cretois](mailto:benjamin.cretois@nina.no)
