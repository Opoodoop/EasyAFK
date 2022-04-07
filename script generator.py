import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

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

    with open(path_to_save + '/result.txt', 'w', encoding='utf-8') as f:
        for id, name in get_ids(username).items():
            f.write("start/min steam-idle.exe "+id+"\n")


if __name__ == '__main__':
    main()