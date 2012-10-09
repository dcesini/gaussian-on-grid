%int=./gauss_scratch/ampicillin0.int
%rwf=./gauss_scratch/ampicillin0.rwf
%d2e=./gauss_scratch/ampicillin0.d2e
%nosave
%chk=./Gaussian/ampicillin0.chk
%nproc=12
%Mem=10GB
#p B3LYP/6-31G(d,p) Opt=Redundant Geom=checkpoint

 ampicillin neutral geometry optimization no solvent

0 1



