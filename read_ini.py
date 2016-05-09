try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


def get_params(ini_file):
	# instantiate
	config = ConfigParser()

	# parse existing file
	config.read(ini_file)

	# read values from a section
	params = {}

	params['stl_scale'] = config.getfloat('stl', 'mm_per_unit')

	params['material_thickness'] = config.getfloat('material', 'thickness_mm')
	
	params['slice_density'] = config.getfloat('slicer', 'slices_per_mm')

	params['layout_margin'] = config.getfloat('layout', 'margin_mm')
	params['layout_width'] = config.getfloat('layout', 'max_row_width_mm')

	return params