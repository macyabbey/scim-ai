from smolagents import CodeAgent, HfApiModel

from ..instrument import trace_provider

from ..scimexampleobjects import minimal_user, 
                                 full_user, 
                                 full_enterprise_user, 
                                 group

from dotenv import load_dotenv
load_dotenv()

from .tools import build_server, 
                   start_server, 
                   test_server, 
                   update_application_config, 
                   update_pom, 
                   write_connected_group_service, 
                   write_connected_user_service

                
# model_id = "meta-llama/Llama-3.3-70B-Instruct" 

# You can choose to not pass any model_id to HfApiModel to use a default free model
# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
model = HfApiModel()
agent = CodeAgent(
  tools=[
    update_application_config, 
    update_pom, 
    write_connected_group_service, 
    write_connected_user_service,
    build_server, 
    start_server, 
    test_server
  ], 
  model=model, 
  add_base_tools=True,
  additional_authorized_imports=["pprint"]
)