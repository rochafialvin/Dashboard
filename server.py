from flask import Flask, render_template, request
import seaborn as sb
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

def category_plot(cat_plot = 'histoplot', cat_x = 'sex', cat_y = 'total_bill', estimator = 'count'):
    
    dfTips = sb.load_dataset('tips')

    data = [
        go.Histogram(
            x = dfTips[cat_x], # series
            y = dfTips[cat_y], # series
            histfunc=estimator
        )
    ]

    layout = go.Layout(
        title="Histogram",
        title_x=0.5,
        xaxis={"title" : cat_x},
        yaxis=dict(title=cat_y)
    )

    final = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/')
def index():
    plot = category_plot()

    return render_template('index.html', plot=plot)


if __name__ == '__main__':
    app.run(debug=True)