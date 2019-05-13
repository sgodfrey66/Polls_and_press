
# Import plotly libraries
import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
# set plot.ly to run offline in notebook mode
plotly.offline.init_notebook_mode()
# set configuration file
plotly.io.orca.config.executable = '/Users/stephengodfrey/anaconda3/envs/dsi/bin/orca'


# Set up a plotly scatter plot
class ScatterPlotPlotly:
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
	

	Parameters
	----------
	data : pandas dataframe
		Dataframe containing the x and y data.
	x_column : string
		Name of the column in the dataframe to use as the x-axis values
		of the chart.
	y_columns : list of tuples
		Names of the columns in the dataframe to use as the y-axis values
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

	methods
	----------
	create_traces 
		Create plotly traces for graphing.	
		Inputs: 
			none
		output: 
			list of trace objects
	set_font
		Set font to be used in a particular graphing object.
		Inputs:
			where : string
		Output:
			dictionary of font parameters
	define_layout
		Create layout object to be used in draw_plot method.
		Inputs:
			none
		Output:
			Plotly layout object
	draw_plot
		Draw the ROC curve and create the confusion matrix table.
		Inputs:
			none
		Output:
			In notebook graph


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

	def __init__(self, data = None, x_column = '', y_columns = [], 
				mode = '', dual_axes = False, c_title = '',  x_axis_title = '',
				y_axis_title = '', show_legend = True, out_file = '',
				**kwargs):
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


# ROC and confusion matrix table plot.ly
class ClassSummaryPlotly:
	"""
	Create an ROC plot and a confusion matrix table for a classification model using plot.ly. The
	chart is an xy scatter with the y-axis equal to the true positive rates (TPR) plotted versus 
	an x-axis equal to the false positive rate (FPR).  The confusion table contains the actual and 
	predicted values in the format of sklearn.

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
	

	Parameters
	----------
	data : pandas dataframe
		Dataframe containing the FPR and TPR data.
	fpr_column : string
		A two-value tuple with the name and alias of the column in the dataframe with the FPR data.
	tpr_columns : list of tuples
		Names of the columns in the dataframe to use as the y-axis values
		of the chart where multiple tpr plots can be placed on the same graph.
	conf_matrix : np.array
		Array containing confusion matrix values in the format from sklearn.  Each row of the array
		are the actual values sorted in ascending order.  Each column of these rows representation the
		predictions for that actual value.  Values along the diagonal are the correct predictions.
	class_names : list of strings
		Names of the classes.
	mode : string
		Corresponds to the plot.ly scatter mode.  Values = 'lines', 'markerts', 'lines-markers'
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
		table_fill_color : string
			Table fill color.
		table_line_color : string
			Table line color.

	methods
	----------
	create_traces 
		Create plotly traces for graphing.	
		Inputs: 
			none
		output: 
			list of trace objects
	set_font
		Set font to be used in a particular graphing object.
		Inputs:
			where : string
		Output:
			dictionary of font parameters
	define_layout
		Create layout object to be used in draw_plot method.
		Inputs:
			none
		Output:
			Plotly layout object
	draw_plot
		Draw the ROC curve and create the confusion matrix table.
		Inputs:
			none
		Output:
			In notebook graph

	"""
	_defaults = {
		'font_family': 'DejaVu Sans',
		'font_size': 18,
		'font_size_u' :22,
		'font_size_l': 14,
		'font_color':'#7f7f7f',
		'table_fill_color':'#FFFFFF',
		'table_line_color': '#506784'
	}

	data = None
	fpr_column = ''
	tpr_columns = []
	conf_matrix = 0
	class_names = []
	mode  = ''
	c_title  = ''
	x_axis_title = ''
	y_axis_title = ''
	show_legend = True
	out_file = ''

	def __init__(self, data = None, fpr_column = '', tpr_columns = [], conf_matrix = 0,
				class_names = [], mode = '', c_title = '',  x_axis_title = '',
				y_axis_title = '', show_legend = True, out_file = '',
				**kwargs):

		self.__dict__.update(self._defaults)
		self.__dict__.update(kwargs)

		self.data = data
		self.fpr_column = fpr_column
		self.tpr_columns = tpr_columns
		self.conf_matrix = conf_matrix
		self.class_names = class_names
		self.mode = mode
		self.c_title =  c_title
		self.y_axis_title = y_axis_title
		self.x_axis_title = x_axis_title       
		self.show_legend = show_legend
		self.out_file = out_file


	def create_traces(self):
		# For each col in the tuple list build a trace
		traces = []
		
		# Indentify special cases of lines and apply dash or weight
		for col in self.tpr_columns:
			if col[0] == 'all':
				line = dict(
					width = 4)
			elif col[0] == 'fpr':
				line = dict(
					width = 4,
					dash = 'dash')
			else:
				line = dict(
					width = 2)

			trace = go.Scatter(
				x = self.data[self.fpr_column],
				y = self.data[col[0]],
				mode = self.mode,
				name = col[1],
				yaxis = 'y1',
				line = line
			)
			traces.append(trace)

		# Calculate the accuracy from the confusion matrix
		# and create a trace for it
		acc_score = int(100*sum([cm[i] for (i,cm) in enumerate(self.conf_matrix)])/\
				sum([sum(list(cm)) for cm in self.conf_matrix]))
		accuracy_trace = go.Scatter(
			x=[.62],
			y=[ .3],
			text=[f'Accuracy: {acc_score}%'],
			mode='text',
			textfont = self.set_font(where = 'title'),
			showlegend = False
		)

		traces.append(accuracy_trace)

		#build a trace for the confusion matrix
		# https://plot.ly/python/reference/?_ga=2.75025938.1687764534.1557537433-1742474213.1555648266#table
		table_trace = go.Table(
			# name = 'Confusion Matrix',
			domain=dict(x=[0.6, 1.0],
						y=[0.3, 0.8]),
			columnwidth = [15] * len(self.conf_matrix),
			# columnorder=[0, 1, 2, 3, 4],
			header = dict(height = 50,
				# values = ['<b>' + class_ + '</b>' for class_ in self.class_names],
				values = ['Matrix'],
				line = dict(color = self.table_fill_color),
				align = ['left'] * len(self.class_names),
				font = self.set_font(where = 'title'),
				fill = dict(color = self.table_fill_color)),
			cells = dict(values = [['Result'] + self.class_names] + 
						[[class_] + list(row) for (class_,row) 
						in zip(self.class_names, self.conf_matrix)],
				line = dict(color = self.table_line_color),
				align = ['center'] * len(self.conf_matrix + 1),
				font = self.set_font(where = 'plot'),
				# format = [None] + [", .2f"] * 2 + [',.4f'],
				# prefix = [None] * 2 + ['$', u'\u20BF'],
				# suffix=[None] * 4,
				height = 27,
				fill = dict(color = self.table_fill_color)
				# ,
				# fill = dict(color = self.table_fill_color)
				)
			)


		traces.append(table_trace)

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
				tickfont=self.set_font(where='tick'),
				domain = [0.0, 0.5]
			),
			yaxis=go.layout.YAxis(
				title=go.layout.yaxis.Title(
					text=self.y_axis_title,
					font=self.set_font(where='plot')
 				),
				tickfont=self.set_font(where='tick'),
				domain = [0.0, 1.0]
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

