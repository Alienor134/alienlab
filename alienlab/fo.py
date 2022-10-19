from joblib import Parallel, delayed
import numpy as np
import skimage.util

class FramesOperator():
    def __init__(self, frames):
        self.frames = np.asarray(frames)
        self.frames_shape = self.frames.shape
        self.inds = np.asarray([*range(self.frames_shape[0])])
        self.selected_inds = [*range(self.frames_shape[0])]
        self.x = [0, self.frames_shape[1]]
        self.y = [0, self.frames_shape[2]]
    
    def crop(self):
        self.frames = self.frames[:, self.x[0]:self.x[1], self.y[0]: self.y[1]]

    def compute_stats(self):
        dict_stats = {'min' : np.min(self.frames, axis = (1,2)),
                      'max' : np.max(self.frames, axis = (1,2)),
                      'mean' : np.mean(self.frames, axis = (1,2)),
                      'std' : np.std(self.frames, axis = (1,2))
                     }
        self.global_stats = dict_stats
        
        dict_stats = {'min' : np.min(self.frames, axis = 0),
                      'max' : np.max(self.frames, axis = 0),
                      'mean' : np.mean(self.frames, axis = 0),
                      'std' : np.std(self.frames, axis = 0)
                     }
        self.frames_stats = dict_stats
    
    def normalize(self, min_target, max_target):
        min_val = np.min(self.global_stats['min'])
        max_val = np.max(self.global_stats['max'])
        self.frames = (self.frames - min_val) * max_target/(max_val - min_val) + min_target
        return self.frames

    def speed(self, task, kwargs):
        return np.asarray(Parallel(n_jobs=-1, max_nbytes=None)(delayed(task)(skimage.util.img_as_ubyte(self.frames[i]), **kwargs) 
                                              for i in self.selected_inds))    
    
    def apply(self, func, **kwargs):
        frames = self.speed(func, kwargs)
        return frames
    
    def select_frames(self, stats, threshold):
        selected_inds = np.where(stats > threshold)[0]
        self.selected_inds = selected_inds
        return selected_inds
    
    def combine(self, func, selected_inds):
        return func(self.frames[selected_inds])