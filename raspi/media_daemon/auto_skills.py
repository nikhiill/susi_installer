import os
import sys
from glob import glob
import shutil

# To get media_daemon folder
if len(sys.argv) <= 1:
    raise Exception('Missing argument')

mntpt = sys.argv[1]
media_daemon_folder = os.path.dirname(os.path.abspath(__file__))
base_folder = os.path.dirname(os.path.dirname(os.path.dirname(media_daemon_folder)))
server_skill_folder = os.path.join(base_folder, 'susi_server/data/generic_skills/media_discovery')

def make_skill(): # pylint-enable
    mp3_files = glob(mntpt + '/**/*.[mM][pP]3', recursive = True)
    ogg_files = glob(mntpt + '/**/*.[oO]gg', recursive = True)
    flac_files = glob(mntpt + '/**/*.flac', recursive = True)
    wav_files = glob(mntpt + '/**/*.wav', recursive = True)
    f = open( '/home/pi/SUSI.AI/susi_installer/raspi/media_daemon/custom_skill.txt','w')
    music_path = list()
    for mp in mp3_files:
        music_path.append("{}".format(mp))
    for ogg in ogg_files:
        music_path.append("{}".format(ogg))
    for flac in flac_files:
        music_path.append("{}".format(flac))
    for wav in wav_files:
        music_path.append("{}".format(wav))
    # we choose ; as separation char since this seems not to be used in
    # any normal file system path naming
    song_list = ";".join( map ( lambda x: "file://" + x, music_path ) )
    # TODO format of the skill looks strange!!!
    skills = ['play audio','!console:Playing audio from your usb device','{"actions":[','{"type":"audio_play", "identifier_type":"url", "identifier":"' + str(song_list) +'"}',']}','eol']
    for skill in skills:
        f.write(skill + '\n')
    f.close()
    shutil.move(os.path.join(media_daemon_folder, 'custom_skill.txt'), os.path.join(server_skill_folder, 'custom_skill.txt'))

if __name__ == '__main__':
    make_skill()
