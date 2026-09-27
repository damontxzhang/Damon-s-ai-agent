import os
from config import max_chars

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        safe_working_dic=os.path.abspath(working_directory)
        target_dic=os.path.abspath(os.path.join(working_directory,file_path))
        valid_file_path = (os.path.commonpath([safe_working_dic, target_dic])== safe_working_dic)
        if not valid_file_path :
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dic):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dic, "r") as f:
            content = f.read(max_chars)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {max_chars} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type":"function",
    "function":{
        "name":"get_file_content",
        "description":"Reads and returns the contents of a text file relative to the working directory. Content may be truncated if it exceeds the maximum character limit.",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"The path to the file to read, relative to the working directory.",
                },
            },
            "required":["file_path"],
        },

    },
}
