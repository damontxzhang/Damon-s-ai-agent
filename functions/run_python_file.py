import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        safe_working_dic=os.path.abspath(working_directory)
        target_dic=os.path.abspath(os.path.join(working_directory,file_path))
        valid_file_path = (os.path.commonpath([safe_working_dic, target_dic])== safe_working_dic)
        if not valid_file_path :
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dic):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command=["python", target_dic]
        if args:
            command.extend(args)
        result=subprocess.run(
          command,
          cwd=working_directory,
          capture_output=True,
          text=True,
          timeout=30
        )

        output=[]
        if result.returncode !=0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:{result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type":"function",
    "function":{
        "name":"run_python_file",
        "description":"Executes a Python file within the working directory and returns its output (stdout and stderr).",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"The path to the file to read, relative to the working directory.",
                },
                "args":{
                    "type":"array",
                    "items":{
                        "type":"string",
                    },
                "description":"Optional list of command line arguments to pass to the sript.",

                },
            },
            "required":["file_path"],
        },

    },
}
