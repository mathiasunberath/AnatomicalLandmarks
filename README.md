# AnatomicalLandmarks
Implementation of our MICCAI and invited IJCARS paper on detecting anatomical landmarks of the pelvis in X-ray images from arbitrary views.

## CT Data Annotation
Our training data is synthetically generated from full body CTs from the NIH Cancer Imaging Archive. In total, 20 CTs (male and female patients) were cropped to an ROI around the pelvis and 23 anatomical landmark positions were annotated manually in 3D. Landmarks were selected to be clinically meaningful and clearly identifiable in 3D; see Fig. 1 a). We release our annotation files under the folder '/annotation'. The name of the .fcsv file is in consistent with the CT data. 
## Projection Geometry
#### Offset Reading
*Dicom Offset* 
The CT volume offset is recorded in the dicom meta data. The dicom slices need to be sorted according to the tag (0020, 0013). Then the dicom offset can be read from tag (0020,0032) in the first slice after sorting.
*Origin Offset*
We calibrated the CT volume in our C-arm geometry by adding an origin offset. The calibrated origin data is uploaded in the text file 'origin.txt'.
*Projection Formula*
**Please use the following sudo code to manipulate the landmark offset.** The 3D annotation landmark point is noted as `landmark3D`. The above mentioned dicom offset is noted as `dicom_offset`; origin offset as `origin_offset`.
```
landmark3D[0] = -(landmark3D[0] + dicom_offset[0]) + origin_offset[0]
landmark3D[1] = -(landmark3D[1] + dicom_offset[1]) + origin_offset[1]
landmark3D[2] = landmark3D[2] - dicom_offset[2] + origin_offset[2] - 25
```
After this, we can then use the conventional pinhole camera projection model to project the 3D landmark onto 2D plane. We note the 3-by-4 projection matrix as `P`. The 3-by-1 projected result is saved at `proj`. The 2D landmark coordinate is saved at `landmark2D`.
```
proj = P * [landmark3D; 1] # Make it homogeneous coordinate
landmark2D[0] = proj[0]/proj[2]
landmark2D[1] = proj[1]/proj[2]
```
## Evaluation
## Reference
[1] Roth, H., Lu, L., Seff, A., Cherry, K.M., Hoffman, J., Wang, S., Summers, R.M.:
A new 2.5 d representation for lymph node detection in ct. The Cancer Imaging
Archive (2015)
