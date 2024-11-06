import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib
import seaborn as sns

matplotlib.use('Agg')

class Plotter:
    def __init__(self):
        """Initialize the Plotter class."""
        pass

    def _save_plot(self):
        """Save the current plot to a BytesIO object and close the plot."""
        try:
            img = io.BytesIO()
            plt.savefig(img, format='jpeg')  # Save as JPEG
            img.seek(0)  # Rewind the BytesIO object for reading
            plt.close()  # Close the plot to free up memory
            return img
        except Exception as e:
            print(f"Error in saving plot: {e}")
            return None

    def create_plot(self, df, data):
        """Create a plot based on the provided data dictionary."""
        plot_type = data.get('plot_type', None)

        # Map plot types to their respective methods
        plot_methods = {
            'line': self.line_plot,
            'bar': self.bar_plot,
            'scatter': self.scatter_plot,
            'histogram': self.histogram_plot,
            'pie': self.pie_chart,
            'heatmap': self.heatmap,
            'boxplot': self.boxplot,
            'violin': self.violin_plot
        }

        # Call the appropriate method based on plot_type
        plot_method = plot_methods.get(plot_type)

        if plot_method:
            try:
                return plot_method(df, **data)
            except Exception as e:
                print(f"Error in creating {plot_type} plot: {e}")
                return None
        else:
            print("Invalid plot type specified.")
            return None

    def line_plot(self, df, **kwargs):
        """Create a line plot."""
        try:
            x_data = df[kwargs.get('x_data', None)]
            y_data = df[kwargs.get('y_data', None)]

            #if x_data is None or y_data is None:
            #    raise ValueError("Both x_data and y_data must be provided.")

            plt.figure(figsize=kwargs.get('figsize', (8, 4)))
            plt.plot(x_data, y_data, color=kwargs.get('color', 'blue'), 
                     linestyle=kwargs.get('linestyle', '-'), 
                     marker=kwargs.get('marker', 'o'), 
                     label=kwargs.get('label', 'label_here'))

            plt.title(kwargs.get('title', 'Line Plot'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))
            plt.ticklabel_format(style='plain')

            #if kwargs.get('show_legend', True):
            #    plt.legend()
            plt.legend()

            return self._save_plot()  # Save and return the image
        except Exception as e:
            print(f"Error in line plot: {e}")
            return None

    def bar_plot(self, **kwargs):
        """Create a bar plot."""
        try:
            x_data = kwargs.get('x_data', None)
            y_data = kwargs.get('y_data', None)

            #if x_data is None or y_data is None:
            #    raise ValueError("Both x_data and y_data must be provided.")

            plt.figure(figsize=kwargs.get('figsize', (8, 4)))
            plt.bar(x_data, y_data, 
                    color=kwargs.get('color', 'blue'), 
                    label=kwargs.get('label', 'label_here'))

            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.title(kwargs.get('title', 'Bar Plot'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True), axis='y')  # Grid only on y-axis

            #if kwargs.get('show_legend', True):
            #    plt.legend()
            plt.legend()

            return self._save_plot()  # Save and return the image
        except Exception as e:
            print(f"Error in bar plot: {e}")
            return None

    def scatter_plot(self, df, **kwargs):
        """Create a scatter plot."""
        try:
            x_data = df[kwargs.get('x_data', None)]
            y_data = df[kwargs.get('y_data', None)]

            #if x_data is None or y_data is None:
            #    raise ValueError("Both x_data and y_data must be provided.")

            plt.figure(figsize=kwargs.get('figsize', (8, 4)))
            plt.scatter(x_data, y_data,
                        color=kwargs.get('color', 'blue'))

            plt.title(kwargs.get('title', 'Scatter Plot'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))

            #if kwargs.get('show_legend', True):
            #    plt.legend()
            plt.legend()

            return self._save_plot()  # Save and return the image
        except Exception as e:
            print(f"Error in scatter plot: {e}")
            return None

    def histogram_plot(self, df, **kwargs):
        """Create a histogram plot."""
        try:
            data = df[kwargs.get('data', None)]
            bins = kwargs.get('bins', 20)  # Default number of bins

            #if data is None:
            #    raise ValueError("Data must be provided.")

            plt.figure(figsize=kwargs.get('figsize', (8, 4)))
            plt.hist(data, bins=bins, 
                     color=kwargs.get('color', 'blue'), 
                     edgecolor='black', 
                     alpha=0.7)  # Slightly transparent bars

            plt.title(kwargs.get('title', 'Histogram'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'Frequency'))
            plt.grid(kwargs.get('grid', True))
            plt.legend()

            return self._save_plot()  # Save and return the image
        except Exception as e:
            print(f"Error in histogram plot: {e}")
            return None

    def pie_chart(self, df, **kwargs):
        """Create a pie chart."""
        try:
            sizes = df[kwargs.get('sizes', None)]
            labels = df[kwargs.get('labels', None)]
            explode = kwargs.get('explode', None)
            #explode = (0.1, 0.2, 0.3)  # This will explode the 1st slice by 0.1, the 2nd by 0.2, and the 3rd by 0.3

            #if sizes is None or labels is None:
            #    raise ValueError("Both sizes and labels must be provided.")

            plt.figure(figsize=kwargs.get('figsize', (8, 8)))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode, startangle=90, shadow=True)

            plt.title(kwargs.get('title', 'Pie Chart'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))
            plt.legend()

            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            return self._save_plot()  # Save and return the image
        except Exception as e:
            print(f"Error in pie chart: {e}")
            return None

    def heatmap(self, df, **kwargs):
        """Create a heatmap plot."""
        try:
            data = df[kwargs.get('columns', df.columns)]  # Use specified columns or entire dataframe
            plt.figure(figsize=kwargs.get('figsize', (8, 6)))
            sns.heatmap(data.corr(), annot=kwargs.get('annot', True), cmap=kwargs.get('cmap', 'viridis'))
            plt.title(kwargs.get('title', 'Heatmap'))
            
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))
            plt.legend()

            plt.tight_layout()

            return self._save_plot()
        except Exception as e:
            print(f"Error in heatmap: {e}")
            return None

    def boxplot(self, df, **kwargs):
        """Create a boxplot."""
        try:
            plt.figure(figsize=kwargs.get('figsize', (8, 6)))
            sns.boxplot(data=df[kwargs.get('columns', df.columns)],palette=kwargs.get("color","coolwarm"))    

            plt.title(kwargs.get('title', 'Boxplot'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))
            plt.legend()

            plt.tight_layout()

            return self._save_plot()
        except Exception as e:
            print(f"Error in boxplot: {e}")
            return None

    def violin_plot(self, df, **kwargs):
        """Create a violin plot."""
        try:
            plt.figure(figsize=kwargs.get('figsize', (8, 6)))
            sns.violinplot(data=df[kwargs.get('columns', df.columns)],palette=kwargs.get("color","coolwarm"))

            plt.title(kwargs.get('title', 'Violinplot'))
            plt.xlabel(kwargs.get('xlabel', 'xlabel_here'))
            plt.ylabel(kwargs.get('ylabel', 'ylabel_here'))
            plt.grid(kwargs.get('grid', True))
            plt.legend()

            plt.tight_layout()
            
            return self._save_plot()
        except Exception as e:
            print(f"Error in violin plot: {e}")
            return None
