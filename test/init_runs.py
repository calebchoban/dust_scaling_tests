import sys
import os
import shutil



"""
 Creates GIZMO exectuables and submits job scripts 
"""

options = ['dust','no_dust']


# Copy over ICs from MUSIC
music_path = '../music/run/'
target_dir = './runs/'
IC_folders = []
IC_names = []

for i,name in enumerate(os.listdir(music_path)):
	path = os.path.join(music_path, name)
	if os.path.isdir(path):
		target_folder = os.path.join(target_dir, name)
		music_folder = os.path.join(music_path, name)
		for j,file in enumerate(os.listdir(music_folder)):
			if file.endswith(".ics"):
				try:
					os.mkdir(target_folder)
				except:
					print("Target folder %s already exists" % target_folder)
				try:
					os.mkdir(target_folder + '/init')
				except:
					print("Target folder %s already exists" % target_folder)
				IC_folders += [target_folder + '/init/']
				IC_names += [os.path.join(target_folder, file)]
				shutil.copy2(os.path.join(music_folder, file), target_folder + '/init/')

# Copy over parameters file

finname = 'template/init_parameters.txt'
f=open(finname)
dars = f.readlines()
f.close()

for i in range(len(IC_names)):
	ic = IC_names[i].split('/')[-1]
	folder = IC_folders[i]

	for option in options:
		param_name = os.path.join(folder, 'parameters_' + option + '.txt')

		# Edit param file to have appropriate arguments
		g = open(param_name, 'w')
		linecount = 0
		for line in dars:
			linecount = linecount + 1
			if linecount == 6:
				g.write("InitCondFile\t" + ic +'\n')
			elif linecount == 7:
				g.write("OutputDir\t" + option + '_output/\n')
			else:
				g.write(line)
		g.close()

# Copy over TREECOOL and snapshot_timescale files
for folder in IC_folders:
	os.system('cp TREECOOL ' + folder)
	os.system('cp template/snapshot_scale-factors.txt ' + folder)
	os.system('cp -r spcool_tables ' + folder)


# Create the Config files for each of the runs and compile GIZMO

finname = 'template/Config.sh'
f=open(finname)
dars = f.readlines()
f.close()

foutname = 'Config.sh'

for option in options:
	for i in range(len(IC_names)):
		ic = IC_names[i]
		folder = IC_folders[i]
		GIZMOname = 'GIZMO_' + option

		# Edit Config file to have appropriate arguments
		g = open(foutname, 'w')
		linecount = 0
		for line in dars:
			linecount = linecount + 1
			g.write(line)
		if option == 'dust':
			g.write('\nDUST\nSPECIES\n')
		g.close()

		# Compile GIZMO with Config file
		os.system('make compile')
		os.system('cp GIZMO ' + folder + '/GIZMO_'+option)
		os.system('rm GIZMO Config.sh')

# Now create the job scripts for each of the runs and submit them to the queue

finname = 'template/init_job.sh'
f=open(finname)
dars = f.readlines()
f.close()

for folder in IC_folders:
	name = folder.split('/')[-1]
	for option in options:
			GIZMO_name = 'GIZMO_' + option
			job_name = 'job_' + option + '.sh'

			# Edit Config file to have appropriate arguments
			g = open(job_name, 'w')
			linecount = 0
			for line in dars:
				linecount = linecount + 1
				if (linecount == 2):
					g.write('#SBATCH -J ' + name + '_' + option + '\n')
				if (linecount == 10):
					g.write('#SBATCH -o ' + option + '_job.log\n')
				elif (linecount == 24):
					g.write('\t$MPIRUN tacc_affinity ./' + GIZMO_name + ' parameters_' + option + '.txt 1\n')
				elif (linecount == 27):
					g.write('\t$MPIRUN tacc_affinity ./' + GIZMO_name + ' parameters_' + option + '.txt\n')
				else:
					g.write(line)
			g.close()

			os.system('cp ' + job_name + ' ' + folder)
			os.system('rm ' + job_name)

# Now submit jobs to the queue
for folder in IC_folders:
	name = folder.split('/')[-1]
	for option in options:
			job_name = 'job_' + option + '.sh'
			os.system('cd ' + folder + ' && sbatch ' + job_name)