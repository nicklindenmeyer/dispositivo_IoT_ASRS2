import streamlit as st
import pandas as pd
import requests
import altair as alt
import time

channel_id = "2601361"
read_api_key = "2IMZSGDD358HBWBD"

# número de amostras = periodo em segundos / intervalo
interval_data = 10
results_live = 300/interval_data
results_1h = 3600/interval_data
results_6h = 21600/interval_data
results_12h = 43200/interval_data
results_24h = 86400/interval_data
# results_1w = 604800/interval_data

# intervalo de tempo para a página recarregar
update_interval = 10

st.set_page_config(
    page_title="Disposivito IoT para monitoramento de energia elétrica do ASRS²", page_icon=":zap:")

# @st.cache_data()


def fetch_data_from_thingspeak(channel_id, read_api_key):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds.json?api_key={read_api_key}&results={results_live}"
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.rename(columns={
        'field1': 'voltage',
        'field2': 'current',
        'field3': 'power_factor',
        'field4': 'active_power',
        'field5': 'apparent_power'
    })
    return df


df = fetch_data_from_thingspeak(channel_id, read_api_key)


def fetch_data_from_thingspeak_1h(channel_id, read_api_key):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds.json?api_key={read_api_key}&results={results_1h}"
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.rename(columns={
        'field1': 'voltage',
        'field2': 'current',
        'field3': 'power_factor',
        'field4': 'active_power',
        'field5': 'apparent_power'
    })
    return df


def fetch_data_from_thingspeak_6h(channel_id, read_api_key):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds.json?api_key={read_api_key}&results={results_6h}"
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.rename(columns={
        'field1': 'voltage',
        'field2': 'current',
        'field3': 'power_factor',
        'field4': 'active_power',
        'field5': 'apparent_power'
    })
    return df


def fetch_data_from_thingspeak_12h(channel_id, read_api_key):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds.json?api_key={read_api_key}&results={results_12h}"
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.rename(columns={
        'field1': 'voltage',
        'field2': 'current',
        'field3': 'power_factor',
        'field4': 'active_power',
        'field5': 'apparent_power'
    })
    return df


def fetch_data_from_thingspeak_24h(channel_id, read_api_key):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds.json?api_key={read_api_key}&results={results_24h}"
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.rename(columns={
        'field1': 'voltage',
        'field2': 'current',
        'field3': 'power_factor',
        'field4': 'active_power',
        'field5': 'apparent_power'
    })
    return df


def fetch_time_update(channel_id):
    url = f"https://api.thingspeak.com/channels/{
        channel_id}/feeds/last.json?timezone=America%2FSao_Paulo"
    response = requests.get(url)
    data = response.json()
    data['created_at'] = pd.to_datetime(data['created_at'])
    df = data['created_at']
    return df


time_update = fetch_time_update(channel_id)

latest_data = df.iloc[-1]
rms_voltage = latest_data['voltage']
rms_current = latest_data['current']
power_factor = latest_data['power_factor']
active_power = latest_data['active_power']
apparent_power = latest_data['apparent_power']

latest_data = df.iloc[-2]
old_rms_voltage = latest_data['voltage']
old_rms_current = latest_data['current']
old_power_factor = latest_data['power_factor']
old_active_power = latest_data['active_power']
old_apparent_power = latest_data['apparent_power']

delta_rms_voltage = float(rms_voltage) - float(old_rms_voltage)
delta_rms_current = float(rms_current) - float(old_rms_current)
delta_power_factor = float(power_factor) - float(old_power_factor)
delta_active_power = float(active_power) - float(old_active_power)
delta_apparent_power = float(apparent_power) - float(old_apparent_power)

with st.container():
    st.title(
        "Dispositivo :red[IoT] para monitoramento de energia elétrica do :red[ASRS²]:zap:")
    st.subheader(
        "LabCIM | Engenharia Elétrica | Ulbra | Canoas | RS", divider='rainbow')
    st.write(f"Última atualização: {time_update}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Tensão", f"{rms_voltage} V", f"{
                delta_rms_voltage:.2f} V", delta_color="off")
    col2.metric("Corrente", f"{rms_current} A", f"{
                delta_rms_current:.2f} A", delta_color="inverse")
    col3.metric("Fator de Potência", f"{power_factor}", f"{
                delta_power_factor:.2f}")
    col1.metric("Potência Ativa", f"{active_power} W", f"{
                delta_active_power:.2f} W", delta_color='inverse')
    col2.metric("Potência Aparente", f"{apparent_power} VA", f"{
                delta_apparent_power:.2f} VA", delta_color='inverse')
    st.divider()

with st.container():
    period = st.selectbox("Selecione o período", [
                          "Live", "1h", "6h", "12h", "24h"])

    if period == 'Live':
        df_periodic = df
    elif period == '1h':
        df_1h = fetch_data_from_thingspeak_1h(channel_id, read_api_key)
        df_periodic = df_1h
    elif period == '6h':
        df_6h = fetch_data_from_thingspeak_6h(channel_id, read_api_key)
        df_periodic = df_6h
    elif period == '12h':
        df_12h = fetch_data_from_thingspeak_12h(channel_id, read_api_key)
        df_periodic = df_12h
    elif period == '24h':
        df_24h = fetch_data_from_thingspeak_24h(channel_id, read_api_key)
        df_periodic = df_24h

    st.write("Tensão")
    voltage_chart = alt.Chart(df_periodic).mark_line().encode(
        x='created_at:T',
        y='voltage:Q'
    ).properties(
        width='container',
        height=200
    )
    st.altair_chart(voltage_chart, use_container_width=True)
    st.divider()

    st.write("Corrente")
    current_chart = alt.Chart(df_periodic).mark_line().encode(
        x='created_at',
        y='current:Q'
    ).properties(
        width='container',
        height=200
    )
    st.altair_chart(current_chart, use_container_width=True)
    st.divider()

    st.write("Fator de potência")
    power_factor_chart = alt.Chart(df_periodic).mark_line().encode(
        x='created_at',
        y='power_factor:Q'
    ).properties(
        width='container',
        height=200
    )
    st.altair_chart(power_factor_chart, use_container_width=True)
    st.divider()

    st.write("Potência Ativa")
    active_power_chart = alt.Chart(df_periodic).mark_line().encode(
        x='created_at',
        y='active_power:Q'
    ).properties(
        width='container',
        height=200
    )
    st.altair_chart(active_power_chart, use_container_width=True)
    st.divider()

    st.write("Potência Aparente")
    apparent_power_chart = alt.Chart(df_periodic).mark_line().encode(
        x='created_at',
        y='apparent_power:Q'
    ).properties(
        width='container',
        height=200
    )
    st.altair_chart(apparent_power_chart, use_container_width=True)
    st.divider()

url_thingSpeak = "https://thingspeak.com/channels/2601361"
url_linkedIn = "https://www.linkedin.com/in/nicklindenmeyer/?originalSubdomain=br"
link_text_thingSpeak = "ThingSpeak"
link_text_linkedIn = "Nicolas Lindenmeyer"

st.write("Fonte: [ThingSpeak](https://thingspeak.com/channels/2601361)")
st.write(
    "Desenvolvido por [Nicolas Lindenmeyer](https://www.linkedin.com/in/nicklindenmeyer/)")

st.caption(
    "Trabalho de conclusão de curso de Engenharia Elétrica - Universidade Luterana do Brasil")
st.caption("Aplicação desenvolvida em _Python_ com o uso da biblioteca _Streamlit_")

time.sleep(update_interval)
st.experimental_rerun()
