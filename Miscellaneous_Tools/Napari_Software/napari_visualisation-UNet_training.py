#!/usr/bin/env python
# coding: utf-8

# # NAPARI visualization of UNet Training Data
#
# You can use this notebook to view, modified and save out training data for UNet models
#
# Labels:
# + 0 - background
# + 1 - GFP/Phase
# + 2 - RFP
#
#
# Extra key bindings:
# + 'w' - calculate weightmap
# + 's' - save labels
# + 'o' - output all weightmaps and metadata for tfrecord creation
# + '\>' - grow the label under the mouse cursor
# + '\<' - shrink the label under the mouse cursor

# In[1]:


import os
import re
import enum
import json
import napari
from skimage import io
import numpy as np
from scipy import ndimage

from scipy.ndimage.morphology import distance_transform_edt
from scipy.ndimage import gaussian_filter


# In[2]:


@enum.unique
class Channels(enum.Enum):
    BRIGHTFIELD = 0
    GFP = 1
    RFP = 2
    IRFP = 3
    PHASE = 4
    WEIGHTS = 98
    MASK = 99


# ---
#
# ## Set up the data path and channel used

# In[3]:


# DATA_PATH = '/home/arl/Dropbox/Data/TrainingData/UNet_training_Ras'
# # DATA_PATH = '/home/arl/Dropbox/Data/TrainingData/UNet_training_Scribble'
# channels = [Channels.GFP, Channels.RFP]


DATA_PATH = '/Volumes/lowegrp/TrainingData/UNet_Training_Confluency/'
channels = [Channels.BRIGHTFIELD]

WEIGHT_AMPLITUDE = 10.


# ---

# ## Code
#

# In[4]:


def strip_modified_filename(filename):
    if filename.endswith('.modified.tif'):
        stripped_fn = filename[:-len('.modified.tif')]
        return stripped_fn
    return filename


def make_folder(foldername):
    if os.path.exists(foldername):
        return
    os.mkdir(foldername)


def file_root(filename):
    FILENAME_PATTERN = r'([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_*.tif'
    grps = re.search(FILENAME_PATTERN, filename)
    return grps


def load_training_data(pth, channels=[Channels.GFP, Channels.RFP]):
    """ load training data for visualisation with napari """

    all_channels = [Channels.MASK] + channels

    # find the sets and sort them
    sets = [f for f in os.listdir(pth) if os.path.isdir(os.path.join(pth, f))]
    sets.sort(key=lambda s: int(s[3:]))

    def set_filename_format(filename):
        grps = file_root(filename)
        if grps.group(1) in [c.name.lower() for c in all_channels]:
            FILENAME_FORMAT = 2
        else:
            FILENAME_FORMAT = 1

        def filename_formatter(filename, channel):
            assert (channel in [c.name.lower() for c in all_channels])
            grps = file_root(filename)

            return '{}_{}.tif'.format(*[grps.group(FILENAME_FORMAT), channel])
            # return '{}_{}.tif'.format(*[channel, grps.group(FILENAME_FORMAT)])

        return filename_formatter

    files = {k: {'files': [], 'data': [], 'sets': [], 'path': []} for k in all_channels}

    for s in sets:

        # root_folders
        l_root = os.path.join(pth, s, 'labels')

        # check that this folder exists
        if not os.path.exists(l_root):
            raise IOError('{} does not exist. Do you need to rename label -> labels?'.format(l_root))

        # get the training label files
        label_files = [f for f in os.listdir(l_root) if f.endswith('.tif')]

        # sort to remove unmodified files and replace with the modified files
        unmodified_files, modified_files = [], []
        for i, f in enumerate(label_files):
            if f.endswith('.modified.tif'):
                modified_files.append(strip_modified_filename(f))
            else:
                unmodified_files.append(f)

        unmodified_files = list(set(unmodified_files).difference(set(modified_files)))
        label_files = unmodified_files + [f + '.modified.tif' for f in modified_files]

        # print label_files
        fnfmt = set_filename_format(label_files[0])

        files[Channels.MASK]['path'] += [s + '/labels/' + f for f in label_files]
        files[Channels.MASK]['files'] += [strip_modified_filename(f) for f in label_files]
        files[Channels.MASK]['data'] += [io.imread(os.path.join(l_root, f)) for f in label_files]
        files[Channels.MASK]['sets'] += [s] * len(label_files)

        for channel in channels:
            cfiles = [fnfmt(l, channel.name.lower()) for l in label_files]
            files[channel]['path'] += [s + '/' + channel.name.lower() + '/' + f for f in cfiles]
            files[channel]['files'] += cfiles
            files[channel]['data'] += [io.imread(os.path.join(pth, s, channel.name.lower(), f)) for f in cfiles]
            files[channel]['sets'] += [s] * len(label_files)

    # now make image stacks
    for channel in files.keys():

        for i, im in enumerate(files[channel]['data']):
            print(channel, files[channel]['path'][i], im.shape, im.dtype)

        files[channel]['data'] = np.stack(files[channel]['data'], axis=0)

    return files


# In[5]:


data = load_training_data(DATA_PATH, channels)


# In[6]:


def normalize_images(stack):
    normed = stack.astype(np.float32)
    for i in range(stack.shape[0]):
        # normed[i,...] = (normed[i,...]-np.mean(normed[i,...])) / np.std(normed[i,...])
        c = normed[i, ...]
        p_lo = np.percentile(c, 5)
        p_hi = np.percentile(c, 99)
        normed[i, ...] = np.clip((c - p_lo) / p_hi, 0., 1.)
    return normed


# In[7]:


def bounding_boxes(seg):
    lbl, nlbl = ndimage.label(seg)
    class_label, _, minxy, maxxy = ndimage.extrema(seg, lbl, index=np.arange(1, nlbl + 1))
    return class_label, minxy, maxxy


# In[8]:


seg = np.zeros(data[channels[0]]['data'].shape, dtype=np.uint8)
mask = data[Channels.MASK]['data']
if mask.ndim == 3:
    seg = mask > 0
elif mask.ndim == 4:
    seg[mask[:, 0, ...] > 0] = 1
    seg[mask[:, 1, ...] > 0] = 2


# In[9]:


def convert_to_mask(labels, unique_labels=range(1, len(channels) + 1)):
    print(unique_labels)
    seg = np.zeros((len(unique_labels),) + labels.shape, dtype=np.uint8)
    for i, l in enumerate(unique_labels):
        seg[i, ...] = labels == l
    return np.squeeze(seg)


# In[10]:


def save_labels(viewer):
    # get the current image
    current_slice = viewer.layers[viewer.active_layer].coordinates[0]
    source_set = data[Channels.MASK]['sets'][current_slice]
    source_file = data[Channels.MASK]['files'][current_slice]
    source_fn = os.path.join(source_set, 'labels', source_file)

    # get the current layer
    current_labels = viewer.layers['labels'].data[current_slice, ...]
    current_mask = convert_to_mask(current_labels)

    # write out the modified segmentation mask
    new_file = os.path.join(DATA_PATH, source_fn + '.modified.tif')
    print(new_file)
    io.imsave(new_file, current_mask.astype('uint8'))

    print(current_slice, current_labels.shape, new_file)


# In[11]:


weightmaps = np.zeros((seg.shape), dtype=np.float32)


def calculate_weightmaps(viewer, weight=WEIGHT_AMPLITUDE, current_slice=0):
    # get the current layer and make it binary
    mask = viewer.layers['labels'].data[current_slice, ...].astype(np.bool)

    wmap = weight * (
                gaussian_filter(mask.astype(np.float32), sigma=5.) - gaussian_filter(mask.astype(np.float32), sigma=.1))

    # normalize it
    wmap += 1.
    wmap[mask] = 1.

    viewer.layers['weightmaps'].data[current_slice, ...] = wmap.astype(np.float32)
    viewer.layers['weightmaps'].contrast_limits = (np.min(wmap), np.max(wmap))
    viewer.layers['weightmaps'].visible = True

    return wmap


# In[12]:


def grow_shrink_label(viewer, grow=True):
    # get the current image
    current_slice = viewer.layers[viewer.active_layer].coordinates[0]
    current_labels = viewer.layers['labels'].data[current_slice, ...]

    cursor_coords = [int(p) for p in viewer.layers[viewer.active_layer].position]
    labelled, _ = ndimage.label(current_labels.astype(np.bool))
    real_label = current_labels[cursor_coords[0], cursor_coords[1]]

    if real_label < 1: return

    print(real_label)
    mask = labelled == labelled[cursor_coords[0], cursor_coords[1]]
    if grow:
        mask = ndimage.morphology.binary_dilation(mask, iterations=3)
    else:
        current_labels[mask] = 0
        mask = ndimage.morphology.binary_erosion(mask, iterations=3)

    current_labels[mask] = real_label
    viewer.layers['labels'].data[current_slice, ...] = current_labels
    viewer.layers['labels']._set_view_slice()


# In[ ]:


# start napari
with napari.gui_qt():
    viewer = napari.Viewer()

    if Channels.GFP in data:
        gfp = normalize_images(data[Channels.GFP]['data'])
        viewer.add_image(gfp, name='GFP', colormap='green', contrast_limits=(0., 1.))

    if Channels.RFP in data:
        rfp = normalize_images(data[Channels.RFP]['data'])
        viewer.add_image(rfp, name='RFP', colormap='magenta', contrast_limits=(0., 1.))
        viewer.layers['RFP'].blending = 'additive'

    if Channels.PHASE in data:
        phase = normalize_images(data[Channels.PHASE]['data'])
        viewer.add_image(phase, name='Phase', colormap='gray')

    if Channels.BRIGHTFIELD in data:
        bf = normalize_images(data[Channels.BRIGHTFIELD]['data'])
        viewer.add_image(bf, name='Brightfield', colormap='gray')

    viewer.add_image(weightmaps, name='weightmaps', colormap='plasma', visible=False)
    viewer.add_labels(seg, name='labels')

    viewer.layers['labels'].opacity = 0.4
    viewer.layers['weightmaps'].blending = 'additive'


    @viewer.bind_key('s')
    def k_save_labels(viewer):
        save_labels(viewer)


    @viewer.bind_key('w')
    def k_calculate_weightmaps(viewer):
        current_slice = viewer.layers[viewer.active_layer].coordinates[0]
        calculate_weightmaps(viewer, current_slice=current_slice)


    @viewer.bind_key('<')
    def k_shrink_label(viewer):
        print('shrink label')
        grow_shrink_label(viewer, grow=False)


    @viewer.bind_key('>')
    def k_grow_label(viewer):
        print('grow label')
        grow_shrink_label(viewer, grow=True)


    @viewer.bind_key('o')
    def k_output(viewer):
        print('output all with metadata')

        data[Channels.WEIGHTS] = {'files': [], 'sets': [], 'path': []}

        for i in range(viewer.layers['weightmaps'].data.shape[0]):
            wmap = calculate_weightmaps(viewer, current_slice=i)

            source_set = data[Channels.MASK]['sets'][i]
            source_file = data[Channels.MASK]['files'][i]

            fn = file_root(source_file).group(1)

            weight_folder = os.path.join(DATA_PATH, source_set, 'weights')
            make_folder(weight_folder)

            weight_fn = '{}_weights.tif'.format(fn)
            io.imsave(os.path.join(weight_folder, weight_fn), wmap.astype(np.float32))

            data[Channels.WEIGHTS]['files'].append(weight_fn)
            data[Channels.WEIGHTS]['sets'].append(source_set)
            data[Channels.WEIGHTS]['path'].append('{}/weights/{}'.format(source_set, weight_fn))

        # write out a JSON file with the data
        jfn = os.path.join(DATA_PATH, 'training_metadata.json')
        jdata = {}
        for channel in data.keys():
            jdata[channel.name.lower()] = data[channel]['path']

        with open(jfn, 'w') as json_file:
            json.dump(jdata, json_file, indent=2, separators=(',', ': '))

# In[ ]:


# In[ ]:


# # convert segmentation output labels to multichannel stacks

# p = '/Users/arl/Dropbox/Data/TrainingData/set12'
# files = [f for f in os.listdir(os.path.join(p,'labels')) if f.endswith('.tif')]
# for f in files:
#     mask = io.imread(os.path.join(p, 'labels', f))
#     print(mask.shape)
#     gfp = mask==1
#     rfp = mask==2
#     new_mask = np.stack([gfp, rfp], axis=0)
#     io.imsave(os.path.join(p,f), new_mask.astype('uint8'))


# In[ ]:




