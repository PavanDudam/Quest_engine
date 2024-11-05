import streamlit as st
import pandas as pd
from groq import Groq
from quesytEngine_db import save_query_result, get_recent_results

# Initialize Groq client with API key
client = Groq(api_key="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")

st.title("QuestEngine CSV Analyzer")
st.write("Upload a CSV file, and ask a question or request a summary based on the data.")

# File upload component
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file using pandas
    data = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.write(data.head())

    # Choose query type
    query_type = st.radio("What would you like to do?", ["Summarize CSV", "Ask a question"])

    # User input based on choice
    if query_type == "Ask a question":
        user_query = st.text_input("Enter your query:")
    else:
        user_query = "Summarize the CSV file."

    # Submit button
    if st.button("Submit"):
        # Prepare the prompt
        prompt = f"{user_query}\nData Preview:\n{data.head().to_string()}"

        # Call the API using the Groq client with streaming enabled
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Collect streaming response chunks
            answer = ""
            for chunk in completion:
                answer += chunk.choices[0].delta.content or ""

            st.write("Response:")
            st.write(answer)

            # Save the query and result to MongoDB
            data_preview = data.head().to_dict()
            save_query_result(user_query, answer, data_preview)
            st.success("Query and result saved to the database.")

        except Exception as e:
            st.error(f"Error in model response: {e}")

# Display recent results from MongoDB
st.write("Previous results from MongoDB:")
try:
    documents = get_recent_results()
    for doc in documents:
        st.write(doc)
except Exception as e:
    st.error(f"Error retrieving from MongoDB: {e}")

