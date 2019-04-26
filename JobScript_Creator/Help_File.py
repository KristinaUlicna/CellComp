file = open('/Volumes/lowegrp/JobServer/jobs/JOB_SegClass_Kristina_19-04-10_pos0.job.complete', 'r')
print (file)

for line in file:
    line = line.rstrip()
    print (line)

#server directory absolute path: '/Volumes/lowegrp/JobServer/jobs/'

print(os.path.exists("/home/el/myfile.txt"))
#self.job_file = open('/Volumes/lowegrp/Data/{}/{}/'.format(self.user, self.type) + job_name + '.job', 'w')
