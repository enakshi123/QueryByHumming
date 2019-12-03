import matplotlib.pyplot as plt 
import path_functions
import statistics 
import numpy as nu 
import h5py 
import scipy
import librosa
import os 
import pickle
import pretty_midi

from path_functions import *
from statistics import mode
from falconn import LSHIndex,Queryable,LSHConstructionParameters,DistanceFunction,LSHFamily,StorageHashTable
from scipy.signal import lfilter, savgol_filter, medfilt

#paramerers of the model are globally defined for the trainded network
number_of_patched = 20
patch_size = 25
segment_length = 500  # number_of_patches * patch_size
feature_size = 301
number_of_classes = 62
SR = 22050
hop_size = 226

def Generate_query_pitch_estimates(track_name):
	audio_fpath = '{0}/{1}.mid'.format(get_path_to_dataset_audio(),track_name)
	midi_data = pretty_midi.PrettyMIDI(audio_fpath)
	pitch_estimates = []

	i=0
	for instrument in midi_data.instruments:
		note_pitches = []
		onset = []
		offset = []

		if not instruments.in_drum:
			i = i+1

			for note in instruments.notes:
				note_pitches.append(node.pitch)
				onset.append(time_to_index(note.start))
				offset.append(time_to_index(note.end))

			pitch_estimates = convert_note_to_pitch_estimates(note_pitches,onset,offset)

	return pitch_estimates[200:1000]

def StoreDB_pitch_estimates(dirList):
  
  for track_name in dirlist:
    audio_fpath = '{0}/{1}.mid'.format(get_path_to_dataset_audio(),track_name)
    midi_data = pretty_midi.PtettyMIDI(audio_fpath)
    
    i=0
    for instrument in midi_data.instruments:
      track_name_new = track_name + str(i)
      note_pitches = []
      onset=[]
      offset=[]
      
      if not instrument.is_drum:
        i+=1
        
        for note in instrument.notes:
          
          note_pitches.append(note.pitch)
          onset.append(time_to_index(note.start))
          offset.append(time_to_index(note.end))
          
        note = [note_pitches,onset,offset]
        note = np.array(note)
        np.save('{0}/pitch_estimates_DB/{1}'.format(get_path_to_database(),track_name_new),note)
        
  return 

def GenerateDB(track_name,pitch_estimates,pitch_vectorDB,pirchvector_index,vector_length,stride):
  
  num_of_pitch_vectors = int((pitch_estimates.size - vector_length)/stride)
  pitch_vectorDB = np.zeros((1,vector_length))

  for i in range (num_of_pitch_vectors):
  	pitch_vectorDB = np.concatinate((pitch_vectorDB,np.matrix(pitch_estimates[stride*i:stride*i+vector_length])),axis = 0)
  	pitchvector_index.append([track_name,time(i)])

  pitch_vectorDB = np.asmatrix(pitch_vectorDB)
  Store_DB(pitch_vectorDB,pitchvector_index,"Vector_Wise_Normalised")
  print("{0} added to dataset, current shape:".format(track_name),pitch_vectorDB.shape)

  return pitch_vectorDB,pitchvector_index

def GenerateDB_freq_normalisation(track_name, pitch_estimates, pitch_vectorDB,pitchvector_index, vector_length,stride):
	
	num_of_pitch_vectors = int((len(pitch_estimates )- vector_length)/stride)

	for i in range(num_of_pitch_vectors):
		pitch_vectors = (freq_normalisation(pitch_estimates[stride*i:stride*i+vector_length]))
		pitch_vectorDB = np.concatinate((pitch_vectorDB,np.matrix(pitch_vector)),axis = 0)
		pitchvector_index.append([track_name,time(i)])

	pitch_vectorDB = np.asmatrix(pitch_vectorDB)

	return pitch_vectorDB, pitchvector_index

def GenerateDB_vectorwise_freq_normalisation(track_name, vector_length=20, stride=3):

	pitch_vectorDB = np.zeros((i.vector_length))
	pitchvector_index = [["Null",0]]

	[note_pitches,onset,offset] = np.load('{0}/pitch_estimates_DB/{1}.npy'.format(get_path_to_database(),track_name))
	pitch_estimates = convert_note_to_pitch_estimates(note_pitches,onset,offset)

	pitch_vectorDB, pitchvector_index = GenerateDB_freq_normalisation(track_name, pitch_estimates,pitch_vectorDB,pitchvector_index,vector_length,stride)

	return pitch_vectorDB, pitchvector_index





      




