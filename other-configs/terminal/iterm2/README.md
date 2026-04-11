# iTerm2

This folder tracks the main iTerm2 preferences plist:

- `com.googlecode.iterm2.plist`

Use the helper script to sync it:

```bash
./other-configs/terminal/iterm2/iterm2-sync.sh status
./other-configs/terminal/iterm2/iterm2-sync.sh export
./other-configs/terminal/iterm2/iterm2-sync.sh apply
```

What the script does:

- `export`: saves the current `com.googlecode.iterm2` defaults domain into this folder
- `apply`: imports the tracked plist and tells iTerm2 to load settings from this folder as its custom settings folder
- `status`: shows the tracked plist path and current iTerm2 custom-folder settings

Recommended flow:

1. On the source machine, run `export`.
2. Commit the updated plist.
3. On the target machine, clone the repo and run `apply`.
4. Quit and reopen iTerm2.

If you want edits in iTerm2's GUI to write back into this repo automatically, enable:

- `iTerm2 > Settings > General > Settings > Save changes to folder when iTerm2 quits`

If you need a full machine-to-machine migration beyond the main plist, use iTerm2's built-in:

- `Settings > General > Settings > Export/Import All Settings and Data`
