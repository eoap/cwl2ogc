cwlVersion: v1.2
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.1.0
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  - class: Workflow
    id: water-bodies
    label: Water body detection based on NDWI and the otsu threshold
    doc: Water bodies detection based on NDWI and otsu threshold applied to Sentinel-2 or Landsat-9 staged acquisitions
    requirements:
      - class: ScatterFeatureRequirement
    inputs:
      aoi:
        label: area of interest
        doc: area of interest as a bounding box
        type: string
      epsg:
        label: EPSG code
        doc: EPSG code
        type: string
        default: "EPSG:4326"
      bands:
        label: bands used for the NDWI
        doc: bands used for the NDWI
        type: string[]
        default: ["green", "nir"]
      item:
        doc: Reference to a STAC item
        label: STAC item reference
        type: Directory
    outputs:
      - id: stac_catalog
        outputSource:
          - node_stac/stac_catalog
        type: Directory
    steps:
      node_crop:
        run: "#crop"
        in:
          item: item
          aoi: aoi
          epsg: epsg
          band: bands
        out:
          - cropped
        scatter: band
        scatterMethod: dotproduct
      node_normalized_difference:
        run: "#norm_diff"
        in:
          rasters:
            source: node_crop/cropped
        out:
          - ndwi
      node_otsu:
        run: "#otsu"
        in:
          raster:
            source: node_normalized_difference/ndwi
        out:
          - binary_mask_item
      node_stac:
        run: "#stac"
        in:
          item: item
          rasters:
            source: node_otsu/binary_mask_item
        out:
          - stac_catalog
  - class: CommandLineTool
    id: crop
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        coresMax: 1
        ramMax: 512
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/eoap/mastering-app-package/crop@sha256:a40bc27f475e9027524508839433bf2db3360278f8163f1d61140550bd97795d
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      item:
        type: Directory
        inputBinding:
          prefix: --input-item
      aoi:
        type: string
        inputBinding:
          prefix: --aoi
      epsg:
        type: string
        inputBinding:
          prefix: --epsg
      band:
        type: string
        inputBinding:
          prefix: --band
    outputs:
      cropped:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: norm_diff
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        coresMax: 1
        ramMax: 512
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/eoap/mastering-app-package/norm_diff@sha256:85588958311b20f6c257531fe087da8dee3d962fdb4a4a8a1b1d61915e0a74a9
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      rasters:
        type: File[]
        inputBinding:
          position: 1
    outputs:
      ndwi:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: otsu
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        coresMax: 1
        ramMax: 512
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/eoap/mastering-app-package/otsu@sha256:a390c8613df6da7617a28dd588a78b9f07f0be9d30a284eb98cc5467288309ef
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      raster:
        type: File
        inputBinding:
          position: 1
    outputs:
      binary_mask_item:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: stac
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        coresMax: 1
        ramMax: 512
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/eoap/mastering-app-package/stac@sha256:61d590777cf88ed890dbb0b8e24bc1163868ae8a6f335343060365c4182827a4
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      item:
        type: Directory
        inputBinding:
          prefix: --input-item
      rasters:
        type: File
        inputBinding:
          prefix: --water-body
    outputs:
      stac_catalog:
        outputBinding:
          glob: .
        type: Directory
s:codeRepository:
  URL: https://github.com/eoap/mastering-app-package.git
s:author:
  - class: s:Person
    s.name: Jane Doe
    s.email: jane.doe@acme.earth
    s.affiliation: ACME
