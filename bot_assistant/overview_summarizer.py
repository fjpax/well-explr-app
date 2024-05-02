import pandas as pd
import openai
import os
openai.api_key=os.environ.get('OPENAI_API_KEY')
def summarize_dataframe(df, user_query):
    GPT_MODEL = "gpt-4-turbo-2024-04-09"  # Replace with your desired model
    
    columns = ['wlbDrillingOperator', 'wlbPurpose', 'wlbStatus', 'wlbContent', 'wlbWellType']
    normalized_counts = {column: (df[column].value_counts(normalize=True) * 100).round(2) for column in columns}
    data_string = str(normalized_counts)

    instruction = "Given the data containing value counts as percentages for each column in a DataFrame, please provide a brief summary highlighting the most significant findings in a list format. Include some number results for easy reading. Focus on key trends, dominant values, or notable disparities in the data across different columns.  Adjust your summary based on the user query."
    message ="User query:" + user_query+ "\n\n"+ "This is data:\n\n" + data_string
    prompt_message = [{"role": "system", "content": instruction}, {"role": "assistant", "content": message}]

    # Ensure you have set your API key in your environment or replace 'YOUR_API_KEY' with your actual key


    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        temperature=0.0,
        messages=prompt_message,
        max_tokens=500,
    )

    return response.choices[0].message['content']

def summarize_any_dataframe(df, user_query):
    GPT_MODEL = "gpt-4-turbo-2024-04-09"  # Replace with your desired model
    
    columns = df.columns
    #normalized_counts = {column: (df[column].value_counts(normalize=True) * 100).round(2) for column in columns}
    #convert df to dict
    df_dict = df.to_dict()
    data_string = str(df_dict)

    instruction = "Given the data containing columns and values in a DataFrame, Please provide a brief summary highlighting the most significant findings in a list format. Include some number results for easy reading. Focus on key trends, dominant values, or notable disparities in the data across different columns.  Adjust your summary based on the user query."
    message ="User query:" + user_query+ "\n\n"+ "This is data:\n\n" + data_string
    prompt_message = [{"role": "system", "content": instruction}, {"role": "assistant", "content": message}]

    # Ensure you have set your API key in your environment or replace 'YOUR_API_KEY' with your actual key


    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        temperature=0.0,
        messages=prompt_message,
        max_tokens=500,
    )

    return response.choices[0].message['content']

