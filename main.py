import streamlit as st
import requests
import json


def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True


# Function to add a header
def add_header():
  st.session_state.headers.append({"key": st.empty(), "value": st.empty()})


# Function to handle sending the request
def send_request(method, url, actual_headers, params, body, auth):
  try:
    response = requests.request(method,
                                url,
                                headers=actual_headers,
                                params=params,
                                json=body,
                                auth=auth)
    st.session_state.response = response
    st.session_state.view_format = 'JSON'
  except Exception as e:
    st.error(f'An error occurred: {str(e)}')


# Function to display the response
def display_response():
  if st.session_state.response is not None:
    st.subheader('Response')

    # Response Headers
    # st.write("##### Headers")
    # st.json(dict(st.session_state.response.headers.__dict__['_store']))

    # Select View Format
    st.write("##### Body")
    st.session_state.view_format = st.selectbox(
      'View Format', ['JSON', 'Text'],
      index=0 if st.session_state.view_format == 'JSON' else 1)

    # Response Body
    if st.session_state.view_format == 'JSON':
      try:
        if st.session_state.response.headers[
            'Content-Type'] == 'application/json':
          st.json(st.session_state.response.json())
        elif is_json(st.session_state.response.text):
          st.json(st.session_state.response.json())
        else:
          st.warning('Response is not in JSON format. Showing as text.')
          st.write(st.session_state.response.text)
      except json.JSONDecodeError:
        st.warning('Failed to decode JSON response. Showing as text.')
        st.write(st.session_state.response.text)
    else:
      st.write(st.session_state.response.text)
  else:
    st.warning('No response available. Please send a request.')


st.title('ApiLit - Dashboard')
st.subheader('HTTP Request Panel')

method = st.selectbox('Choose HTTP Method', ['GET', 'POST', 'PUT', 'DELETE'])
url = st.text_input('Enter URL', value='')

# Initialize session state for headers
if 'headers' not in st.session_state:
  st.session_state.headers = []
if 'response' not in st.session_state:
  st.session_state.response = None
if 'view_format' not in st.session_state:
  st.session_state.view_format = None

# Headers Section
st.subheader('Headers')
actual_headers = {}
if st.button('Add Header'):
  add_header()
for i, header in enumerate(st.session_state.headers):
  cols = st.columns(2)
  key = cols[0].text_input(f'Header Key {i + 1}', key=f"key{i}")
  value = cols[1].text_input(f'Header Value {i + 1}', key=f"value{i}")
  if key and value:
    actual_headers[key] = value

params_input = st.text_area('Enter Parameters (JSON format)')
params = json.loads(params_input) if params_input else None
body_input = st.text_area('Enter Body Content (JSON format)') if method in [
  'POST', 'PUT'
] else None
body = json.loads(body_input) if body_input else None
auth_enabled = st.checkbox('Enable Basic Authentication')
if auth_enabled:
  username = st.text_input('Username')
  password = st.text_input('Password', type='password')
  auth = (username, password)
else:
  auth = None

if st.button('Send Request'):
  send_request(method, url, actual_headers, params, body, auth)

display_response()
