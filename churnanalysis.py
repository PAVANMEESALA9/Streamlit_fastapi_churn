# import requests
# import streamlit as st

# def main():
#     st.title("Churn Analysis Q&A")

#     # Fetch distinct questions from FastAPI endpoint
#     API_URL_distinct_questions = 'http://localhost:8000/getQuestions'
#     try:
#         response = requests.get(API_URL_distinct_questions)
#         response.raise_for_status()  # Raise error for bad status codes
#         data = response.json()
#         distinct_questions = data.get("Questions", [])
#         distinct_analysis = data.get("Analysis", [])
#     except (requests.RequestException, ValueError) as e:
#         st.error(f"Error retrieving data: {e}")
#         return
    
    

#     # Display dropdown to select question
#     selected_question = st.selectbox("Select a question:", distinct_questions)

#     # Fetch analysis and query result for selected question from FastAPI endpoint
#     API_URL_get_query = 'http://localhost:8000/getquery'
#     try:
#         response = requests.get(API_URL_get_query, params={"Question": selected_question})
#         response.raise_for_status()  # Raise error for bad status codes
#         query_result = response.json()
#         analysis = query_result.get("Analysis", "")
#         query = query_result.get("Query", "")
        
#     except (requests.RequestException, ValueError) as e:
#         st.error(f"Error retrieving data: {e}")
#         return
    
#     #Filter analysis based on selected question
#     filtered_analysis = [analysis for question, analysis in zip(distinct_questions, distinct_analysis) if question == selected_question]

#     # Display analysis, query, and table upon button click
#     if st.button("Get Insight"):
#         st.text("Insight:")
#         st.success(filtered_analysis)

#         st.subheader("Query:")
#         st.text(query)

#         st.subheader("Table:")
#         # Here you can display the table based on the query_result if needed

# if __name__ == "__main__":
#     main()



import streamlit as st
import requests
import pandas as pd

# Streamlit UI
def main():
    st.title("Churn Analysis Q&A")

    # Fetch distinct questions from FastAPI endpoint
    API_URL_distinct_questions = 'http://localhost:8000/getQuestions'
    try:
        response_questions = requests.get(API_URL_distinct_questions)
        response_questions.raise_for_status()  # Raise error for bad status codes
        data_questions = response_questions.json()
        distinct_questions = data_questions.get("Questions", [])
        distinct_analysis = data_questions.get("Analysis", [])
    except (requests.RequestException, ValueError) as e:
        st.error(f"Error retrieving questions: {e}")
        return

    # Display dropdown to select question
    selected_question = st.selectbox("Select a question:", distinct_questions)

    # Filter analysis based on selected question
    filtered_analysis = [analysis for question, analysis in zip(distinct_questions, distinct_analysis) if question == selected_question]

    # Fetch table data for selected question from FastAPI endpoint
    API_URL_table_data = 'http://localhost:8000/getTableData'
    try:
        response_table_data = requests.get(API_URL_table_data, params={"question": selected_question})
        response_table_data.raise_for_status()  # Raise error for bad status codes
        table_data = response_table_data.json()
        columns_list = table_data.get("headers", [])
        values_list = table_data.get("data", [])
    except (requests.RequestException, ValueError) as e:
        st.error(f"Error retrieving table data: {e}")
        return

    # Retrieve answer and data upon selection
    if st.button("Get Insight"):
        st.text("Insight:")
        st.success("\n".join(filtered_analysis))
        st.subheader("Table:")
        df = pd.DataFrame(values_list, columns=columns_list)
        st.dataframe(df.set_index(df.columns[0]))

if __name__ == "__main__":
    main()









# import streamlit as st
# import requests
# import pandas as pd

# st.markdown("""
#         <style>
#             .st-ef {
#                 padding-top: 1rem;
#                 padding-bottom: 2rem;
#                 padding-left: 0rem;
#                 padding-right: 0rem;
#             }
#         </style>
#         """, unsafe_allow_html=True)

# # Streamlit UI
# def main():
#     API_URL_distinct_questions = 'http://localhost:8000/getQuestions'
#     API_URL_table_data = 'http://localhost:8000/getTableData'
#     try:
#         response_questions = requests.get(API_URL_distinct_questions)
#         response_questions.raise_for_status()  # Raise error for bad status codes
#         data_questions = response_questions.json()
#         distinct_questions = data_questions.get("Questions", [])
#         distinct_analysis = data_questions.get("Analysis", [])

#         response_table_data = requests.get(API_URL_table_data)
#         response_table_data.raise_for_status()  # Raise error for bad status codes
#         table_data = response_table_data.json()
#         columns_list = table_data.get("columns", [])
#         values_list = table_data.get("values", [])
#     except (requests.RequestException, ValueError) as e:
#         st.error(f"Error retrieving data: {e}")
#         return

#     st.title("Churn Analysis Q&A")
#     # Display dropdown to select question
#     selected_question = st.selectbox("Select a question:", distinct_questions)

#     # Filter analysis based on selected question
#     filtered_analysis = [analysis for question, analysis in zip(distinct_questions, distinct_analysis) if question == selected_question]

#     # Retrieve answer and data upon selection
#     if st.button("Get Insight"):
#         st.text("Insight:")
#         st.success("\n".join(filtered_analysis))

#     st.subheader("Table:")
#     # Display table using st.table()
#     if columns_list and values_list:
#         df = pd.DataFrame(values_list, columns=columns_list)
#         st.table(df)

# if __name__ == "__main__":
#     main()





