import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

begining = "@echo off\necho welcome to opoodoop's steam afk script\n\n## here you can change the directory for idle master \n## download idle master here https://github.com/JonasNilson/idle_master_extended/releases \n\nCD [Idle master directory here]\n\n"
TheEnd = "\necho stop afking?\npause\ntaskkill /IM \"steam-idle.exe\" /F"

def get_steam_xml(username):
    xml_url = 'http://steamcommunity.com/id/{}/games?tab=all&xml=1'.format(
        username)
    return urllib.request.urlopen(xml_url)


def get_ids(username):
    tree = ET.parse(get_steam_xml(username))
    root = tree.getroot()

    if root.find('error') is not None:
        print(root.find('error').text)
        sys.exit(0)

    return {game.find('appID').text: game.find("name").text for game in root.iter('game')}


def main():
    username = input('Steam username: ')
    path_to_save = ""

    if path_to_save == '':
        path_to_save = '.'
    else:
        path_to_save = path_to_save.replace('\\', '/')
        if path_to_save[-1:] == '/':
            path_to_save = path_to_save[:-1]

    if not os.path.isdir(path_to_save):
        print('Directory does not exist')
        sys.exit(0)

    with open(path_to_save + '/result.bat', 'w', encoding='utf-8') as f:
        f.write(begining)
        for id, name in get_ids(username).items():
            f.write("start/min steam-idle.exe "+id+"\necho sucsessfully started game \""+name+"\" \n")
        f.write(TheEnd)



if __name__ == '__main__':
    main()