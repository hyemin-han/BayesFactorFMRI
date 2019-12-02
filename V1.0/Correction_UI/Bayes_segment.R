library(BayesFactor)
library("oro.nifti")

# Get parameter Correction.
# Four params are needed
# 1: current task number
# 2: X range start
# 3: X range end
# 4: gamma for Cauchy prior
# 5: list file name (optional)
# 6: mask img file name (optional)
args = commandArgs(trailingOnly=TRUE)
# if there are no four params, error
if (length(args)<4){
    # Error
  quit(status=1)
}
Current_task = strtoi(args[1])
Range_start = strtoi(args[2])
Range_end = strtoi(args[3])
Correction = as.double(args[4])


if (length(args)==4){
  # default setting -> list file
  list <- 'list.csv'
  filename_mask <- 'mask.nii'
} else  {
  # more than four

  if (length(args) == 5){
    list <- args[5]
    filename_mask <- 'mask.nii'
  } else{
    list <- args[5]
    filename_mask = args[6]
  }
    
}

scale_current = Correction

# read file list
data<-read.csv(list)
filecount <-nrow(data)

# read mask file
MaskImg <- readNIfTI(filename_mask)
MaskImgData = oro.nifti::img_data(MaskImg)

# get mask size image
X <- dim(MaskImg)[1]
Y <- dim(MaskImg)[2]
Z <- dim(MaskImg)[3]

# Create 4D space
AllImg = array(0.0,c(X,Y,Z, filecount))

# Create result BF image space
BFImg = array(0.0,c(X,Y,Z))
# Create result D image space
DImg = array(0.0,c(X,Y,Z))

for (i in 1:filecount)  {
	filename <- toString(data[i,1])
	# Read the current nifti
	Img <- readNIfTI(filename)
	
	# Extract current image data
	ImgData = oro.nifti::img_data(Img)
	
	# copy to the AllImg
	for (x in 1:X){
		for (y in 1:Y){
			for (z in 1:Z){
				AllImg[x,y,z,i] <- ImgData[x,y,z]
			}
		}
	}
}

# then, when mask is not 0 & not nan
# for each voxel, do ttestBF with the modified prior
for (i in Range_start:Range_end){
	for (j in 1:Y){
		for (k in 1:Z){
			# check whether nan or zero
			if ((MaskImgData[i,j,k]==0) || (is.nan(MaskImgData[i,j,k])) ){
				# do nothing
			}
			else
			{


				# do ttestBF
				BF <- ttestBF(x=AllImg[i,j,k,1:filecount],rscale=scale_current, nullInterval=c(0,Inf))
				# get bf value
				bf <- as.data.frame(BF)
				bf10 <- bf$bf[1]
				# get median effect size
				suppressMessages(GETMEAN <- posterior(BF[1], iteration = 10000))
				getmean <- as.data.frame(GETMEAN)
				delta <- median(getmean$delta)
				# store value in maps
				BFImg[i,j,k]<-bf10
				DImg[i,j,k]<-delta
				
				

			}
		}
	}
	# notify that the current x is done
	status <- sprintf('%d / %d Done! (Task: %d) \n',i-Range_start+1,Range_end-Range_start+1,Current_task)
	print(status)
	
	# at the end of each x, store the current BFImg and DImg
	dir.create('output')
	BF_result <- sprintf("./output/BF_%d.Rdata",i)
	D_result <- sprintf("./output/D_%d.Rdata",i)
	BF_current <- BFImg[i,1:Y,1:Z]
	D_current <- DImg[i,1:Y,1:Z]
	save(BF_current,file=BF_result)
	save(D_current,file=D_result)
}

# notify that the current task is done
result = sprintf("DONE:%d",Current_task)
print(result)
