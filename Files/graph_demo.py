from plotly.graph_objs import graphs
from plotly.offline import plot


def generate_plot(x_axis, y_axis):
    figure = graphs.Figure()
    scatter_plot = graphs.Scatter(x_axis, y_axis)
    figure.add_trace(scatter_plot)
    return plot(figure, output_type='div')


def generate_html(plot_html):
    html_content = '<html><head><title>Plot Demo</title></head><body>{}</body></html>'.format(plot_html)

    try:
        with open('plot_demo.html', 'w') as plot_file:
            plot_file.write(html_content)
    except (IOError, OSError) as file_io_error:
        print('Unable to generate plot file. Exception: {}'.format(file_io_error))


if __name__ == '__main__':
    plot_html = generate_plot([1, 2, 3], [4, 5, 6])
    generate_html(plot_html)
