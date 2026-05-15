import streamlit as st
import json
import os
import base64
st.set_page_config(page_title="Отели от Назиляпы",layout="centered")
DATA_FILE="hotels.json"
if"hotels"not in st.session_state:
 if os.path.exists(DATA_FILE):
  try:
   with open(DATA_FILE,"r",encoding="utf-8")as f:st.session_state.hotels=json.load(f)
  except:st.session_state.hotels=[]
 else:st.session_state.hotels=[]
def save_hotels():
 with open(DATA_FILE,"w",encoding="utf-8")as f:json.dump(st.session_state.hotels,f,ensure_ascii=False,indent=2)
st.title("🌍 Отели от Назиляпы")
st.subheader("Управление отелями")
if st.button("➕ Добавить новый отель",use_container_width=True):st.session_state.show_form=True
if st.session_state.get("show_form",False):
 st.write("---")
 name=st.text_input("Название отеля")
 country=st.text_input("Страна")
 city=st.text_input("Город")
 district=st.text_input("Район")
 description=st.text_area("Описание отеля")
 stars=st.slider("⭐ Звёзды",1,7,5)
 photos=st.file_uploader("Фото отеля (много можно)",type=["jpg","png","jpeg"],accept_multiple_files=True)
 col1,col2=st.columns(2)
 with col1:
  if st.button("✅ Сохранить отель",use_container_width=True):
   if name:
    photo_list=[]
    for photo in photos:
     photo_list.append({"name":photo.name,"data":base64.b64encode(photo.read()).decode()})
    st.session_state.hotels.append({"name":name,"country":country,"city":city,"district":district,"description":description,"stars":stars,"photos":photo_list})
    save_hotels()
    st.session_state.show_form=False
    st.rerun()
 with col2:
  if st.button("❌ Отмена",use_container_width=True):st.session_state.show_form=False;st.rerun()
st.write("### Сохранённые отели")
if st.button("🗑 Очистить последний отель",use_container_width=True):
 if st.session_state.hotels:st.session_state.hotels.pop();save_hotels();st.rerun()
for i,hotel in enumerate(st.session_state.hotels):
 st.write(f"**{i+1}. {hotel['name']}**")
 st.write(f"📍 {hotel.get('country','')} | {hotel.get('city','')} | {hotel.get('district','')}")
 st.write(f"⭐ {hotel.get('stars',0)} звёзд")
 if hotel.get("description"):st.write(hotel["description"])
 if hotel.get("photos"):
  cols=st.columns(3)
  for idx,photo in enumerate(hotel["photos"]):
   try:
    image_data=base64.b64decode(photo["data"])
    st.image(image_data,width=250)
   except:pass
 st.write("---")
st.caption("ВЕРСИЯ 1.2")