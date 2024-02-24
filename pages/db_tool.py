import streamlit as st

def do_sql(sql: str):
    conn = st.connection("my_mysql")
    df = conn.query(sql)
    st.dataframe(df)
    
    
def main():
    # st.title('Uber pickups in NYC')
    sql = "select * from vadmin_auth_menu"
    do_sql(sql)
    
if __name__ == '__main__':
    main()