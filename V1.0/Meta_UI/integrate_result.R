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