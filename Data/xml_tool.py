import xml.etree.ElementTree as ET


def clips_time_read(tree: ET.ElementTree) -> list[tuple[float, float]]:
    """
    傳入`ElementTree`
    回傳 clips 片段的時間
    return list[tuple[float, float]]
    """
    xml_sequence = tree.getroot().find("sequence")
    xml_track = xml_sequence.find("media").find("video").find("track")
    rate = int(xml_sequence.find("rate").find("timebase").text)
    clips = []
    for clip in xml_track.findall("clipitem"):
        start_time = int(clip.find("in").text) / rate  # frame
        end_time = int(clip.find("out").text) / rate  # frame
        clips.append((start_time, end_time))
    return clips


def list_path_find(tree: ET.ElementTree, paths: list[str]) -> ET.Element:
    for path in paths:
        tree = tree.find(path)
    return tree


def set_rate(tree: ET.ElementTree, set_rate: int) -> None:
    sequence = tree.getroot().find("sequence")
    track = list_path_find(sequence, ["media", "video", "track"])
    file = list_path_find(track, ["clipitem", "file"])

    sequence_rate = sequence.find("rate").find("timebase")  # 取出置幀率物件
    file_rate = list_path_find(file, ["rate", "timebase"])
    media_rate = list_path_find(
        file, ["media", "video", "samplecharacteristics", "rate", "timebase"]
    )

    sequence_rate.text = set_rate  # 設定幀率
    file_rate.text = set_rate  # 設定幀率
    media_rate.text = set_rate  # 設定幀率


def clipitem_compact(name: str) -> ET.ElementTree:
    xmeml = ET.Element("xmeml", attrib={"version": "4"})
    sequence = ET.SubElement(xmeml, "sequence")
    sequence_name = ET.SubElement(sequence, "name")
    sequence_name.text = name

    for clip in track.findall("clipitem"):
        clip.find("in").text = clip.find("start").text
        clip.find("out").text = clip.find("end").text
    return xmeml
