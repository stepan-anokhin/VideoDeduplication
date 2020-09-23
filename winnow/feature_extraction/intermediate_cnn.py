from .extraction_routine import start_video_extraction


class IntermediateCnnExtractor:

    def __init__(self, video_src, reprs, storepath, frame_sampling=1, save_frames=False):
        self.video_src = video_src
        self.reprs = reprs
        self.storepath = storepath
        self.frame_sampling = frame_sampling
        self.save_frames = save_frames

    def start(self, batch_size=8, cores=4):
        print('Starting feature extraction process from {}'.format(self.video_src))
        start_video_extraction(self.video_src,
                               self.reprs,
                               self.storepath,
                               batch_sz=batch_size,
                               cores=cores,
                               frame_sampling=self.frame_sampling,
                               save_frames=self.save_frames)
