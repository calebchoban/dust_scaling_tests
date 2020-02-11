import sys
import os



"""
 Creates GIZMO exectuables and submits job scripts 
"""

num_nodes = [16,32,64]
num_threads = [1,2,4]
options = ['dust','no_dust']

#num_nodes = [16]
#num_threads = [1]
#options = ['dust']

finname = 'template/Config.sh'
f=open(finname)
dars = f.readlines()
f.close()

# Create the Config files for each of the runs and compile GIZMO

foutname = 'Config.sh'

for option in options:
	for thread in num_threads:
		GIZMOname = 'GIZMO_' + option + '_' + str(thread)

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
		os.system('cp GIZMO runs/GIZMO_'+option+'_t'+str(threads))
		os.system('rm GIZMO')


# Now create the job scripts for each of the runs and submit them to the queue

finname = 'template/restart_job.sh'
f=open(finname)
dars = f.readlines()
f.close()

for option in options:
	for thread in num_threads:
		for nodes in num_nodes:
			GIZMO_name = 'GIZMO_' + option + '_t' + str(thread)
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
					g.write('$MPIRUN tacc_affinity ./GIZMO_' + option + '_t' + str(thread) + ' gizmo_parameters.txt 2'+'\n')
				else:
					g.write(line)
			g.close()

			os.system('cp ' + job_name + ' ./runs/')
			os.system('rm ' + job_name)
