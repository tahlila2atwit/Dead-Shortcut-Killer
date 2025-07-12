import os
import win32com.client

# get the path to the user's desktop
desk = os.path.join(os.environ["USERPROFILE"], "Desktop")

# holds all the dead shortcut file paths
dead_lnks = []

# create shell object to access shortcut targets
shell = win32com.client.Dispatch("WScript.Shell")

# loop through each file on the desktop
for f in os.listdir(desk):

  # full path to the shortcut file
  f_path = os.path.join(desk, f)

  # only check if it's a .lnk (shortcut) file
  if f.lower().endswith(".lnk"):

    try:
      # get the shortcut target (where the .lnk points to)
      shrt = shell.CreateShortcut(f_path)
      tgt = shrt.Targetpath

      # if the target doesn't exist, add it to the dead list
      if not os.path.exists(tgt):
        dead_lnks.append((f_path, tgt))  # store both shortcut and its target

    except:
      # just skip if something fails
      pass

# write all dead shortcuts to a log file
with open("dead_shortcuts_log.txt", "w") as log:

  for lnk, tgt in dead_lnks:
    log.write(f"[DEAD] {lnk} -> {tgt}\n")

# show how many were found
print(f"\nFound {len(dead_lnks)} dead shortcuts. Check 'dead_shortcuts_log.txt'.")

# ask if user wants to delete them
choice = input("\nDelete all dead shortcuts? (Y/N): ").strip().lower()

# if user says yes, delete them
if choice == "y":

  with open("dead_shortcuts_log.txt", "a") as log:
    log.write("\n[DELETED SHORTCUTS]\n")

    for lnk, _ in dead_lnks:
      try:
        os.remove(lnk)
        log.write(f"{lnk} deleted\n")
      except:
        pass

  print("\nDeleted all dead shortcuts.")

else:
  print("\nNo shortcuts were deleted.")
