import numpy as np
import cv2
from skimage import restoration, exposure


class CZTEnhancedEmulator:
    """
    Emulates the high-definition characteristics of Cadmium Zinc Telluride (CZT) detectors
    by applying advanced image restoration techniques to standard radiographic/scintigraphic data.
    """

    def __init__(self):
        # CZT detectors have better energy resolution, effectively seeing less 'scatter'
        # and sharper edges than NaI crystals.
        pass

    def enrich_image(self, image_array: np.ndarray) -> np.ndarray:
        """
        pipeline:
        1. Denoise (Preserve Edges)
        2. Deconvolution (Recover Resolution / simulate CZT PSF)
        3. CLAHE (Simulate high contrast / scatter rejection)
        """
        # Ensure image is normalized float 0-1
        img_float = image_array.astype(np.float32)
        if img_float.max() > 1.0:
            img_float /= img_float.max()

        # 1. Denoise using Non-local Means (simulating direct conversion low noise)
        # Using fastNlMeansDenoising from OpenCV (converted to uint8 for compat or use skimage)
        # We'll use skimage for float support
        from skimage.restoration import denoise_nl_means, estimate_sigma
        sigma_est = np.mean(estimate_sigma(img_float))
        denoised = denoise_nl_means(img_float, h=1.15*sigma_est, fast_mode=True,
                                    patch_size=5, patch_distance=6)

        # 2. Resolution Recovery (Richardson-Lucy Deconvolution)
        # Simulating the removal of the "blur" from a standard Gamma Camera (NaI)
        # Estimated PSF of a standard collimator (Gaussian approx)
        psf = self._generate_gaussian_psf(shape=(5, 5), sigma=1.0)
        deconvolved = restoration.richardson_lucy(denoised, psf, num_iter=15)

        # 3. Scatter Rejection Simulation (CLAHE)
        # CZT rejects scatter better, leading to higher local contrast
        enhanced = exposure.equalize_adapthist(deconvolved, clip_limit=0.03)

        return enhanced

    def _generate_gaussian_psf(self, shape=(5, 5), sigma=1):
        m, n = [(ss-1.)/2. for ss in shape]
        y, x = np.ogrid[-m:m+1, -n:n+1]
        h = np.exp(-(x*x + y*y) / (2.*sigma*sigma))
        h[h < np.finfo(h.dtype).eps*h.max()] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h
