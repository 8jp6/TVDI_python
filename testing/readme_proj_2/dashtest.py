from dash import Dash, html, dcc, callback, Input, Output,_dash_renderer
import pandas as pd
import dash_mantine_components as dmc
from dash_iconify import DashIconify
_dash_renderer._set_react_version("18.2.0")

# 載入數據
try:
    df = pd.read_csv(r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj_2\student_lifestyle_dataset.csv')
    print("數據加載成功")
    print(df.head())  # 檢查數據結構
except Exception as e:
    print("數據加載失敗:", e)

# 準備資料選項
radio_data = [
    ['Study_Hours_Per_Day', '學習時間'],
    ['Extracurricular_Hours_Per_Day', '課外活動時間'],
    ['Sleep_Hours_Per_Day', '睡眠時間'],
    ['Social_Hours_Per_Day', '社交時間'],
    ['Physical_Activity_Hours_Per_Day', '體育活動時間'],
    ['GPA', '平均成績'],
    ['Stress_Level', '壓力水平']
]

# 準備學生選擇下拉選單數據
selected_data = [{'value': value, 'label': value} for value in df['Student_ID'].unique()]

# 初始化 Dash 應用
app1 = Dash(__name__, external_stylesheets=dmc.styles.ALL, requests_pathname_prefix="/dashapp/")

# 應用佈局
app1.layout = dmc.MantineProvider(
    dmc.AppShell(
        children=[
            dmc.AppShellHeader(
                dmc.NavLink(
                    label="學生生活統計",
                    leftSection=DashIconify(icon="tabler:gauge"),
                    active=True,
                    variant="filled",
                    color="blue",
                    id="school_icon",
                    h=70,
                    href='/',
                    refresh=True
                ),
                h=70
            ),
            dmc.AppShellMain(
                [
                    dmc.Container(
                        dmc.Title(f"學生生活統計數據分析", order=2),
                        fluid=True,
                        ta='center',
                        my=30
                    ),
                    dmc.Flex(
                        [
                            dmc.Stack(
                                [
                                    dmc.RadioGroup(
                                        children=dmc.Group([dmc.Radio(l, value=k) for k, l in radio_data], my=10),
                                        id="radio_item",
                                        value=radio_data[0][0],  # 預設選擇第一個選項
                                        label="請選擇查詢的種類",
                                        size="md",
                                        mb=10,
                                    ),
                                    dmc.Select(
                                        label="請選擇學生",
                                        placeholder="請選擇1個",
                                        id="dropdown-selection",
                                        data=selected_data,
                                        value=selected_data[0]['value'] if selected_data else None,  # 預設選擇第一個學生
                                        w=200,
                                        mb=10,
                                    )
                                ],
                            ),
                            dmc.ScrollArea(
                                children=[],
                                h=300,
                                w='50%',
                                id='scrollarea'
                            )
                        ],
                        direction={"base": "column", "sm": "row"},
                        gap={"base": "sm", "sm": "lg"},
                        justify={"base": "center"},
                    ),
                    dmc.Container(
                        dmc.LineChart(
                            id='lineChart',
                            h=300,
                            dataKey="Student_ID",
                            data=[],  # 初始設為空數據
                            series=[],
                            curveType="bump",
                            tickLine="xy",
                            withXAxis=True,
                            withDots=True,
                            gridAxis='x',
                            withLegend=True,
                            xAxisLabel='學生編號'
                        ),
                        my=50
                    )
                ],
            ),
        ],
        header={'height': 70}
    )
)

# 更新圖表的回調函數
@callback(
    [Output('lineChart', 'data'),
     Output('lineChart', 'series')],
    [Input('dropdown-selection', 'value'),
     Input('radio_item', 'value')]
)
def update_graph(student_id, selected_metric):
    # 同時處理 student_id 或 selected_metric 為 None 的情況
    if not student_id or not selected_metric:
        return [], []

    dff = df[df['Student_ID'] == student_id]
    if dff.empty:
        return [], []

    # 確保 selected_metric 存在於數據框中
    if selected_metric not in dff.columns:
        return [], []

    data_to_plot = dff[['Student_ID', selected_metric]].to_dict('records')
    label = f'{student_id} 的 {selected_metric}'
    series = [{"name": selected_metric, "label": label, "color": "indigo.6"}]
    return data_to_plot, series


@callback(
    Output('scrollarea', 'children'),
    [Input('dropdown-selection', 'value'),
     Input('radio_item', 'value')]
)
def update_table(student_id, selected_metric):
    if not student_id or not selected_metric:
        return dmc.Text("未選擇學生或指標")

    dff = df[df['Student_ID'] == student_id]
    if dff.empty:
        return dmc.Text(f"無數據可顯示")

    if selected_metric not in dff.columns:
        return dmc.Text(f"無法顯示數據，因為欄位 {selected_metric} 不存在")

    table_data = dff[['Student_ID', selected_metric]].to_dict('records')
    rows = [
        dmc.TableTr(
            [dmc.TableTd(record['Student_ID']),
             dmc.TableTd(record[selected_metric])]
        ) for record in table_data
    ]

    head = dmc.TableThead(
        dmc.TableTr([dmc.TableTh("Student_ID"), dmc.TableTh(selected_metric)])
    )
    body = dmc.TableTbody(rows)
    caption = dmc.TableCaption(f"{student_id} 的 {selected_metric} 統計數據")
    return dmc.Table([head, body, caption])



# 啟動應用
if __name__ == '__main__':
    app1.run(debug=True)
