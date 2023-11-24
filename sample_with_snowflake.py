import streamlit as st # type:ignore
import streamlit.components.v1 as components # type:ignore
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html # type:ignore
from pygwalker.data_parsers.database_parser import Connector # type:ignore
import pandas as pd # type:ignore

# Streamlitのページ設定。タイトルとレイアウトを設定する
st.set_page_config(
    page_title="Snowflake X Streamlit X PyGWalker",
    layout="wide"
)
 
# 1.PyGWalkerの通信機能を初期化
init_streamlit_comm()

# 2.Snowflakeと接続するコネクタを取得
# TODO: 各パラメータをシークレットに変更する。SQLも一回変数化する
url = ''
sql = """
    SELECT
        *
    FROM
        SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
"""

# 3.PyGWalkerのフロントエンドのHTMLを取得する
# `use_kernel_calc=True`を指定するときは、PyGWalkerのHTMLをキャッシュすることが推奨
# そのため、`@st.cache_resource`を使用してキャッシュするが、このときハッシュできない引数 Connector の変数名には`_`をつけている
@st.cache_resource
def get_html(_conn: Connector) -> str:
    # Streamlitのコンポーネントに埋め込むHTMLを取得するときはwalk()の代わりにget_streamlit_html()を使用する
    # Snowflakeをバックエンドとして使用するときはDataFrameではなくConnectorを渡すs
    # PyGWalkerの通信機能を使用するため、`use_kernel_calc=True`を指定する
    html = get_streamlit_html(_conn, use_kernel_calc=True, debug=False)
    return html

# 4.PyGWalkerのフロントエンドのHTMLをStreamlitのコンポーネントに埋め込む
html = get_html(conn) 
components.html(html, width=1300, height=1000, scrolling=True)
