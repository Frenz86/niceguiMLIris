import requests
import streamlit as st

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


def make_prediction(method, payload):
    headers = {'accept': 'application/json'} if method == "GET" else {'Content-Type': 'application/json'}

    try:
        response = requests.get(url_API, params=payload, headers=headers) if method == "GET" else requests.post(url_API, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return

    result = response.json()
    st.write("Prediction:", result)


def main():
    if st.button("Predict IRIS with method GET"):
        make_prediction("GET", payload)

    if st.button("Predict Iris with method POST"):
        make_prediction("POST", payload)


if __name__ == '__main__':
    main()
