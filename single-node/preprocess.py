
import os
import numpy as np

def load_data(data_path, prefix = "_train"):
	imgs_train = np.load(os.path.join(data_path, "imgs"+prefix+".npy"),
						 mmap_mode="r", allow_pickle=False)
	msks_train = np.load(os.path.join(data_path, "msks"+prefix+".npy"),
						 mmap_mode="r", allow_pickle=False)

	return imgs_train, msks_train

def update_channels(imgs, msks, input_no=3, output_no=3, mode=1):
	"""
	mode: int between 1-3
	"""

	imgs = imgs.astype("float32")
	msks = msks.astype("float32")

	shp = imgs.shape
	new_imgs = np.zeros((shp[0],shp[1],shp[2],input_no))
	new_msks = np.zeros((shp[0],shp[1],shp[2],output_no))


	if mode == 1:
		# Entire tumor (all 4 modalities combined)
		new_imgs[:,:,:,0] = imgs[:,:,:,2]
		new_msks[:,:,:,0] = msks[:,:,:,0]+msks[:,:,:,1]+msks[:,:,:,2]+msks[:,:,:,3]

	elif mode == 2:
		# Active tumor
		new_imgs[:,:,:,0] = imgs[:,:,:,0]
		new_msks[:,:,:,0] = msks[:,:,:,3]

	elif mode == 3:
		# Active core (necrosis, enchancing, non-enchancing)
		new_imgs[:,:,:,0] = imgs[:,:,:,1]
		new_msks[:,:,:,0] = msks[:,:,:,0]+msks[:,:,:,2]+msks[:,:,:,3]

	else:
		print("Error mode must be 1, 2, or 3 for entire tumor, active tumor, or active core")

	return new_imgs, new_msks