import matplotlib.pyplot as plt
import numpy as np
import cv2
from improutils import *
import ipywidgets as widgets


def create_slider(min, max, default, description,slider_type= 'int'):
    description = description.ljust(30, '\xa0')
    if slider_type == 'float':
        return widgets.FloatSlider( min=min, max=max, step=0.01,value=default, 
                                   description=description, 
                                   continuous_update=False, 
                                   orientation='horizontal',
                                   style=dict(description_width='initial'),
                                   layout=widgets.Layout(width='auto'),
                                  )
    elif slider_type == 'int':
        return widgets.IntSlider( min=min, max=max, step=1,value=default, 
                                   description=description, 
                                   continuous_update=False, 
                                   orientation='horizontal',
                                   style=dict(description_width='initial'),
                                   layout=widgets.Layout(width='auto'),
                                  )
    elif slider_type == 'float_log':
        return widgets.FloatLogSlider( min=min, max=max, base = 5, step=0.01,value=default, 
                            description=description, 
                            continuous_update=False, 
                            orientation='horizontal',
                            style=dict(description_width='initial'),
                            layout=widgets.Layout(width='auto'),
                            )