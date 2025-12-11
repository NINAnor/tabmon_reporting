#!/bin/bash

declare -a clusters=("Cap Lardier" "Porquerolles" "Port-Cros" "Salins des Pesquiers" "Vieux Salins" "Forêt d'Orient" "Amsterdamse Waterleidingduinen"
 "Hoge Veluwe" "Loenderveen" "Onlanden" "Oostvaardersplassen" "Utsira" "Lillehammer" "Hamar" "Jaeren" "Lista" "Pasvik" "Trondelag_1"
 "Trondelag_2" "Trondelag_4" "Vega" "Varanger" "Varanger_alone" "Trondelag_3" "Solsones" "Mas de Melons" "Delta del Ebre"
 "AiguamollsEmporda" "Osona" "Calanques")

mkdir -p reports

for cluster in "${clusters[@]}"; do
    echo "Rendering $cluster..."
    cluster_safe="${cluster// /_}"
    
    # Render with embed-resources (creates tabmon_reports.html)
    pixi run quarto render report/tabmon_reports.qmd --to html \
        -P cluster_name:"$cluster" \
        --embed-resources
    
    mv report/tabmon_reports.html "reports/${cluster_safe}_report.html"
done