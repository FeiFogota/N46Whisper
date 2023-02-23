# -*- coding: utf-8 -*-
#
# python-srt2ass: https://github.com/ewwink/python-srt2ass
# by: ewwink
# modified by:  一堂宁宁

import sys
import os
import re
import codecs


def fileopen(input_file):
    # use correct codec to encode the input file
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    tmp = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="r", encoding=enc) as fd:
                # return an instance of StreamReaderWriter
                tmp = fd.read()
                break
        except:
            # print enc + ' failed'
            continue
    return [tmp, enc]


def srt2ass(input_file,sub_style):
    if '.ass' in input_file:
        return input_file

    if not os.path.isfile(input_file):
        print(input_file + ' not exist')
        return

    src = fileopen(input_file)
    tmp = src[0]
    # encoding = src[1] # Will not encode so do not need to pass codec para
    src = ''
    utf8bom = ''

    if u'\ufeff' in tmp:
        tmp = tmp.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'
    
    tmp = tmp.replace("\r", "")
    lines = [x.strip() for x in tmp.split("\n") if x.strip()]
    subLines = ''
    tmpLines = ''
    lineCount = 0
    output_file = '.'.join(input_file.split('.')[:-1])
    output_file += '.ass'

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and re.match('-?\d\d:\d\d:\d\d', lines[(ln+1)]):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if re.match('-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0')
                if sub_style =='default':
                    tmpLines += 'Dialogue: 0,' + line + ',default,,0,0,0,,'
                elif sub_style =='ikedaCN':
                    tmpLines += 'Dialogue: 0,' + line + ',池田字幕1080p,,0,0,0,,'
                elif sub_style == 'sugawaraCN':
                    tmpLines += 'Dialogue: 0,' + line + ',中字 1080P,,0,0,0,,'
                elif sub_style == 'kaedeCN':
                    tmpLines += 'Dialogue: 0,' + line + ',den SR红色,,0,0,0,,'
            else:
                if lineCount < 2:
                    tmpLines += line
                else:
                    tmpLines += "\n" + line
            lineCount += 1
        ln += 1


    subLines += tmpLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)
    # replace style
    # subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    # subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    # subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    # subLines = re.sub(r'</font>', "", subLines)

    if sub_style == 'default':
        head_str = head_str_default
    elif sub_style == 'ikedaCN':
        head_str = head_str_ikeda
    elif sub_style == 'sugawaraCN':
        head_str = head_str_sugawara
    elif sub_style == 'kaedeCN':
        head_str = head_str_kaede

    output_str = utf8bom + head_str + '\n' + subLines
    # encode again for head string
    output_str = output_str.encode('utf8')

    with open(output_file, 'wb') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\')
    output_file = output_file.replace('/', '//')
    return output_file


# if len(sys.argv) > 1:
#     for name in sys.argv[1:]:
#         srt2ass(name,sub_style=)


head_str_default = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: default,Meiryo,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00050506,-1,0,0,0,100,100,5,0,1,3.5,0,2,135,135,10,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text'''



head_str_ikeda = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubStyle,Arial,20,&H0300FFFF,&H00FFFFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,3,2,0,2,10,10,10,1
Style: 池田字幕1080p,思源黑体,70,&H00FFFFFF,&H000000FF,&H00008A11,&H00000000,-1,0,0,0,100,100,1.5,0,1,2,1,2,8,8,5,1
Style: staff1080p,思源黑体,55,&H00FFFFFF,&H00FFFFFF,&H34000000,&H00000000,-1,0,0,0,100,100,2.25,0,1,2.5,0,7,12,10,4,1
Style: 注释1080p,思源宋体,55,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,8,8,8,10,1
Style: 歌词1080p,方正兰亭圆_GBK,60,&H00FCFDFD,&H000000FF,&H00000000,&H00030202,-1,0,0,0,100,100,0,0,1,1.5,1.5,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.30,0:00:03.00,staff1080p,,0,0,0,,特蕾纱熊猫观察会'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：'''


head_str_sugawara = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: 中字 1080P,思源黑体 CN Medium,90,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,3.5,0,2,135,135,10,1
Style: staff 1080P,思源宋体 CN Medium,70,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,4,2,7,10,10,10,1
Style: 标注 1080P,思源黑体 CN Medium,70,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: 中字 720P,思源黑体 CN Medium,60,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,3,0,2,135,135,10,1
Style: staff 720P,思源宋体 CN Medium,50,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,3,2,7,10,10,10,1
Style: 标注 720P,思源黑体 CN Medium,50,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: staff msg,思源宋体 CN Medium,25,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,4,2,7,10,10,10,1
Style: 中字 msg,思源黑体 CN Medium,25,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,4,0,2,135,135,10,1
Style: 标注 msg,思源黑体 CN Medium,25,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: 歌词日语 1080P,Swei Spring Sugar CJKtc,60,&H00FFFFFF,&H000000FF,&H009B46A5,&H5A9B46A5,0,0,0,0,100,100,0,0,1,2,0,2,10,10,30,1
Style: 歌词中文 1080P,Swei Spring Sugar CJKtc,90,&H00FFFFFF,&H000000FF,&H009B46A5,&H5F9B46A5,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,100,1
Style: 歌词中文 720P,Swei Spring Sugar CJKtc,60,&H00FFFFFF,&H000000FF,&H009B46A5,&H5F9B46A5,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,70,1
Style: 歌词日语 720P,Swei Spring Sugar CJKtc,40,&H00FFFFFF,&H000000FF,&H009B46A5,&H5A9B46A5,0,0,0,0,100,100,0,0,1,1,0,2,10,10,15,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.24,staff 1080P,,0,0,0,,{'''+r'''\fad(1200,50)\pos(15.2,0.4)}菅原咲月字幕组'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：'''


head_str_kaede = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: staff,微软雅黑,60,&H00FFFFFF,&H00923782,&H0076137B,&H00540D67,-1,0,0,0,100,100,0,0,1,3,0,7,15,15,15,1
Style: den SR红色,微软雅黑,70,&H0AFFFFFF,&H004B4B9E,&H322828E0,&H640A0A72,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,70,1
Style: 注释,微软雅黑,68,&H00FFFFFF,&H000000FF,&H3D000000,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,4.5,0,8,23,23,23,1
Style: 红色,微软雅黑,75,&H00FFFFFF,&H000000FF,&H004243CB,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,15,1
Style: den - 中文歌词,微软雅黑,70,&H0AFFFFFF,&H004B4B9E,&H322828E0,&H640A0A72,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,70,1
Style: den - 日文歌词,微软雅黑,50,&H0AFFFFFF,&H00F9F9F9,&H32000001,&H640A0A72,-1,0,0,0,100,100,0,0,1,1,0,2,15,15,9,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,staff,,0,0,0,,{'''+r'''\fad(300,300)}「三番目の楓」'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：'''
