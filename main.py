#!/usr/local/anaconda2/bin/python
from __future__ import print_function
from PA import parse_args
from H5 import Input, Target, LIMBS
from file_validation import load_names
from matplotlib import pyplot as plt
import cv2
import os
import dataproc.skeleton as sk


def h5_initialize(base_dir):
	input_list = ["train_input.h5", "valid_input.h5"]
	target_list = ["train_target.h5", "valid_target.h5"]
	return (Input(base_dir, input_list[0]), Input(base_dir, input_list[1]), 
		Target(base_dir, target_list[0]), Target(base_dir, target_list[1]))


def dataset_process(base_dir, _set, _list):
	[ipt, tgt] = _set
	num = len(_list)
	if num != ipt.count() or num != tgt.count():
		return None
	for i in range(num):
		fn = _list[i]
		fp = os.path.join(base_dir, fn)
		print("[%d/%d] >> %s" % (i + 1, num, fn))
		# show_rank(ipt.rank[i])
		# show_rankMat(ipt.rankMat[i])
		# print(tgt.S3d[i])
		# sk.draw_skel3D_16(tgt.S3d[i])
		# print(tgt.S2d[i])
		img = cv2.cvtColor(cv2.imread(fp, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
		sk.draw_skel2D_16(tgt.S2d[i], img, color=(15,255,78), thick=3)
		plt.imshow(img)
		plt.show()
		break
	print(' >>> ')


def show_rank(mat):
	for i in range(LIMBS):
		print("%d " % mat[i], end='')
	print()


def show_rankMat(mat):
	for i in range(LIMBS):
		for j in range(LIMBS):
			print("%.3f " % mat[i][j], end='')
			pass
		print()
	print()


if __name__ == "__main__":

	option = parse_args()

	bp_annot = option.path_ann
	bp_img = option.path_img

	t_input, v_input, t_target, v_target = h5_initialize(option.dir_data)
	train_set = [t_input, t_target]
	valid_set = [v_input, v_target]
	train_list = load_names(bp_annot, "train_images.txt")
	valid_list = load_names(bp_annot, "valid_images.txt")
	pairs = [(train_set, train_list), (valid_set, valid_list)]

	for _s, _l in pairs:
		dataset_process(bp_img, _s, _l)
		break  # train_set first
