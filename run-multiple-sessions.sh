#!/bin/bash

tmux new-session -s llm -d
for (( i=0; i<$1; i=i+1 )) do
  tmux new-window -t llm ./run.sh
done

