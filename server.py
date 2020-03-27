from flask import Flask, render_template, request
import seaborn as sb
import plotly
import plotly.graph_objs as go
# Data dari flask di kirim ke browser dalam bentuk json
import json

app = Flask(__name__)

# Sumber data
dfTips = sb.load_dataset('tips')

# # # # # # # # # #
# HISTOGRAM & BOX #
# # # # # # # # # #

def category_plot(cat_plot = 'histoplot', cat_x = 'sex', cat_y = 'total_bill', estimator ='count'):
    
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

@app.route('/')
def index():
    plot = category_plot()

    # list dropdown
    list_plot = [('histoplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]
    list_y = [('total_bill', 'Total Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]

    return render_template(
        'category.html', 
        plot=plot, 
        focus_plot='histoplot', 
        focus_x='sex', 
        focus_y='total_bill', 
        focus_estimator='count',
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_estimator
    )

@app.route('/cat_fn')
def cat_fn():
    cat_plot = request.args.get('cat_plot')
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y') # total_bill
    estimator = request.args.get('estimator') # avg

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

    # list dropdown
    list_plot = [('histoplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]
    list_y = [('total_bill', 'Total Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]
                                                                                            
    return render_template(
        'category.html', 
        plot=plot, 
        focus_plot=cat_plot, 
        focus_x=cat_x, 
        focus_y=cat_y, 
        focus_estimator=estimator,
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_estimator
    )


# # # # # #
# SCATTER # 
# # # # # #

def scatter_plot(cat_x, cat_y):

    # membuat plot, nama variable tidak harus 'data'
    data_source = [
        go.Scatter(
            x = dfTips[cat_x],
            y = dfTips[cat_y],
            mode = 'markers'
        )
    ]

    # membuat layout, nama variable tidak harus 'layout'
    layout_source = go.Layout(
        title='Scatter',
        title_x= 0.5,
        xaxis = {"title" : cat_x},
        yaxis = {"title" : cat_y}
    )

    # Gabungkan antara plot dengan layout
    # variable yang menyimpan dictionary tidak harus final
    # dict harus memiliki key 'data' dan 'layout
    final = {"data" : data_source, "layout" : layout_source}

    # hasil json yang akan dikirim tidak harus menggunakan 'graphJSON'
    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

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
    
    # Kirim ke browser
    return render_template('scatter.html', plot=plot, focus_x=cat_x, focus_y=cat_y)


# # # #
# PIE #
# # # #

def pie_plot(hue):

    # result : list of tupple dari penghitungan banyak data secara unique 
    result = dfTips[hue].value_counts()

    labels_source = []
    values_source = []

    for item in result.iteritems():
        labels_source.append(item[0])
        values_source.append(item[1])

    data_source = [
        go.Pie(
            labels=labels_source,
            values=values_source
        )
    ]

    layout_source = go.Layout(
        title='Pie',
        title_x=0.5
    )

    final = {"data" : data_source, "layout" : layout_source}

    # hasil json yang akan dikirim tidak harus menggunakan 'graphJSON'
    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue_source = request.args.get('hue')

    # Saat diakses melalui link, hue_sorce akan bernilai None
    if hue_source == None:
        hue_source = 'sex'

    plot_source = pie_plot(hue_source)

    return render_template('pie.html', plot=plot_source, focus_hue=hue_source)


if __name__ == '__main__':
    app.run(debug=True)