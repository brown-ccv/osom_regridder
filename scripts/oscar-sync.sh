# Run this script on your machine to sync a the directory on 
# Oscar with local changes.

USERNAME="amurph40"

rsync -azvp --progress . $USERNAME@ssh.ccv.brown.edu:~/osom_regridder