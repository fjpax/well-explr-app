import dash

from dash import Input, Output, State, html, Dash, callback, dcc,dash_table
from dash import Input, Output, State, html




app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Chatbot Assistant'),
    dcc.Textarea(id='conversation', value='', readOnly=True, style={'width': '100%', 'height': '200px'}),
    html.Div([
        dcc.Input(id='input-field', type='text', placeholder='Type your message...', style={'width': '80%'}),
        html.Button('Send', id='send-button', n_clicks=0, style={'marginLeft': '10px'})
    ], style={'display': 'flex', 'alignItems': 'center'})
], style={'width': '400px', 'margin': 'auto'})

@callback(
    [Output('conversation', 'value'), Output('input-field', 'value')],
    [Input('send-button', 'n_clicks')],
    [State('input-field', 'value'), State('conversation', 'value')]
)
def update_conversation(n_clicks, message, conversation):
    if n_clicks > 0:
        # Append the user's message to the conversation
        conversation += f'User: {message}\n'
        # Process the user's message and generate a response
        response = 'Bot: This is the response to your message.\n'
        # Append the bot's response to the conversation
        conversation += response
        return conversation, ''
    
    return conversation, None

if __name__ == '__main__':
    app.run_server(debug=True)