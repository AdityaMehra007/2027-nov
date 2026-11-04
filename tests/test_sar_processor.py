import pytest
from omniverse.modules.aether.sar_processor import SARProcessor, FloodExtentMask

def test_sar_otsu_threshold_bimodal():
    processor = SARProcessor()
    # Bimodal distribution: water (-22 to -18 dB) and land (-12 to -8 dB)
    water_samples = [-22.0, -21.5, -20.0, -19.5, -18.5, -19.0, -20.5]
    land_samples = [-11.0, -10.5, -9.0, -9.5, -8.5, -10.0, -11.5]
    samples = water_samples + land_samples

    thresh = processor.compute_otsu_threshold(samples)
    # Threshold should sit cleanly in valley between -18 and -12
    assert -18.0 <= thresh <= -12.0

def test_sar_swath_inundation_mapping():
    processor = SARProcessor()
    # 10x10 pixel grid with 30 water pixels
    grid = [-20.0] * 30 + [-10.0] * 70
    mask = processor.process_sar_swath(
        area_name="Brahmaputra Flood Plain",
        backscatter_db_grid=grid,
        pixel_resolution_m=100.0  # 100m resolution -> 10,000 m2 per pixel = 0.01 km2
    )

    assert isinstance(mask, FloodExtentMask)
    assert mask.total_pixels == 100
    assert mask.water_pixels == 30
    # 30 * 0.01 km2 = 0.30 km2
    assert round(mask.inundation_area_km2, 2) == 0.30
    assert mask.confidence_score >= 90.0
