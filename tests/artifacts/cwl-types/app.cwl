cwlVersion: v1.2
class: CommandLineTool
id: main
label: "Echo OGC BBox"
baseCommand: echo

requirements:
  InlineJavascriptRequirement: {}
  SchemaDefRequirement:
    types:
    - $import: https://raw.githubusercontent.com/eoap/schemas/main/geojson.yaml

inputs:
  aoi:
    type: https://raw.githubusercontent.com/eoap/schemas/main/geojson.yaml#FeatureCollection
    label: "Area of interest"
    doc: "Area of interest defined as a bounding box"
    loadContents: true
    inputBinding:
      valueFrom: |
        ${
          /* Validate the length of bbox to be either 4 or 6 */
          var aoi = JSON.parse(self.contents);
          var bboxLength = aoi.bbox.length;
          if (bboxLength !== 4 && bboxLength !== 6) {
            throw "Invalid bbox length: bbox must have either 4 or 6 elements.";
          }
          /* Convert bbox array to a space-separated string for echo */
          return aoi.bbox.join(' ') + " CRS: " + aoi.crs;
        }

outputs:
  echo_output:
    type: stdout
  persistent_output:
    type: File
  dir_output:
    label: Vegetation indexes
    doc: Vegetation indexes
    type:
      type: array
      items: Directory

stdout: echo_output.txt
