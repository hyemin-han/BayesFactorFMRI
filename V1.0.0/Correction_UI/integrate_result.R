# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


# Integrate X images from X = x to xmax
# For BFs, Means, and Medians

library("oro.nifti")
integrate_result<-function(filename_list = 'mask.nii'){
  # To get a header, read one original file in the list (First item)
  # Read filelist
 # data<-read.csv(filename_list)
 # filecount <-nrow(data)
  
  # Get the first file
 # filename <- toString(data[1,1])
  # Read the current nifti
  Img <- readNIfTI(filename_list)
  # Extract current image data
  ImgData = oro.nifti::img_data(Img)
  
  XX = dim(ImgData)[1]
  YY = dim(ImgData)[2]
  ZZ = dim(ImgData)[3]
  
  # Start with BFs.
  for (i in 1:XX){
  	filename <- sprintf("./output/BF_%d.Rdata",i)
  	# Read the current RData.
  	load (file =filename)
  	# Attach current BFs
  	for (j in 1:YY){
  		for (k in 1:ZZ){
  			ImgData[i,j,k] = BF_current[j,k]
  		}
  	}
  }
  
  # set data type
  datatype(Img)<-64
  bitpix(Img)<-64
  

  # Write BFs.nii
  # Set Image data
  oro.nifti::img_data(Img)<-ImgData
  writeNIfTI(Img,"BFs",gzipped = FALSE)
  
  # Then, Ds
  for (i in 1:XX){
  	filename <- sprintf("./output/D_%d.Rdata",i)
  	# Read the current RData.
  	load (file =filename)
  	# Attach current Mean
  	for (j in 1:YY){
  		for (k in 1:ZZ){
  			ImgData[i,j,k] = D_current[j,k]
  		}
  	}
  }
  
  
  # Write Ds.nii
  # Set Image data
  oro.nifti::img_data(Img)<-ImgData
  writeNIfTI(Img,"Ds",gzipped = FALSE)
  
  # done
  return(1)
}