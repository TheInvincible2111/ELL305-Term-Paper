$pdf_mode = 1;
$bibtex_use = 2;
$out_dir = '../build/aux';
$aux_dir = '../build/aux';
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$biber = 'biber %O %B';

END {
    if (-e '../build/aux/main.pdf') {
        require File::Copy;
        File::Copy::copy('../build/aux/main.pdf', '../build/pdf/ELL305-Draft-1.pdf');
    }
}
