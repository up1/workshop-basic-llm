import time
import gradio as gr
import single_retriever
from llama_index.core.llms import ChatMessage,MessageRole

def get_stream_response(query_string,radio,model):
  chat_message = [ ChatMessage(role=MessageRole.USER, content=query_string) ]

  if radio == 'logs':
     return single_retriever.get_chat_engine('logs_collection', 'logs_vector_idx', model).stream_chat(query_string)
  elif radio == 'devguide':
     return single_retriever.get_chat_engine('devguide_collection', 'devguide_vector_idx', model).stream_chat(query_string)
#   elif radio == 'all':
#      return fusion_retriever.get_chat_engine(model).stream_chat(chat_message)
  else:
     return single_retriever.default_llm(model).stream_chat(query_string)

def chat_with_llm(message,history,radio,model):
 i               = len(message)
 query           = message[: i+1]
 response_str    = ''
 stream_response = get_stream_response(query,radio,model)
 if radio == 'none' :
   result = stream_response
   for r in result:
     time.sleep(0.1)
     response_str += r.delta
   yield response_str
 else:
   result = stream_response.response_gen
   for r in result:
     time.sleep(0.1)
     response_str += r
   yield response_str

with gr.Blocks( title = 'GenAI with RAG', fill_height = True ) as app:
  radio   = gr.Radio(choices = ['logs', 'devguide','all'], value='logs', label='Context')
  radio.change(fn=None, inputs=radio, outputs=None)
  
  model   = gr.Dropdown(['llama3.2:1b'],value='llama3.2:1b',label='Model')
  model.change(fn=None, inputs=model, outputs=None)
  
  gr.ChatInterface(
    chat_with_llm,
    title             = 'Log Analysis with RAG',
    description       = f'You are interacting with <b>{model.value}</b>',
    additional_inputs = [radio,model],
    theme             = 'soft')

app.launch(share=False, server_name='0.0.0.0', server_port=7860)