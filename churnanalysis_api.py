# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from fastapi import FastAPI
# from fastapi.exceptions import HTTPException
# import pandas as pd
# from sqlalchemy.sql import select
# from sqlalchemy.sql import text
 
# app = FastAPI()
 
# Base = declarative_base()
 
# class YourModel(Base):
#     __tablename__ = 'Queries'  # Replace 'your_table_name' with your actual table name
 
#     id = Column(Integer, primary_key=True)
#     Questions = Column(String)
#     Analysis = Column(String)
#     Query = Column(String)
#     Insight = Column(String) 
 
# connection_string = 'mssql+pyodbc://devadmin:SqlServer123$@54.39.28.195,2552/Powerbi_Demo?driver=ODBC+Driver+17+for+SQL+Server'
 
# # Create the SQLAlchemy engine
# engine = create_engine(connection_string)
 
# Session = sessionmaker(bind=engine)
 
# # Create a session
# session = Session()
 
# @app.get("/getQuestions")
# def getQuestions():
 
#     quesDict = {}
#     quesList = []
#     analysisList = []
#     # Execute the query
#     query_result = session.query(YourModel).all()
    
#     for item in query_result:
#             quesList.append(item.Questions)
#             analysisList.append(item.Analysis)
    
#     quesDict["Questions"] = quesList
#     quesDict["Analysis"] = analysisList
#     return quesDict

# @app.get("/getquery")
# def getquery(Question: str):
#     # Query the database to find the query corresponding to the input question
#     query_result = session.query(YourModel).filter_by(Questions=Question).first()
#     print(query_result)

#     if query_result is None:
#         # If no matching question found, raise an HTTPException with 404 status code
#         raise HTTPException(status_code=404, detail="Question not found")
    
#     # Return the corresponding query
#     return {"Query": query_result.Query}





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI,HTTPException,Response
import pyodbc
from pydantic import BaseModel
from typing import List, Dict
import json
from decimal import Decimal
 
app = FastAPI()
 
Base = declarative_base()
 
class YourModel(Base):
    __tablename__ = 'Queries'  # Replace 'your_table_name' with your actual table name
 
    id = Column(Integer, primary_key=True)
    Questions = Column(String)
    Analysis = Column(String)
    Query = Column(String)
    Insight = Column(String)
 
 
 
connection_string_SQLAlchemy = 'mssql+pyodbc://devadmin:SqlServer123$@54.39.28.195,2552/Powerbi_Demo?driver=ODBC+Driver+17+for+SQL+Server'
 
connection_string_pyodbc = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=54.39.28.195,2552;DATABASE=Powerbi_Demo;UID=devadmin;PWD=SqlServer123$'
 
# Create the SQLAlchemy engine
engine = create_engine(connection_string_SQLAlchemy)
 
Session = sessionmaker(bind=engine)
 
# Create a session
session = Session()
 
@app.get("/getQuestions")
def getQuestions():
 
    quesDict = {}
    quesList = []
    analysisList = []
    # Execute the query
    query_result = session.query(YourModel).all()
 
    for item in query_result:
        quesList.append(item.Questions)
        analysisList.append(item.Analysis)
    quesDict["Questions"] = quesList
    quesDict["Analysis"] = analysisList
    return quesDict

@app.get("/getquery")
def getquery(Question: str):
    # Query the database to find the query corresponding to the input question
    query_result = session.query(YourModel).filter_by(Questions=Question).first()
    print(query_result)

    if query_result is None:
        # If no matching question found, raise an HTTPException with 404 status code
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Return the corresponding query
    return {"Query": query_result.Query}

 
# @app.get("/getTableData")
# def getTableData(question:str):
#     query_result = session.query(YourModel.Query).filter(YourModel.Questions == question).all()
 
#     sql_query = "\n".join(row[0] for row in query_result)
   
#     conn = pyodbc.connect(connection_string_pyodbc)
 
#     cursor = conn.cursor()
 
   
#     data_table = cursor.execute(sql_query)
#     column_names = [column[0] for column in cursor.description]
#     # print(data_table)
 
#     table_data = {}
#     headers = []
#     data = []
#     for row in column_names:
#         headers.append(row)
#     for row in data_table:
#         data.append(row)
#     table_data["headers"] = headers
#     # print(table_data)
#     table_data["data"] = data
#     # print(table_data)
#     return table_data


@app.get("/getTableData")
async def get_table_data(question: str) -> Dict[str, List[Dict]]:
    try:
        query_result = session.query(YourModel.Query).filter(YourModel.Questions == question).all()
        sql_query = "\n".join(row[0] for row in query_result)
       
        conn = pyodbc.connect(connection_string_pyodbc)
        cursor = conn.cursor()
       
        cursor.execute(sql_query)
        column_names = [column[0] for column in cursor.description]
        data = cursor.fetchall()

        table_data = {"headers": column_names, "data": []}
        for row in data:
            # Convert Decimal objects to float for JSON serialization
            row = [float(elem) if isinstance(elem, Decimal) else elem for elem in row]
            table_data["data"].append(dict(zip(column_names, row)))
        
        json_data = json.dumps(table_data)  # Convert table_data to JSON string
        
        headers = {"Content-Type": "application/json"}  # Set Content-Type header
        
        return Response(content=json_data, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









