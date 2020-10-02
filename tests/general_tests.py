import os
import tempfile

from winnow.storage.repr_storage import ReprStorage
from winnow.storage.repr_utils import path_resolver, bulk_read

os.environ['WINNOW_CONFIG'] = os.path.abspath('config.yaml')
import pytest
import numpy as np
from winnow.feature_extraction import IntermediateCnnExtractor, FrameToVideoRepresentation, SimilarityModel
from winnow.utils import scan_videos, create_video_list, get_hash,resolve_config
import yaml
from pathlib import Path

NUMBER_OF_TEST_VIDEOS = 40

representations = ['frame_level', 'video_level', 'video_signatures']

cfg = resolve_config(config_path="tests/config.yaml")

# Load main config variables from the TEST config file

DATASET_DIR = cfg.sources.root
DST_DIR = cfg.repr.directory
VIDEO_LIST_TXT = cfg.processing.video_list_filename
USE_DB = cfg.database.use
CONNINFO = cfg.database.uri
KEEP_FILES = cfg.processing.keep_fileoutput
HANDLE_DARK = cfg.processing.filter_dark_videos
DETECT_SCENES = cfg.processing.detect_scenes
MIN_VIDEO_DURATION = cfg.processing.min_video_duration_seconds
DISTANCE = float(cfg.processing.match_distance)

supported_video_extensions = ['.mp4', '.ogv', '.webm', '.avi']


# Ensures that the config file follows specs
def test_config_input():
    assert type(DATASET_DIR) == str, 'video_source_folder takes a string as a parameter'
    assert type(DST_DIR) == str, 'destination_folder takes a string as a parameter'
    assert type(USE_DB) == bool, 'use_db takes a boolean as a parameter'
    assert type(CONNINFO) == str, 'use_db takes a boolean as a parameter'


@pytest.fixture(scope="module")
def reprs():
    """Fixture that creates an empty representation folder in a temporary directory."""
    with tempfile.TemporaryDirectory(prefix="representations-") as directory:
        yield ReprStorage(directory=directory)


@pytest.fixture(scope="module")
def videos():
    """Paths of videos in a test_data."""
    return scan_videos(DATASET_DIR, '**', extensions=supported_video_extensions)


@pytest.fixture(scope="module")
def dataset_path_hash_pairs(videos):
    """(path_inside_storage,sha256) pairs for test dataset videos."""
    storepath = path_resolver(source_root=DATASET_DIR)
    return [(storepath(path), get_hash(path)) for path in videos]


@pytest.fixture(scope="module")
def intermediate_cnn_results(videos, reprs):
    """Ensure processing by intermediate CNN is done.

    Each test dependent on this fixture is guaranteed to be
    executed AFTER processing by the intermediate CNN is done.

    Returns:
        ReprStorage with populated with intermediate CNN results.
    """
    storepath = path_resolver(source_root=DATASET_DIR)
    videos_list = create_video_list(videos, VIDEO_LIST_TXT)
    extractor = IntermediateCnnExtractor(videos_list, reprs, storepath)
    extractor.start(batch_size=16, cores=4)
    return reprs


@pytest.fixture(scope="module")
def frame_to_video_results(intermediate_cnn_results):
    """Ensure video-level features are extracted.

    Each test dependent on this fixture is guaranteed to be
    executed AFTER video-level features extraction is done.

    Returns:
        ReprStorage populated with video-level features.
    """
    reprs = intermediate_cnn_results
    converter = FrameToVideoRepresentation(reprs)
    converter.start()
    return reprs


@pytest.fixture(scope="module")
def signatures(frame_to_video_results):
    """Get calculated signatures as a dict.

    Each test dependent on this fixture is guaranteed to be
    executed AFTER signatures are calculated.

    Returns:
        Signatures dict (orig_path,hash) => signature.
    """
    reprs = frame_to_video_results
    sm = SimilarityModel()
    signatures = sm.predict(bulk_read(reprs.video_level))
    for (path, sha256), sig_value in signatures.items():
        reprs.signature.write(path, sha256, sig_value)
    return signatures


def test_video_extension_filter(videos):
    not_videos = sum(Path(video).suffix not in supported_video_extensions for video in videos)

    assert not_videos == 0


def test_intermediate_cnn_extractor(intermediate_cnn_results, dataset_path_hash_pairs):
    assert set(intermediate_cnn_results.frame_level.list()) == set(dataset_path_hash_pairs)

    frame_level_features = list(bulk_read(intermediate_cnn_results.frame_level).values())

    shapes_correct = sum(features.shape[1] == 4096 for features in frame_level_features)

    assert shapes_correct == len(dataset_path_hash_pairs)


def test_frame_to_video_converter(frame_to_video_results, dataset_path_hash_pairs):
    assert set(frame_to_video_results.video_level.list()) == set(dataset_path_hash_pairs)

    video_level_features = np.array(list(bulk_read(frame_to_video_results.video_level).values()))

    assert video_level_features.shape == (len(dataset_path_hash_pairs), 1, 4096)


def test_signatures_shape(signatures, dataset_path_hash_pairs):
    assert set(signatures.keys()) == set(dataset_path_hash_pairs)

    signatures_array = np.array(list(signatures.values()))
    assert signatures_array.shape == (NUMBER_OF_TEST_VIDEOS, 500)


@pytest.mark.usefixtures("signatures")
def test_saved_signatures(reprs, dataset_path_hash_pairs):
    signatures = bulk_read(reprs.signature)
    assert set(signatures.keys()) == set(dataset_path_hash_pairs)

    signatures_array = np.array(list(signatures.values()))
    assert signatures_array.shape == (NUMBER_OF_TEST_VIDEOS, 500)
