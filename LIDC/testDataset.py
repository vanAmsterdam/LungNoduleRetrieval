import pickle
import numpy as np
import matplotlib.pyplot as plt
import pylidc as pl
from LIDC.lidcUtils import CheckPatch


def test_dicom_rescale_consistency():
    cnt_intercept_errors = 0
    cnt_slope_erros = 0
    for scan in pl.query(pl.Scan).all():
        dicom = scan.load_all_dicom_images(verbose=0)
        intercepts  = [di.RescaleIntercept for di in dicom]
        slopes      = [di.RescaleSlope for di in dicom]

        if np.unique(intercepts) > 1:
            cnt_intercept_errors += 1
            print("int- patient {}".format(scan.patient_id))
        if np.unique(slopes) > 1:
            cnt_slope_erros += 1
            print("slp- patient {}".format(scan.patient_id))

    print('Intercept Errors: {}'.format(cnt_intercept_errors))
    print('Slope Errors: {}'.format(cnt_slope_erros))


if __name__ == "__main__":

    check_patch = False
    check_dicom_consistency = True

    if check_patch:
        plt.interactive(True)
        dataset = pickle.load(open('LIDC/NodulePatchesClique.p', 'br'))
        CheckPatch(dataset[111])

    if check_dicom_consistency:
        test_dicom_rescale_consistency()
