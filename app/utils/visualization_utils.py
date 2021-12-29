import plotly.graph_objects as go


def get_bar_chart(x, y, orientation: str = 'h') -> go.Figure:
    """
    Returns an bar chart Plotly graphing object Figure
    :return:
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y, orientation=orientation))
    fig.update_layout(
        xaxis=dict(title="Sender Index"),
        yaxis=dict(title="Sender", autorange="reversed"),
        title="Number of Emails By Sender",
        autosize=False,
        height=2500,
        width=1600
    )
    return fig


def cumulative_count_plot(x, y, fill: str = "tozeroy") -> go.Figure:
    """
    Returns an instance of go.Figure with a plot of cumulative email count
    :param x:
    :param y:
    :param fill:
    :return:
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, fill=fill))

    fig.update_layout(
        xaxis=dict(tickmode='linear', title="Sender Index", tick0=0, dtick=100),
        yaxis=dict(title="Cumulative Email Count"),
        title="Cumulative Email Count by index of Sender"
    )

    return fig
