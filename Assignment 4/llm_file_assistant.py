import json
import os

from openai import OpenAI

from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file
)


# --------------------------------------------------
# OpenRouter Client
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)


# --------------------------------------------------
# Tool Definitions
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents and metadata of a PDF, TXT, or DOCX file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["filepath"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory, optionally filtered by extension.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory containing the files."
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional file extension such as .pdf, .docx, or .txt."
                    }
                },
                "required": ["directory"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file and create directories if necessary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path where the file should be created."
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write into the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search for a keyword inside a PDF, TXT, or DOCX file. Search is case-insensitive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path of the file to search."
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Keyword or phrase to search for."
                    }
                },
                "required": ["filepath", "keyword"]
            }
        }
    }
]


# --------------------------------------------------
# Tool Executor
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "read_file":
        return read_file(
            arguments["filepath"]
        )

    elif tool_name == "list_files":
        return list_files(
            arguments["directory"],
            arguments.get("extension")
        )

    elif tool_name == "write_file":
        return write_file(
            arguments["filepath"],
            arguments["content"]
        )

    elif tool_name == "search_in_file":
        return search_in_file(
            arguments["filepath"],
            arguments["keyword"]
        )

    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }


# --------------------------------------------------
# LLM Assistant
# --------------------------------------------------

def ask_assistant(user_query):

    messages = [
        {
            "role": "system",
            "content": """
You are a file assistant.

You have access to tools for reading, listing,
writing, and searching files.

The resumes are stored in the "resumes" directory.

Use the available tools whenever the user's request
requires accessing or modifying files.

Do not invent file contents.

If the user asks about resume contents, read or search
the actual files first.
"""
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # --------------------------------------------------
    # Tool-calling loop
    # --------------------------------------------------

    while True:

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # No tool call means the LLM has finished
        if not assistant_message.tool_calls:

            return assistant_message.content

        # Add assistant's tool request to conversation
        messages.append(assistant_message)

        # Execute every requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"\n[AI called tool: {tool_name}]"
            )

            print(
                f"[Arguments: {arguments}]"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            # Send tool result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("===================================")
    print("      Resume AI File Assistant")
    print("===================================")

    while True:

        user_query = input("\nYou: ")

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:

            answer = ask_assistant(user_query)

            print("\nAssistant:")
            print(answer)

        except Exception as e:

            print(f"\nError: {e}")

