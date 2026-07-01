# Jaynitor
A cleaner app for Archlinux that does not compromise on its looks (intended for Hyprland users)

## Inspiration, Scope, and Effect

**Inspiration**: Jaynitor is an on-going project to create an advanced utility for finding and clearing all types
of junk on an Archlinux system. The app revolves around the core principle of the Archlinux project, **KISS**
(*Keep it simple, stupid*). The architecture has been designed for usability, efficiency and aesthetic.

**The UI**: Jaynitor features a hand-made TUI coded in **Textual** and brought to life by **TUI Studio**.
The TUI is designed for aesthetics and to integrate and run flawlessly on a Hyprland environment without
disturbing the user's RICE. This addresses the need of visually stunning utilities among RICErs.

**Scope**: The scope and *effect* of Jaynitor has been planned in three phases named after their difficulty of
implementation as initially researched by the author @lord-of-the-strings.

### 1. EASY (cache/tools exist)
- pacman cache
- orphan packages
- AUR helper cache (yay/paru)
- flatpak leftovers
- Thumbnails cache

### 2. MEDIUM (junk/logic required)
- systemd journal logs
- pacnew/pacsave files
- stray configs
- giant language libraries mistakenly pushed to public repos cloned on the device
- broken symlinks
- unused apps
- heavy unused files
- duplicates
### 3. HARD (user protection)
Audit and verify AUR packages against supply chain risks

**NOTE**: This project is under active development. Your contributions are welcome. Fork this repo, check the scripts in 
utils/ and the commented Textual code in tui/, and open a PR today! All PRs will be merged after thorough
verification, please ensure that the final code does not cause a problem of any kind including aesthetic
in a custom RICEd Hyprland-on-Archlinux setup.
