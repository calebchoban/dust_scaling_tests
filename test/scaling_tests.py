import sys
import os



"""
 Creates GIZMO exectuables and submits job scripts 
"""

# Edit these to set the number of nodes, OMP_THREADS and what run options you want
# to run scaling tests on
num_nodes = [16,32,64]
num_threads = [1,2,4]
options = ['dust','no_dust']

# This is the snapshot you want to restart the scaling tests from
IC_snapshot = 'snapshot_112.hdf5'


###############################################################################################

# Get names of files in runs which have restart snapshots
# and copy over restart snapshot to scaling folder
target_dir = './runs/'
run_folders = []
init_folders = []

for i,name in enumerate(os.listdir(target_dir)):
	path = os.path.join(target_dir, name)
	if os.path.isdir(path):
		init_folders += [os.path.join(target_dir, name) + '/init/']
		run_folders += [os.path.join(target_dir, name) + '/scaling/']
		for option in options:
			try:
				os.makedirs(os.path.join(run_folders[-1],option + '/'))
			except:
				print("Scaling folder %s already exists" % os.path.join(run_folders[-1],option + '/'))
			os.system('cp ' + init_folders + option + '_output/' + IC_snapshot + ' ' + os.path.join(run_folders[-1],option))


finname = 'template/Config.sh'
f=open(finname)
dars = f.readlines()
f.close()

# Create the Config files for each of the runs and compile GIZMO

foutname = 'Config.sh'

for run_folder in run_folders:
	for option in options:
		for thread in num_threads:
			GIZMOname = 'GIZMO_' + option + '_t' + str(thread)

			# Edit Config file to have appropriate arguments
			g = open(foutname, 'w')
			linecount = 0
			for line in dars:
				linecount = linecount + 1
				if (linecount == 1):
					print 'OPENMP='+str(thread)
					g.write('OPENMP='+str(thread)+'\n')
				else:
					g.write(line)
			if option == 'dust':
				g.write('\nDUST\nSPECIES\n')
			g.close()

			# Compile GIZMO with Config file
			os.system('make compile')
			os.system('cp GIZMO ' + run_folder + '/' + option + '/' + GIZMOname)
			os.system('rm GIZMO')

# Copy over parameters file

finname = 'template/restart_parameters.txt'
f=open(finname)
dars = f.readlines()
f.close()

for run_folder in run_folders:
	for option in options:
		for thread in num_threads:
			for nodes in num_nodes:

				param_name = os.path.join(run_folder + option + '/', 'restart_param_t' + str(thread) + '_n' + str(nodes) + '.txt')

				# Edit param file to have appropriate arguments
				g = open(param_name, 'w')
				linecount = 0
				for line in dars:
					linecount = linecount + 1
					if linecount == 6:
						g.write("InitCondFile\t" + IC_snapshot +'\n')
					elif linecount == 7:
						g.write("OutputDir\toutput" + '_t' + str(thread) + '_n' + str(nodes) + '/')
					else:
						g.write(line)
				g.close()



# Now create the job scripts for each of the runs and submit them to the queue

finname = 'template/restart_job.sh'
f=open(finname)
dars = f.readlines()
f.close()

for run_folder in run_folders:
	for option in options:
		for thread in num_threads:
			for nodes in num_nodes:
				GIZMO_name = 'GIZMO_' + option + '_t' + str(thread)
				param_name = 'restart_param_t' + str(thread) + '_n' + str(nodes) + '.txt'
				job_name = 'job_' + option + '_t' + str(thread) + '_n' + str(nodes) + '.sh'

				# Edit Config file to have appropriate arguments
				g = open(job_name, 'w')
				linecount = 0
				for line in dars:
					linecount = linecount + 1
					if (linecount == 2):
						g.write('#SBATCH -J scaling_' + option + '_t' + str(thread) + '_n' + str(nodes)+'\n')
					elif (linecount == 5):
						g.write('#SBATCH --nodes=' + str(nodes)+'\n')
					elif (linecount == 6):
						g.write('#SBATCH --ntasks-per-node=' + str(48/thread)+'\n')
					elif (linecount == 10):
						g.write('#SBATCH -o ' + option + '_t' + str(thread) + '_n' + str(nodes) + '.log'+'\n')
					elif (linecount == 17):
						g.write('export OMP_NUM_THREADS=' + str(thread)+'\n')
					elif (linecount == 21):
						g.write('$MPIRUN tacc_affinity ./GIZMO_' + option + '_t' + str(thread) + ' ' + param_name + ' 2'+'\n')
					else:
						g.write(line)
				g.close()

				os.system('cp ' + job_name + ' ' + run_folder + '/' + option + '/')
				os.system('rm ' + job_name)


# Now submit jobs to the queue

for run_folder in run_folders:
	for option in options:
		for thread in num_threads:
			for nodes in num_nodes:
				job_name = 'job_' + option + '_t' + str(thread) + '_n' + str(nodes) + '.sh'
				os.system('cd ' + run_folder + 'scaling/' + option + ' && sbatch ' + job_name)