#!/bin/bash
SESSION=$USER

test -f ~/TimeLaps/ConfigServer
if [ $?=1 ];then
    python ~/TimeLaps/FichierConfig.py
fi

tmux -2 new-session -d -s $SESSION

tmux new-window -t $SESSION:1 -n 'TimeLaps'
tmux send-keys "python /home/pi/TimeLaps/CapturePhoto.py" C-m
tmux split-window -v
tmux resize-pane -D 5
tmux send-keys " ssh -p 525 -t spm@77.147.64.38 tmux a || ssh -p 525 -t spm@77.147.64.38 tmux" C-m
tmux select-pane -t 0
tmux split-window -h
tmux resize-pane -R 10
tmux send-keys "python /home/pi/TimeLaps/TransfertFichier.py" C-m
tmux split-window -v
tmux send-keys "python /home/pi/TimeLaps/ListDossierAttente.py" C-m

# Attach to session
tmux -2 attach-session -t $SESSION
