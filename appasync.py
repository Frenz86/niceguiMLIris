import streamlit as st
import requests
import asyncio

st.title("FANTASTICAPI - POST-GET Debugger")

url_API = st.text_input("Inserisci URL dell'API", "http://localhost:8000/predict")

input1 = st.number_input("Please write the first feature", 2.0)
input2 = st.number_input("Please write the second feature", 1.4)
input3 = st.number_input("Please write the third feature", 3.0)
input4 = st.number_input("Please write the fourth feature", 3.0)

payload = {
            "feature1": input1,
            "feature2": input2,
            "feature3": input3,
            "feature4": input4,
            }


async def make_prediction(method, payload):
    headers = {'accept': 'application/json'}
    try:
        if method == "GET":
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url_API, params=payload, headers=headers))
        else:
            headers['Content-Type'] = 'application/json'
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.post(url_API, json=payload, headers=headers))

        if response.status_code == 200:
            result = response.json()
            st.write("Prediction:", result)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
    if st.button("Predict IRIS with method GET"):
        asyncio.run(make_prediction("GET", payload))

    if st.button("Predict Iris with method POST"):
        asyncio.run(make_prediction("POST", payload))


if __name__ == '__main__':
    main()
