# blender-stl-reload
A simple helper add-on to reload STL files from disk, whenever these change.

## Warning

For now you can consider this a hack I'm using to load & reload STL files from build123d scripts to get an overview of part assemblies. The file watchdog mechanism is not yet implemented but will follow shortly
Use at your own risk. 

## Installation

- Download the stl_watcher.py file
- Edit > Preferences > Add-ons > Install Add-on & select the stl_watcher.py file
- Enable the add on

## Usage

- File > Import > STL Watcher 
- Toolbar: Update STLs (updates all STLs in place keeping position & orientation as well as materials) 

## Features

- Assign colors & names on import
- In-place reload of STL files, keeping orientation & materials

## Non features

- Linkages & mechanisms
- Multi-part upload. 
