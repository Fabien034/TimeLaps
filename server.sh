#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

tmux new-window -t $SESSION:1 -n 'ServeurTimeLaps'
tmux send-keys "python /home/spm/TimeLaps/server.py" C-m

# Attach to session
tmux -2 attach-session -t $SESSION
