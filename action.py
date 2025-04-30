# from langchain_core.tools import tool
#
#
# @tool
# def fetch_drinks():
#     """执行动作001"""
#     print("perform action 001")
#     return "001"
#     # filename = 'example.txt'
#     #
#     # # 使用 'w' 模式打开文件，表示写入。如果文件不存在，会自动创建
#     # with open(filename, 'w', encoding='utf-8') as file:
#     #     # 向文件中写入文本
#     #     file.write('这是创建的新文件。\n')
#     #     file.write('可以在这里添加更多内容。\n')
#     #
#     # print(f"文件 '{filename}' 已成功创建并写入内容。")
#
#
# @tool
# def provide_beef():
#     """执行动作002"""
#     print("perform action 002")
#
#
# tools = [fetch_drinks, provide_beef]


import re

def fetch_drinks():
    """执行动作001"""
    print("perform action 001")

def provide_beef():
    """执行动作002"""
    print("perform action 002")

def provide_food():
    """执行动作003"""
    print("perform action 003")

def provide_book():
    """执行动作004"""
    print("perform action 004")

def map_search():
    """执行动作005"""
    print("perform action 005")

def wait():
    """执行动作000"""
    print("perform action 000")

functions = {
    "000": wait,
    "001": fetch_drinks,
    "002": provide_beef,
    "003": provide_food,
    "004": provide_book,
    "005": map_search,
}


def _parse_function_name(generated_response):
        match = re.search(r'Answer:\s*(\d+)', generated_response)
        if match:
            return match.group(1)
        else:
            return "000"


class ActionExecutor:
    def __init__(self):
        self.function_mapping = functions


    def run(self, generated_response):

        function_name = _parse_function_name(generated_response)
        if function_name in self.function_mapping:
            function = self.function_mapping[function_name]
            result = function()
            return {"result": result}
        else:
            return {"error": f"Unknown function name: {function_name}"}
