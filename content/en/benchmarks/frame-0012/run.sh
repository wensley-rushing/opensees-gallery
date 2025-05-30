#!/bin/sh
for pattern in A B C D; do 
  center=$pattern
  for center in $pattern C; do #A B C D; do 
    for section in const fiber; do
      for warping in n o p r; do 
        echo Section=$section Warping=$warping Pattern=$pattern Center=$center Element=ExactFrame python e0012.py; 
        Section=$section Warping=$warping Pattern=$pattern Center=$center Element=ExactFrame python e0012.py; 
      done; 
    done;
  done;
done
