%int=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3res.int
%rwf=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3res.rwf
%d2e=./gauss_scratch/RibuprofenAniAg2_RDFTVDZaug_3res.d2e
%nosave
%chk=./Gaussian/ibuprofenVDZAg/RibuprofenAniAg2_RDFTVDZaug_3res.chk
%nproc=8
%Mem=3GB
#p B3LYP/Gen Opt=Redundant Geom=Checkpoint Guess=Read Pseudo=Read SCF(QC,MaxCyc=250) 6D

 R-Ibuprofen Anion/aug-cc-pVDZ no solvent Ag2/LANL2DZ geometry opt, 2nd Ring setting

-1 1

C H O 0
aug-cc-pVDZ
****
Ag 0
LANL2DZ
****

Ag 0
LANL2DZ



