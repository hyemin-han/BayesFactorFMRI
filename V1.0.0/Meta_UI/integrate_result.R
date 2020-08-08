# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


# Integrate X images from X = 1 to 91
# For BFs, Means, and Medians

library("oro.nifti")

integrate_result<-function(filename){
  # To get a header, read one original file in the list (First item)
  # Read filelist
  
  Img <- readNIfTI(filename)
  # Extract current image data
  ImgData = oro.nifti::img_data(Img)
  
  # Start with BFs.
  for (i in 1:91){
  	filename <- sprintf("./Outputs/BF%d.Rdata",i)
  	# Read the current RData.
  	load (file =filename)
  	# Attach current BFs
  	for (j in 1:109){
  		for (k in 1:91){
  			ImgData[i,j,k] = BFs[j,k]
  		}
  	}
  }

  # backup
  BFImg = ImgData
  
  # set data type
  datatype(Img)<-64
  bitpix(Img)<-64
  
    
  # Then, Means
  for (i in 1:91){
  	filename <- sprintf("./Outputs/Mean%d.Rdata",i)
  	# Read the current RData.
  	load (file =filename)
  	# Attach current Mean
  	for (j in 1:109){
  		for (k in 1:91){
  			ImgData[i,j,k] = Means[j,k]
  		}
  	}
  }
  
  # Write Means.nii
  # Set Image data
  oro.nifti::img_data(Img)<-ImgData
  writeNIfTI(Img,"Means",gzipped = FALSE)
  
  # write only plus values
  for (i in 1:91){
    for (j in 1:109){
      for (k in 1:91){
        #Nan Pass
        if (is.nan(ImgData[i,j,k])){
          next
        }
        # plus?
        if (ImgData[i,j,k] > 0){
          # write
          ImgData[i,j,k] = BFImg[i,j,k]
        }
        # zero or minus?
        else{
          ImgData[i,j,k] = 0
        }
      }
    }

  }

  # Write BFs.nii
  # Set Image data
  oro.nifti::img_data(Img)<-ImgData
  writeNIfTI(Img,"BFs",gzipped = FALSE)

  # Then, Medians
  for (i in 1:91){
  	filename <- sprintf("./Outputs/Median%d.Rdata",i)
  	# Read the current RData.
  	load (file =filename)
  	# Attach current Median
  	for (j in 1:109){
  		for (k in 1:91){
  			ImgData[i,j,k] = Medians[j,k]
  		}
  	}
  }
  
  # Write Medians.nii
  # Set Image data
  oro.nifti::img_data(Img)<-ImgData
  writeNIfTI(Img,"Medians",gzipped = FALSE)
}