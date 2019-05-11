
# Import plotly libraries
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
# set plot.ly to run offline in notebook mode
plotly.offline.init_notebook_mode()
# set configuration file
plotly.io.orca.config.executable = '/Users/stephengodfrey/anaconda3/envs/dsi/bin/orca'


# Set up a plotly scatter plot
class scatter_plot_plotly:
	"""
	Create a plot.ly scatter plot with the purpose of customzing the look
	and feel of the chart and standardizing that look with other charts in 
	the notebook.

	Libraries and uses
	------------------
	The following libraries are used in this object:
		import plotly
		import plotly.plotly as py
		import plotly.graph_objs as go
		import plotly.io as pio

	The following is set to allow for offline notebook plotting:
		plotly.offline.init_notebook_mode()

	The location of the orca executable file is sepcified in this file:
		plotly.io.orca.config.executable = '/Users/stephengodfrey/anaconda3/envs/dsi/bin/orca'
	

	The class defaults to the font formats specified in the following variables.  For example,
		p_font_family = 'DejaVu Sans'
		p_font_size = 18
		p_font_size_u = 22
		p_font_size_l = 14
		p_font_color = '#7f7f7f'


	Parameters
	----------
	data : pandas dataframe
		Dataframe containing the x and y data.
	x_column : string
		Name of the column in the data dataframe to use as the x-axis values
		of the chart.
	y_columns : list
		Names of the columns in the data dataframe to use as the y-axis values
		of the chart where multiple sactter plots can be placed on the same 
		graph.
	mode : string
		Corresponds to the plot.ly scatter mode.  Values = 'lines', 'markerts', 'lines-markers'
	dual_axes : boolean
		Employ a single or dual y-axes.  True sets to y-axes, false to a single x-axis.
	c_title : string
		Chart title.
	x_axis_title : string
		Title applied to the x-axis.
	y_axis_title : string, list
		Title applied to the y-axis or y-axes.  If value is set to a list, the first item is
		applied to the left y-axis and the second is applied to the right  y-axis.
	show_legend : boolean
		Variable to control the display of the legend.  A value of true will display the legend
		and a false value will hide it.
	out_file : string
		Name and path for the file to save the output.  If value is '', no file is saved.
	
	**kwargs : dict
		font_family: string
			Name of the font family to apply to the graph.  See this link for a listing of possible 
			fonts: http://jonathansoma.com/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/)
		font_size : integer
			Size of the base font in the plot.
		font_size_u : integer
			Size of the upper font used for selected features in the plot.
		font_size_l : integer
			Size of the lower font used for selected features in the plot.
		font_color : string
			Font color to be used in the plot.


	"""
	_defaults = {
		'font_family': 'DejaVu Sans',
		'font_size': 18,
		'font_size_u' :22,
		'font_size_l': 14,
		'font_color':'#7f7f7f'
	}

	data = None
	x_column = ''
	y_columns = []
	mode  = ''
	dual_axes = False
	c_title  = ''
	x_axis_title = ''
	y_axis_title = ''
	show_legend = True
	out_file = ''
	# font_family = 'DejaVu Sans'
	# font_size = 18
	# font_size_u = 22
	# font_size_l = 14
	# font_color = '#7f7f7f'

	def __init__(self, data = None, x_column = '', y_columns = [], 
				mode = '', dual_axes = False, c_title = '',  x_axis_title = '',
				y_axis_title = '', show_legend = True, out_file = '',
				**kwargs):

				# font_family = p_font_family, font_size = p_font_size,
				# font_size_u = p_font_size_u, font_size_l = p_font_size_l, 
				# font_color = p_font_color):
		self.__dict__.update(self._defaults)
		self.__dict__.update(kwargs)

		self.data = data
		self.x_column = x_column
		self.y_columns = y_columns
		self.mode = mode
		self.dual_axes = dual_axes 
		self.c_title =  c_title
		if type(y_axis_title)==str:
			self.y_axis_title = [y_axis_title]
		else:
			self.y_axis_title = y_axis_title
		self.x_axis_title = x_axis_title       
		self.show_legend = show_legend
		self.out_file = out_file
		import plotly.graph_objs as go


		# self.font_family = font_family
		# self.font_size = font_size
		# self.font_size_u = font_size_u
		# self.font_size_l = font_size_l
		# self.font_color = font_color

	def create_traces(self):
		# For each col in the tuple list build a trace
		traces = []
		if len(self.y_columns)==2 and self.dual_axes == True:
			y_axis=['y1','y2']
		else:
			y_axis=['y1'] * len(self.y_columns)
		    
		for (i,col) in enumerate(self.y_columns):
			trace = go.Scatter(
				x = self.data[self.x_column],
				y = self.data[col[0]],
				mode = self.mode,
				name = col[1],
				yaxis=y_axis[i]
			)
			traces.append(trace)
		return traces

	# Return the font settings corresponding to where on the chart they apply
	def set_font(self, where = ''):
		if where == 'plot':
			return dict(family=self.font_family, size=self.font_size, color=self.font_color)
		elif where == 'title':
			return dict(family=self.font_family, size=self.font_size_u, color=self.font_color)
		elif where == 'tick':
			return dict(family=self.font_family, size=self.font_size_l, color=self.font_color)
		else:
			return ''

	# Define the layout settings
	def define_layout(self):
	    # Define the layout object
		if self.dual_axes == False or len(self.y_columns) != 2:
			gl = go.Layout(
				title=go.layout.Title(
					text=self.c_title,
					font=self.set_font(where='title'),
					xref='paper',
					x=0
				),
				xaxis=go.layout.XAxis(
					title=go.layout.xaxis.Title(
						text=self.x_axis_title,
						font=self.set_font(where='plot')
					),
					tickfont=self.set_font(where='tick')
				),
				yaxis=go.layout.YAxis(
					title=go.layout.yaxis.Title(
						text=self.y_axis_title[0],
						font=self.set_font(where='plot')
	 				),
					tickfont=self.set_font(where='tick')
				),
				legend=go.layout.Legend(
					x=0.0, y=1.1,
					font=self.set_font(where='plot')
				),
				showlegend = self.show_legend
			)
		else:
			gl = go.Layout(
				title=go.layout.Title(
					text=self.c_title,
					font=self.set_font(where='title'),
					xref='paper',
					x=0
				),
				xaxis=go.layout.XAxis(
					title=go.layout.xaxis.Title(
						text=self.x_axis_title,
						font=self.set_font(where='plot')
					),
					tickfont=self.set_font(where='tick')
				),
				yaxis=go.layout.YAxis(
					title=go.layout.yaxis.Title(
						text=self.y_axis_title[0],
						font=self.set_font(where='plot')
					),
					tickfont=self.set_font(where='tick')
				),            
				yaxis2=go.layout.YAxis(
					title=go.layout.yaxis.Title(
						text=self.y_axis_title[1],
						font=self.set_font(where='plot')
					),
					tickfont=self.set_font(where='tick'),
					overlaying='y',
					side='right'
				),
				legend=go.layout.Legend(
					x=0.0, y=1.1,
					font=self.set_font(where='plot')
				),
				showlegend = self.show_legend
			) 
		return gl

	# Create the plot
	def draw_plot(self):
	 	# Draw the plot
		plot_figure = go.Figure(data = self.create_traces(), layout = self.define_layout())
		if self.out_file != '':
			pio.write_image(fig = plot_figure, file = self.filename)
		plotly.offline.iplot(plot_figure)
