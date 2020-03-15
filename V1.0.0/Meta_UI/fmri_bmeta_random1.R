# Get parameter Correction.
# Three params are needed
# 1: current task number
# 2: X range start
# 3: X range end
# 4: list file name (optional)

args = commandArgs(trailingOnly=TRUE)
if (length(args)<3){
  # Error
  quit(status=1)
}
Current_task = strtoi(args[1])
Range_start = strtoi(args[2])
Range_end = strtoi(args[3])

if (length(args)==3){
  # default setting -> list file
  list <- 'list.csv'

} else  {
  # more than four
  
  if (length(args) == 4){
    list <- args[4]

  } 
}

library("oro.nifti")
library("metaBMA")

# Create output dir
dir.create("Outputs")

# Read filelist
data<-read.csv(list)
filecount <-nrow(data)

filename <- toString(data[1,1])
# Read the first nifti
Img <- readNIfTI(filename)

# get mask size image
X <- dim(Img)[1]
Y <- dim(Img)[2]
Z <- dim(Img)[3]


# Create 4D space
AllImg = array(0.0,c(filecount,X,Y,Z))

# before get started, read config file
config <- read.csv('config.csv')
# get scale value (default = 0.7071068)
configscale<-config$scale[1]
if (!is.numeric(configscale)){
  configscale<-0.7071068
}
# print out the current scale value for information
print(sprintf('Current Cauchy Scale = %f',configscale))

# Read each nifti file
for (i in 1:filecount)  {
	filename <- toString(data[i,1])
	# Read the current nifti
	Img <- readNIfTI(filename)
	
	# Extract current image data
	ImgData = oro.nifti::img_data(Img)
	
	# T or Z
	Type <- toString(data[i,3])
	# n size
	N <- data[i,2]
	
	# Transform to Fisher's Z
	for (x in Range_start:Range_end) {
		for (y in 1:Y) {
			for (z in 1:Z)  {

				# If NaN
				if (is.nan(ImgData[x,y,z])){
					AllImg[i,x,y,z] = NaN
					next
				}
				# If zero
				if (ImgData[x,y,z] == 0){
					AllImg[i,x,y,z] = NaN
					next
				}				
				# T?
				if (Type == 'T'){
					AllImg[i,x,y,z] = ImgData[x,y,z]
					AllImg[i,x,y,z] = sqrt((AllImg[i,x,y,z]*AllImg[i,x,y,z])/(AllImg[i,x,y,z]*AllImg[i,x,y,z]+N-1))*sign(AllImg[i,x,y,z])
					AllImg[i,x,y,z] = atanh(AllImg[i,x,y,z])
				}
				# Z?
				else {
					AllImg[i,x,y,z] = ImgData[x,y,z] / sqrt(N) * sqrt(N-2.0)
					AllImg[i,x,y,z] = sqrt((AllImg[i,x,y,z]*AllImg[i,x,y,z])/(AllImg[i,x,y,z]*AllImg[i,x,y,z]+N-1))*sign(AllImg[i,x,y,z])
					AllImg[i,x,y,z] = atanh(AllImg[i,x,y,z])
				}
			}
		}
	}

}

# Create SE stuff
SE = array (0.0,c(filecount))
for (i in 1:filecount){
	SE[i] = 1/sqrt(data[i,2]-3.0)
}

# Then, perform bayesmeta for each voxel
# When a voxel value in a specific voxel in all images <> 0 or NaN
BFs = array(0.0,c(Y,Z))
Means = array(0.0,c(Y,Z))
Medians = array(0.0,c(Y,Z))

# Current voxel values
voxels = array(filecount)

for (x in Range_start:Range_end)  {
	for (y in 1:Y){
		for (z in 1:Z){
			# Check NaN
			flag <- 0
			for (i in 1:filecount){
				if (is.nan(AllImg[i,x,y,z])){
					flag <- 1
				}
			}
			# NaN found?
			if (flag){
				# Write NaN and exit
				BFs[y,z] <- NaN
				Means[y,z] <- NaN
				Medians[y,z] <- NaN
				next
			}
			# Do Bayesian Analysis
			# Create an array of voxel values
			for (i in 1:filecount){
				voxels[i] = AllImg[i,x,y,z]
			}
			# HNorm and HCauchy
			mr <- meta_random(voxels,SE,d=prior("cauchy",c(scale=configscale)),tau=prior("beta",c(1,2)),summarize="stan")

			BFs[y,z] <- mr$BF[2,1]
			Means[y,z] <- mr$estimates[1,1]
			Medians[y,z] <- mr$estimates[1,4]
			# From Fisher's z to r
			Means[y,z] <- tanh(Means[y,z])
			Medians[y,z] <- tanh(Medians[y,z])
		}
	}

  # notify that the current x is done
  status <- sprintf('%d / %d Done! (Task: %d) \n',x-Range_start+1,Range_end-Range_start+1,Current_task)
  print(status)
  
  # Write results in binary files
  save(BFs,file=sprintf("./Outputs/BF%d.Rdata",x))
  save(Means,file=sprintf("./Outputs/Mean%d.Rdata",x))
  save(Medians,file=sprintf("./Outputs/Median%d.Rdata",x))
}

# notify that the current task is done
result = sprintf("DONE:%d",Current_task)
print(result)