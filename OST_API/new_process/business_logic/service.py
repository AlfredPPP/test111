from business_logic.api_handler import call_api
from data_access.database import query_database

def process_request(data):
    api_response = call_api("https://api.example.com/endpoint", data)
    db_result = query_database("SELECT * FROM table WHERE condition")
    # 结合API响应和数据库结果进行处理
    return {"api_response": api_response, "db_result": db_result}
