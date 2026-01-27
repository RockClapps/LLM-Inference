#!/bin/bash

mkdir reddust
cd reddust

if [[ ! -f profession.csv ]]; then
  echo 'category,id,answer,postid' > profession.csv
  curl https://pkb.mpi-inf.mpg.de/reddust_data/profession.txt | sed "s/\t/,/g" >> profession.csv
fi

if [[ ! -f hobby.csv ]]; then
  echo 'category,id,answer,postid' > hobby.csv
  curl https://pkb.mpi-inf.mpg.de/reddust_data/hobby.txt | sed "s/\t/,/g" >> hobby.csv
fi

if [[ ! -f family.csv ]]; then
  echo 'category,id,answer,postid' > family.csv
  curl https://pkb.mpi-inf.mpg.de/reddust_data/family.txt | sed "s/\t/,/g" >> family.csv
fi

if [[ ! -f age.csv ]]; then
  echo 'category,id,answer,postid' > age.csv
  curl https://pkb.mpi-inf.mpg.de/reddust_data/age.txt | sed "s/\t/,/g" >> age.csv
fi

if [[ ! -f gender.csv ]]; then
  echo 'category,id,answer,postid' > gender.csv
  curl https://pkb.mpi-inf.mpg.de/reddust_data/gender.txt | sed "s/\t/,/g" >> gender.csv
fi
