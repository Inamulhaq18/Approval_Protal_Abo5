from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import delete
import pandas as pd
import streamlit as st 
import psycopg2
from st_aggrid import AgGrid


engine = create_engine("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c", echo = False)

#Session for DB
Session=sessionmaker(bind=engine)
session=Session
Base=declarative_base()


shopify=pd.read_csv("shopifytemp.csv")
shopifycolumns=list(shopify.columns)
conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()
# Loading approved data from database
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)
pfa=dat
conn.close()
pfa=pfa[pfa["Product_id"]>650]
pfa=pfa[pfa["Product_approval_status"]==1]
pfa=pfa[pfa["shopify_status"]==0]
pfa=pfa.sort_values(by="Product_id")
pfa=pfa.drop_duplicates(subset='Product_Name_en', keep="last")
#Number of items 
number_of_items=(pfa[pfa["Product_live_status"]==1]).shape[1]

pfa.dropna(subset=["Product_Name_en"])
pfa=pfa[pfa['Product_Name_en']!=""]
pfa=pfa[pfa['Product_image_P_url']!=""]

shopifycolumnss=pd.DataFrame(columns=shopifycolumns)
list(shopifycolumnss.columns)

pfa=pfa.dropna(subset=['variety'])

def getrowlen(row):
     try:
      img_len=len((row["variety"]["imgsource"]))
     except:
      img_len=0
     try:
          data_len=len((row["variety"]['data']))
     except:
      data_len=0
     rowlen=max(img_len,data_len)
     return(rowlen)
#    try:
#       len((row["variety"]["imgsource"]))
#       data_len=len((row["variety"]['data']))
#       rowlen=data_len
#       #if "imgsource" in row["variety"]:
#       img_sourcelen=len((row["variety"]["imgsource"]))
#       print("img_sourcelen  ===================================================================================================================:",row["variety"]["imgsource"])
#       rowlen=max(data_len,img_sourcelen)  
#    except KeyError as error:
#       rowlen=1
#    return(rowlen)

def handler(row):
  handler.append(row['Product_Name_en'].replace("","_"))
  return(handler)

def dummyentries(lst,rowlen):
   for i in range(len(lst),rowlen):
     lst.append("")
   return(lst)
handler=[]
Title=[]
rowdata={}

dfshopify=pd.DataFrame(columns=shopifycolumns)

def geturlfor(imgs,row):
          if "R" in str(imgs):
            imgs=imgs.replace("R","")
            p_img=row["Product_image_P_url"].replace("{","")
            p_img=row["Product_image_P_url"].replace("}","")
            p_img=row["Product_image_P_url"].split(",")
            image_link=p_img[int(imgs)-1]
            return(image_link)
          else:
            R_img=row["Product_image_R_url"].replace("{","")
            R_img=row["Product_image_R_url"].replace("}","")
            R_img=row["Product_image_R_url"].split(",")
            image_link=R_img[int(imgs-1)]
            return(image_link)

#The main program
for index, row in pfa.iterrows():
  print("*************************************************************************************************")
  print(row)
  rowlen=getrowlen(row)
  print("Rowlen: ",rowlen)
  print("Imgesrc: ",len((row["variety"]["imgsource"])))
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  #handler
  handler=[]
  for i in range(1,rowlen+1):
    handler.append(row['Product_Name_en'].replace(" ","_"))
  
  if len(handler)>3:
   dftemp=pd.DataFrame({'Handle':handler})
  
  #productname
  Title=[]
  Title=[row['Product_Name_en'].strip()]
  dummyentries(Title,rowlen)
  
  #Body (HTML)
  Body=[]
  Body= [row['Product_describtion_en'].strip()]
  dummyentries(Body,rowlen)
  
  #vendor
  vendor_=[]
  vendor_=[row['Retail_outlet']]
  dummyentries(vendor_,rowlen)

  #Customer Product type 
  CPT=[]
  CPT = [row['Product_subcategory'].strip()]
  dummyentries(CPT,rowlen)

  #Tags
  tags=[]
  tags=[str(row['Product_Category'].strip()+", " + row['Product_subcategory'].strip()+", " + "ABO5 system")]
  dummyentries(tags,rowlen) 
  
  #Published
  Published=[]
  Published=["TRUE"]
  dummyentries(Published,rowlen)

  #Option1 Name
  option1=[]
  if row["variety"]["type"]=="Select":
    option1=[""]
    #st.write("if")
  else:
    option1=[row["variety"]["type"]]
    #st.write("else")
  option1=dummyentries(option1,rowlen)
  #st.write(len(option1))
  if option1[0]!="":
      varientstatus=1
  else:
      varientstatus=0

  #Option1 Value
  try:
    option1_val=(row["variety"]["data"])
    option1_val=dummyentries(option1_val,rowlen)
  except KeyError as error:
    option1_val=[""]
    option1_val=dummyentries(option1_val,rowlen)

  #'Variant Price',price
  price=[row["Product_price"]]
  for i in range(1,rowlen):
    price.append(row["Product_price"])
  VariantPrice=price
  
  #Image Source 
  imgsrc=[row["variety"]]
  image_link=[]
  try:
      templist=[]
      if "imgsource" in row["variety"]:
         #st.write("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
         for item in row["variety"]["imgsource"]:
            templist.append(geturlfor(item,row))
         #strinng="'".join(templist)
         #image_link.append(strinng)
         #image_link=[image_link[0]]
         #st.write("_______________TEMPLIST____________",len(templist))
         image_link=templist
#          st.write("dummyentries_______________:  ",len(image_link))
#          st.write("image_link:  ",len(image_link))
#          st.write("rowlen:  ",rowlen)
      
      
   
  except KeyError as error:
    image_link=[""]
    dummyentries(image_link,rowlen)
    #st.write("except  :",image_link)


  #imageposition
  imageposition=list(range(1,rowlen+1))
  
  #image varient url
  imagevurl=[]
  if rowlen==1:
     #imagevurl=dummyentries(imagevurl,rowlen)
      imagevurl=[""]
  if rowlen > 1:
     if row["variety"]["type"]!="Select":
          urlsdata=[]
          for option in row["variety"]['data']:
           if (option+"_img") in row["variety"]:
            dataa=row["variety"][option+"_img"]
            #urlsdata=[]
            urlsdataa=geturlfor(dataa[0],row)#this needs to return url for a 1,2,3,R1
            urlsdata.append(urlsdataa)

          imagevurl=urlsdata
          if len(urlsdata)<rowlen:
               imagevurl=dummyentries(imagevurl,rowlen)
               
     if row["variety"]["type"]=="Select":
          imagevurl=[""]
          imagevurl=dummyentries(imagevurl,rowlen)
  
  
  #option1 value{"type": "color","data": ["blue"],"blue_img": [4]
  if row["variety"]["type"]!="Select":
     option1val=row["variety"]["type"]
  else:
     option1val=[""]
  option1val=dummyentries(option1val,rowlen)


  if varientstatus==1:
     varlen=len(row["variety"]["data"])
     if "" in row["variety"]["data"]:
          st.write("__+++____+++____+++____+++____+++____+++__")
          totalclean=row["variety"]["data"]
          st.write("Type: ")
          st.write(type(totalclean))
          st.write(totalclean)
          totalclean.remove("")
          st.write("============================================")
          st.write(totalclean)
          varlen=len(totalclean)
    #Publishedd
  if varientstatus==1:
      st.write(Title)
      st.write(row["variety"]["data"])
      st.write("((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))))))))))))))))")
      Published=["TRUE"]*varlen
      Published=dummyentries(Published,rowlen)
  if varientstatus==0:
       Published=["TRUE"]
       Published=dummyentries(Published,rowlen)
   
  #Varient inventory Tracking
  if varientstatus==1:
      VIT=["shopify"]*varlen
      VIT=dummyentries(VIT,rowlen)
  if varientstatus==0:
       VIT=["shopify"]
       VIT=dummyentries(VIT,rowlen)
   
 #Gift Card
  if varientstatus==1:
      gift=["FALSE"]*varlen
      gift=dummyentries(gift,rowlen)
  if varientstatus==0:
       gift=["FALSE"]
       gift=dummyentries(gift,rowlen)
  
#Variant Inventory Qty
  if varientstatus==1:
      VIQ=["50"]*varlen
      VIQ=dummyentries(VIQ,rowlen)
  if varientstatus==0:
       VIQ=["50"]
       VIQ=dummyentries(VIQ,rowlen)

 #Variant Inventory Policy
  if varientstatus==1:
      VIP=["deny"]*varlen
      VIP=dummyentries(VIP,rowlen)
  if varientstatus==0:
       VIP=["deny"]
       VIP=dummyentries(VIP,rowlen)
  #Variant Fulfillment Service
  if varientstatus==1:
      VFS=["manual"]*varlen
      VFS=dummyentries(VFS,rowlen)
  if varientstatus==0:
       VFS=["manual"]
       VFS=dummyentries(VFS,rowlen)
   #Variant Price
  price=row["Product_price"]

  if varientstatus==1:
      VP=[price]*varlen
      VP=dummyentries(VP,rowlen)
  if varientstatus==0:
       VP=[price]
       VP=dummyentries(VP,rowlen)
  
   #Variant Price
  price=row["Product_price"]

  if varientstatus==1:
      pr_ice=[price]*varlen
      pr_ice=dummyentries(pr_ice,rowlen)
  if varientstatus==0:
       pr_ice=[price]
       pr_ice=dummyentries(pr_ice,rowlen)
#Variant Taxable
  if varientstatus==1:
      VT=["True"]*varlen
      VT=dummyentries(VT,rowlen)
  if varientstatus==0:
       VT=[""]
       VT=dummyentries(VT,rowlen)
 
#Status
  if varientstatus==1:
      status__=["Active"]*varlen
      status__=dummyentries(status__,rowlen)
  if varientstatus==0:
       status__=["Active"]
       status__=dummyentries(status__,rowlen)
     
     
  print(option1val)
  print(imagevurl)
  # for h in handler:
  #   a={'Handle': h}
  #   df1=df1.append(a, ignore_index = True)
  st.write(len(handler),len(Title),len(Body),len(vendor_),len(CPT),len(tags),len(option1),len(option1_val),len(Published),len(pr_ice),len(imageposition),len(image_link),len(imagevurl))
  dftemp=pd.DataFrame({'Handle':handler,'Title':Title,'Body (HTML)':Body,'Vendor':vendor_,'Custom Product Type':CPT,'Tags':tags,'Option1 Name':option1,'Option1 Value':option1_val,'Published':Published,'Variant Price':VP,'Image Position':imageposition,'Image Src':image_link,'Variant Image':imagevurl,'Variant Inventory Tracker':VIT,'Variant Inventory Qty':VIQ,'Variant Inventory Policy':VIP,'Variant Fulfillment Service':VFS,'Variant Price':VP,"Variant Taxable":VT,"Gift Card":gift,"Status":status__,})
  dfshopify=dfshopify.append(dftemp,ignore_index=True)
  dftemp=pd.DataFrame({'Handle':handler})
  

  print(option1val)
  print(imagevurl)
  print(imageposition)
  print(option1)
  print(tags)
  print(Title)
  print(handler)
  print("_______________________________________________________________________________________________________________________________")
st.header("😊 🙌")
st.header("Yay ! '{}'  Products Ready to be uploaded ".format(dfshopify["Handle"].nunique()))
st.header("")


AgGrid(dfshopify)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

dfshopify=convert_df(dfshopify)
st.download_button(
   "Press to Download",
   dfshopify,
   "file.csv",
   "text/csv",
)

pids=list(pfa['Product_id'])
pids = ''.join(str(pids))
pids=pids.replace("[","")
pids=pids.replace("]","")
pids=pids.replace("'","")
agree = st.checkbox('Mark as uploaded')

if agree:    
 if st.button("Update"):
   with engine.connect() as con:
      con.execute('UPDATE master_product_table SET "shopify_status" = 1 WHERE "Product_id" IN ({})'.format(pids))
