import numpy as np
def _assert_image_shapes_equal(org_img: np.ndarray, pred_img: np.ndarray, metric: str):
    msg = (f"Cannot calculate {metric}. Input shapes not identical. y_true shape ="
           f"{str(org_img.shape)}, y_pred shape = {str(pred_img.shape)}")

    assert org_img.shape == pred_img.shape, msg

def rmse(org_img: np.ndarray, pred_img: np.ndarray, max_p=4095) -> float:
    """
    Root Mean Squared Error
    Calculated individually for all bands, then averaged
    """
    _assert_image_shapes_equal(org_img, pred_img, "RMSE")

    org_img = org_img.astype(np.float32)

    rmse_bands = []
    for i in range(org_img.shape[2]):
        dif = np.subtract(org_img, pred_img)
        m = np.mean(np.square( dif / max_p))
        s = np.sqrt(m)
        rmse_bands.append(s)

    return np.mean(rmse_bands)
