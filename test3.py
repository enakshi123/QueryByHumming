import os
import pretty_midi
import numpy as np
import random
#from lshash import LSHash
#from numpy import matrix


def get_path():
    path = os.getcwd()
    path = path[:path.rfind('/')]
    

    return path

def get_path_to_database():
    database_path = '{0}/Database'.format(get_path())
    return database_path


def get_path_to_pitch_estimates():
    pitch_path = '{0}/pitch_estimates_DB'.format(get_path_to_database())
    return pitch_path

i=0;
all=np.array([])
a = get_path_to_pitch_estimates()
#print(a)
os.chdir(a)
#b = os.chdir(a)
#print(os.getcwd())
#dataSet=np.array(())
#i=0
dataSet=[]
for track in os.listdir(os.getcwd()):
	#print(track)
    arr1 = np.load(track)
    #arr = np.array(arr1)
    #print(arr1)
    dataSet.append(arr1)
    
   
#print(np.ndim(dataSet))

        




def get_pat():
    #pat = os.getcwd()
    #pat = pat[:pat.rfind('/')]
    #print(pat)
    
    pat='/home/sathwik/Desktop/QBH'
    return pat

    
def get_path_to_databas():
    database_pat = '{0}/querydatabase'.format(get_pat())
    return database_pat


def get_path_to_pitch_estimate():
    pitch_pat = '{0}/pitch_query_DB'.format(get_path_to_databas())
    return pitch_pat

i=0;
all=np.array([])
a = get_path_to_pitch_estimate()
#print(a)
os.chdir(a)
#b = os.chdir(a)
#print(os.getcwd())
for track in os.listdir(os.getcwd()):
	#print(track)
	arr2 = np.load(track)
	#print(arr2)
quer = arr2
print(quer)
#print(dataSet)


	#i = i+1
	#if i >0:
		#break
	#all = np.append(all,arr1)
	#print(arr1)
#print(all[1])
# for name in os.listdir(get_path_to_pitch_estimates()):
#     os.chdir(get_path_to_pitch_estimates())
# 	#full_path=os.path.join(get_path_to_pitch_estimates(),name)
#     foo = np.load(name)
	
	# i=i+1
	# print(data)
	# if i >10:
	# 	break
import falconn
number=len(quer)
def search(dataset,quer,number):
    params_cp = falconn.LSHConstructionParameters()
    params_cp.dimension = len(dataset)
    params_cp.lsh_family = falconn.LSHFamily.CrossPolytope
    params_cp.distance_function = falconn.DistanceFunction.EuclideanSquared
    params_cp.l = 50
    # we set one rotation, since the data is dense enough,
    # for sparse data set it to 2
    params_cp.num_rotations = 1
    params_cp.seed = 5721840
    # we want to use all the available threads to set up
    params_cp.num_setup_threads = 0
    params_cp.storage_hash_table = falconn.StorageHashTable.BitPackedFlatHashTable
    # we build 18-bit hashes so that each table has
    # 2^18 bins; this is a good choise since 2^18 is of the same
    # order of magnitude as the number of data points
    falconn.compute_number_of_hash_functions(18, params_cp)
    table = falconn.LSHIndex(params_cp)
    table.setup(dataset)
    query_object = table.construct_query_object()
    number_of_probes = 30000
    query_object.set_num_probes(number_of_probes)
    result = query_object.find_k_nearest_neighbors(query,number)
    return result
print(search(dataSet,quer,number))










