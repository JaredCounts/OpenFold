# OpenFold
## Authors
Jared, Hunmin, and Anne

## Instructions
From command line or terminal, type `python make_cuts.py input.stl output.svg params.ini`

This will generate a svg file of cuts generated from the stl file using parameters from params.ini.

## TODO
### FEATURES
* Visualizer
	* Maybe a way to load stl files and export svg files via the visualizer?
	* Add buttons and sliders for parameters
	* A non-wireframe mode (ie. have slices not see-through)
	* A proper perspective view.
	* Clean up view logic (use transformation matrices)
* Improved layout engine (better packing)
	* Can better pack polygons on the same slice that aren't connected.
	* Can also do circle-packing style fitting.
* Lovepop style notching (alternating sides)
* A way to export straight to DXF
* Detect notches that are too close to an edge on the side
* Notches don't line up nicely with polygon edge (maybe have the notch go farther)

### OPTIMIZATIONS
* Data structures could improve intersection tests
* Visualizer should use sprites instead of drawing segments manually.

### BUGS
* Slicer skipping axis aligned segments.
* If a whole triangle is on a slice, which segments from it do we add, if any?
* Notches skipped when there's an odd number of intersections
* Segments are duplicated?
* Some parts are floating in air -- a simple graph search can check for connectedness.

### CODE
* Rename 'index' to 'axis' when referring to specific vector coefficients to be more clear
* Folders - eg. /pipeline, /math, etc
* Consistent naming (instead of sometimes using camel casing and sometimes using '_')
	* http://stackoverflow.com/a/159745/6153561
* Just use numpy for vectors, maybe?
* Better transformation engine (ie. so we don't have to add offset every time in make_cuts)
* Convert "segment list" in svg to "paths" for better tracing.

## References
* [The Creation of V-fold Animal Pop-Up Cards from 3D Models Using a Directed Acyclic Graph](http://link.springer.com/chapter/10.1007%2F978-3-642-35473-1_47)
* [Multi-style Paper Pop-up Designs from 3D Models
](https://www.comp.nus.edu.sg/~lowkl/publications/multistyle_popup_eg2014.pdf)
* [crdbrd: Shape Fabrication by Sliding Planar Slices
](http://cybertron.cg.tu-berlin.de/kristian/files/crdbrd.pdf)
* [Fabrication-aware Design with Intersecting Planar Pieces
](http://lgg.epfl.ch/publications/2013/PlanarPieces/paper.pdf)
* [Automatic Paper Sliceform Design
from 3D Solid Models](https://www.comp.nus.edu.sg/~lowkl/publications/sliceform_tvcg2013_lowres.pdf)