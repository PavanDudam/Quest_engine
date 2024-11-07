import streamlit as st
import pandas as pd
from groq import Groq
from quesytEngine_db import save_query_result, get_recent_results

client = Groq(api_key="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")

st.title("QuestEngine CSV Analyzer")
st.write("Upload a CSV file, and ask a question or request a summary based on the data.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.write(data.head())

    query_type = st.radio("What would you like to do?", ["Summarize CSV", "Ask a question"])

    if query_type == "Ask a question":
        user_query = st.text_input("Enter your query:")
    else:
        user_query = "Summarize the CSV file."

    if st.button("Submit"):
        prompt = f"{user_query}\nData Preview:\n{data.head().to_string()}"

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

            answer = ""
            for chunk in completion:
                answer += chunk.choices[0].delta.content or ""

            st.write("Response:")
            st.write(answer)

            data_preview = data.head().to_dict()
            save_query_result(user_query, answer, data_preview)
            st.success("Query and result saved to the database.")

        except Exception as e:
            st.error(f"Error in model response: {e}")

st.write("Previous results from MongoDB:")
try:
    documents = get_recent_results()
    for doc in documents:
        st.write(doc)
except Exception as e:
    st.error(f"Error retrieving from MongoDB: {e}")
