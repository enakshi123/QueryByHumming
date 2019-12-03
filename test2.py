import os
import pretty_midi
import numpy as np

#if __name__="__init__" :

# pat = '/home/shashank/Desktop'
# k = pretty_midi.PrettyMIDI(pat,220,120)
# print(k)

SR = 22050
hop_size = 256

def get_path():
    path = os.getcwd()
    path = path[:path.rfind('/')]

    return path

def get_path_to_query():
    query_path = '{0}/Query'.format(get_path())
    return query_path

def get_path_to_dataset_audio():
    audio_path = '{0}/MIDI_database'.format(get_path())
    return audio_path

def get_path_to_database():
    database_path = '{0}/Database'.format(get_path())
    return database_path

def time_to_index(time):
	return int(time*np.float(SR)/np.float(hop_size))


def StoreDB_pitch_estimates(dirlist):

	for track_name in dirlist:
		audio_fpath = '{0}/{1}.mid'.format(get_path_to_dataset_audio(),track_name)
		midi_data = pretty_midi.PrettyMIDI(audio_fpath)

		i=0
		for instrument in midi_data.instruments:
			track_name_new = track_name + str(i)
			note_pitches = []
			onset = []
			offset = []

			if not instrument.is_drum:
				i=i+1

				for note in instrument.notes:

					note_pitches.append(note.pitch)
					onset.append(time_to_index(note.start))
					offset.append(time_to_index(note.end))

				note = [note_pitches,onset,offset]
				note = np.asarray(note)
				#print(note)
				np.save('{0}/pitch_estimates_DB/{1}'.format(get_path_to_database(),track_name_new), note)
		
	return


if __name__ == '__main__':
	vector_length = 300
	stride = 3

	dirlist = []

	for track_name in os.listdir(get_path_to_dataset_audio()):
		dirlist.append(track_name[:track_name.rfind('.')])
		print(track_name)

	StoreDB_pitch_estimates(dirlist)
	print("Pitch estimates stored successfully!\n\n\n\n")


