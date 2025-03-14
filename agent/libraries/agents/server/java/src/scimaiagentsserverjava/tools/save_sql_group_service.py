import os
from typing import Dict, Any
from smolagents.tools import tool

@tool(
  name="save_sql_group_service",
  description="Saves the SQL Group Service Java code to a file in the server's persistence directory",
  parameters={
    "type": "object",
    "properties": {
      "code_content": {
        "type": "string",
        "description": "The Java code content for the SQL Group Service"
      }
    },
    "required": ["code_content"]
  }
)
def save_sql_group_service(code_content: str) -> Dict[str, Any]:
  """Writes provided Java code to the SqlGroupService.java file.
  
  Args:
    code_content (str): The Java code content for the SQL group service.
    
  Returns:
    Dict[str, Any]: A dictionary containing the status and path of the saved file.
  """
  file_path = os.path.join(
    "src", "main", "java", "com", "scim", "ai", "server", "persistence", "SqlGroupService.java"
  )
  
  try:
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write the Java code to the file
    with open(file_path, 'w') as file:
      file.write(code_content)
    
    return {
      "success": True,
      "message": f"SqlGroupService.java has been created at {file_path}",
      "file_path": file_path
    }
  except Exception as e:
    return {
      "success": False,
      "message": f"Failed to create SqlGroupService.java: {str(e)}",
      "error": str(e)
    }
