# Dead-Shortcut-Killer
Scans your computer for dead shortcuts and asks if you want them deleted

# 🧹 DeadShortcut Sweeper

Tiny Windows automation script that scans your desktop for broken `.lnk` files (shortcuts that point to nothing), logs them, and asks if you want to delete them. 

Made this to clean up my mess, but you might find it helpful too.


### What It Does:
- Scans your Desktop for all `.lnk` shortcut files  
- Checks if the target path exists  
- Logs any broken ones to `dead_shortcuts_log.txt`  
- Gives you a choice: delete them or leave them  
- If deleted, it logs what got removed too


### How to Use:
1. **Right-click CMD → Run as Administrator**  
2. `cd` into the folder where the script is  
3. Run it:

python "Shortcut_Sweeper_1.py"
