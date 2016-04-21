# 6807-Project
## Authors
Jared, Hunmin, and Anne

## Instructions
To use, call `make_cuts(stlFile, svgOutput)` where `stlFile` is the file path to the stl file input and svgOutput is the desired svg file to output the cuts to.

## TODO
### FEATURES
* Come up with a neat project name
* Flexurizer
* Slice and model rendering
* Interactive UI
* Shape labeling for assembly
* Parameterize notch size, flexure size, densities, etc
	* Could parameterize based on material parameters (eg. material width, stiffness, etc)
* Improved layout engine (better packing)
* Lovepop style notching (alternating sides)

### BUGS
* Slicer missing axis aligned segments.
* Slices at origin getting skipped by slicer.
* Overlapping shapes on layout
* Notches skipped when there's an odd number of intersections

### CODE
* Separate vector operations from util.py
	* Or maybe just use numpy?
* Separate intersection stuff from util.py
	* intersect.py or something
* Rename 'index' to 'axis' when referring to specific vector coefficients to be more clear
* Folders - eg. /pipeline, /math, etc
* Consistent naming (instead of sometimes using camel casing and sometimes using '_')
	* http://stackoverflow.com/a/159745/6153561

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