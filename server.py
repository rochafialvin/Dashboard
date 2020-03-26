from flask import Flask, render_template, request
import seaborn as sb
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Histogram dan Box
def category_plot(cat_plot = 'histoplot', cat_x = 'sex', cat_y = 'total_bill', estimator = 'count'):
    
    dfTips = sb.load_dataset('tips')

    if cat_plot == 'histoplot':
        data = [
            go.Histogram(
                x = dfTips[cat_x], # series
                y = dfTips[cat_y], # series
                histfunc=estimator
            )
        ]

        title = 'Histogram'
    else :
        data = [
            go.Box(
                x = dfTips[cat_x], # series
                y = dfTips[cat_y], # series
            )
        ]

        title = 'Box'

    layout = go.Layout(
        title=title,
        title_x=0.5,
        xaxis={"title" : cat_x},
        yaxis=dict(title=cat_y)
    )

    final = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Scattter
def scatter_plot(cat_x, cat_y):

    dfTips = sb.load_dataset('tips')

    data = [
        go.Scatter(
            x = dfTips[cat_x],
            y = dfTips[cat_y],
            mode = 'markers'
        )
    ]

    layout = go.Layout(
        title='Scatter',
        title_x= 0.5,
        xaxis = {"title" : cat_x},
        yaxis = {"title" : cat_y}
    )

    final = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/')
def index():
    plot = category_plot()

    return render_template(
        'category.html', 
        plot=plot, 
        focus_plot='histoplot', 
        focus_x='sex', 
        focus_y='total_bill', 
        focus_estimator='count'
    )

@app.route('/cat_fn')
def cat_fn():
    cat_plot = request.args.get('cat_plot')
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    estimator = request.args.get('estimator')

    # Ketika kita klik menu 'Histogram & Box' di Navigasi
    if cat_plot == None and cat_x == None and cat_y == None and estimator == None:
        cat_plot = 'histoplot'
        cat_x = 'sex'
        cat_y = 'total_bill'
        estimator = 'count'

    # Ketika kita pindah dari boxplot (disabled) ke histogram
    if estimator == None:
        estimator = 'count'

    plot = category_plot(cat_plot, cat_x, cat_y, estimator)

    return render_template('category.html', plot=plot, focus_plot=cat_plot, focus_x=cat_x, focus_y=cat_y, focus_estimator=estimator )

@app.route('/scatt_fn')
def scatt_fn():
    # Memilih dari menu dropdown
    # Keduanya akan bernilai None hanya ketika kita mengunjungi via 'Scatter' menu di navbar
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')

    # Jika kita klick menu 'Scatter' pada navbar, keduanya akan bernilai None
    if cat_x == None and cat_y == None:
        cat_x = 'total_bill'
        cat_y = 'tip'

    plot = scatter_plot(cat_x, cat_y)
    
    return render_template('scatter.html', plot=plot)



if __name__ == '__main__':
    app.run(debug=True)