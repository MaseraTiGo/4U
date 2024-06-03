# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : 4U
# @Time    : 2024/5/31 10:49
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
class Fuck:

    def __enter__(self):
        thread_global.__dict__.setdefault('depth', -1)
        calling_frame = inspect.currentframe().f_back
        if not self._is_internal_frame(calling_frame):
            calling_frame.f_trace = self.trace
            self.target_frames.add(calling_frame)

        stack = self.thread_local.__dict__.setdefault(
            'original_trace_functions', []
        )
        stack.append(sys.gettrace())
        self.start_times[calling_frame] = datetime_module.datetime.now()
        sys.settrace(self.trace)


    def __exit__(self, exc_type, exc_value, exc_traceback):
        if DISABLED:
            return
        stack = self.thread_local.original_trace_functions
        sys.settrace(stack.pop())
        calling_frame = inspect.currentframe().f_back
        self.target_frames.discard(calling_frame)
        self.frame_to_local_reprs.pop(calling_frame, None)

        ### Writing elapsed time: #############################################
        #                                                                     #
        _FOREGROUND_YELLOW = self._FOREGROUND_YELLOW
        _STYLE_DIM = self._STYLE_DIM
        _STYLE_NORMAL = self._STYLE_NORMAL
        _STYLE_RESET_ALL = self._STYLE_RESET_ALL

        start_time = self.start_times.pop(calling_frame)
        duration = datetime_module.datetime.now() - start_time
        elapsed_time_string = pycompat.timedelta_format(duration)
        indent = ' ' * 4 * (thread_global.depth + 1)
        self.write(
            '{indent}{_FOREGROUND_YELLOW}{_STYLE_DIM}'
            'Elapsed time: {_STYLE_NORMAL}{elapsed_time_string}'
            '{_STYLE_RESET_ALL}'.format(**locals())
        )
        #