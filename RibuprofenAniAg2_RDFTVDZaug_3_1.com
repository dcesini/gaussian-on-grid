%int=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3_1.int
%rwf=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3_1.rwf
%d2e=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3_1.d2e
%nosave
%chk=./Gaussian/RibuprofenAniAg2_RDFTVDZaug_3_1.chk
%nproc=8
%Mem=8GB
#p B3LYP/Gen Opt=Redundant Geom=checkpoint Pseudo=Read 6D

 R-Ibuprofen Anion/6-31G(d) no solvent Ag2/LANL2DZ geometry opt, 2nd Ring setting

-1 1

C H O 0
6-31G(d)
****
Ag 0
LANL2DZ
****

Ag 0
LANL2DZ

