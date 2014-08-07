#!/bin/bash

rm -rf ./panic_export
mkdir panic_export
mkdir panic_tmp
./manage.py panic_export
pdftk ./panic_tmp/sottocampo1_dettagli_*.pdf cat output ./panic_export/sottocampo1_dettagli_clan.pdf
pdftk ./panic_tmp/sottocampo2_dettagli_*.pdf cat output ./panic_export/sottocampo2_dettagli_clan.pdf
pdftk ./panic_tmp/sottocampo3_dettagli_*.pdf cat output ./panic_export/sottocampo3_dettagli_clan.pdf
pdftk ./panic_tmp/sottocampo4_dettagli_*.pdf cat output ./panic_export/sottocampo4_dettagli_clan.pdf
pdftk ./panic_tmp/sottocampo5_dettagli_*.pdf cat output ./panic_export/sottocampo5_dettagli_clan.pdf
rm -rf ./panic_tmp
