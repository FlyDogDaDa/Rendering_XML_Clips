import gradio as gr
import os
import zipfile
import xml.etree.ElementTree as ET
import Data.xml_tool as xmlH
import Data.cliper_tool as cliper_tool
import copy


class action_notification:
    def __init__(self, start_text: str, end_text: str) -> None:
        self.start = start_text
        self.end = end_text

    def __enter__(self):
        gr.Info(self.start)

    def __exit__(self, *args):
        gr.Info(self.end)


def get_file_path(file: gr.File, *, file_type=".*") -> str:
    """
    傳入裝有檔案的list，回傳單個檔案路徑。
    以下錯誤會發起訊息視窗：
    檔案數量異常：檔案數量超過1個、沒有選擇檔案
    檔案不存在：
    """
    if file == None:
        gr.Warning(f"檔案未選擇：請選擇一份檔案。\n檔案格式為：{file_type}")
        return
    try:
        file_path: str = file.name
    except:
        raise gr.Error(f"{file}沒有正確的路徑，其不具有name屬性")

    if not os.path.exists(file_path):
        raise gr.Error(f"檔案不存在：{file_path}")

    if not file_path.endswith(file_type):
        gr.Warning(f"檔案非正確的類型：{file_path}不是{file_type}類型")
        return
    return file_path  # 回傳路徑


def process_file(xml_files, mp4_files):
    xml_path = get_file_path(xml_files, file_type=".xml")
    mp4_path = get_file_path(mp4_files, file_type=".mp4")
    if not (xml_path and mp4_path):  # 確認兩個檔案是否缺少
        return  # 回傳中斷程式

    xml_tree = ET.parse(xml_path)  # 讀取 xml 檔
    clips = xmlH.clips_time_read(xml_tree)  # 讀取剪輯片段

    # with action_notification("正在剪輯您的影片，請耐心等待。", "影片剪輯完成，您可以從Data資料夾中檢視。"):
    #     cliper_tool.rendering(mp4_path, clips, os.path.abspath(".\\edited.mp4"))

    with action_notification("正在匯出剪輯後的編輯檔(xml)，請耐心等待。", "編輯檔匯出完成。"):
        xml_compact_tree = xmlH.clipitem_compact(copy.deepcopy(xml_tree))
        # with open("edited.xml", "w") as file:
        xml_compact_tree.write("edited.xml", encoding="utf-8")

    with action_notification("正在壓縮檔案，請耐心等待。", "壓縮完成，您的影片渲染流程順利完成！"):
        zip_file = zipfile.ZipFile("edited.zip", "w", zipfile.ZIP_DEFLATED, True, 9)
        zip_file.write("edited.mp4")
        zip_file.write("edited.xml")
        zip_file.close()

    return "edited.zip"


with gr.Blocks() as main:  # 建立 gradio
    gr.Markdown("# XML渲染工具٩(ˊᗜˋ )و")
    gr.Markdown("把XML和MP4檔案輸入進來，點擊Run就會開始渲染了！")
    with gr.Row():
        xml_input = gr.inputs.File(file_count="single", label="XML file")
        mp4_input = gr.inputs.File(file_count="single", label="MP4 file")
    with gr.Row():
        clear = gr.ClearButton()
        submit = gr.Button("Run", variant="primary")
    gr.Markdown("## 渲染完成之檔案輸出於下方")
    gr.Markdown("點擊右側檔案大小(連結)，即可儲存檔案。")
    zip_output = gr.outputs.File(label="ZIP file")

    clear.add(xml_input).add(mp4_input).add(zip_output)

    submit.click(fn=process_file, inputs=[xml_input, mp4_input], outputs=[zip_output])

# 啟動 gradio 界面
os.system("start http://127.0.0.1:7860")
main.queue().launch()
