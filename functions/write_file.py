import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        safe_working_dic=os.path.abspath(working_directory)
        target_dic=os.path.abspath(os.path.join(working_directory,file_path))
        valid_file_path = (os.path.commonpath([safe_working_dic, target_dic])== safe_working_dic)
        if not valid_file_path :
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dic):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir=os.path.dirname(target_dic)
        os.makedirs(parent_dir,exist_ok=True)

        with open(target_dic,"w") as f:
            f.write(content)

        return  f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error:{e}"

schema_write_file={
    "type":"function",
    "function":{
        "name":"write_file",
        "description":"write or overwrites content to a file at the specified path relative to the working directory.",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"The path of the file to write to, relative to the working directory.",
                },
                "content":{
                    "type":"string",
                    "description":"The text content to be written into the file.",
                },
            },
            "required":["file_path","content"],
        },
    },
}
