# metadata_extraction.py

This module contains API implementations to communicate with SPARC Pennsieve and https://www.protocols.io/workspaces/sparc.

## get_list_of_datasets_with_metadata([])

Return all the dataset from SPARC Pennsieve. Return object:
``` python
[..., {
    'datasetId': 64, 
    'version': 4, 
    'name': 'Quantified Morphology of the Pig Vagus Nerve'
    'model': 'award', 
    "description": "This dataset contains recordings of compound nerve action potentials from the pelvic nerve as well as the pudendal nerves and its branches in response to electrical stimulation on the epidural surface of the sacral spinal cord in anesthetized cats.",
    'properties': {
        'description': 'Experiments to map physiological functions of autonomic nerves and the continued advance of bioelectronictherapies are limited by inadequate activation or block of targeted nerve fibers and unwanted co-activation orblock of non-targeted nerve fibers. More fundamentally, the relationship between applied stimuli and the nervefibers that are activated or blocked, how this relationship varies across individuals and species, and how theserelationships can be controlled remain largely unknown. We will develop, implement and validate an efficientcomputational pipeline for simulation of electrical activation and block of different nerve fiber types withinautonomic nerves. The pipeline will include segmentation of microanatomy from fixed nerve samples, three-dimensional finite-element models of electrodes positioned on nerves, and non-linear cable models of differentnerve fiber types, enabling calculation of quantitative input-output maps of activation and block of specific nervefibers. As key benchmarks of pipeline development and for the proposed analysis and design efforts, we willimplement models of the cervical (VNc) and abdominal (VNa) vagus nerves in rat, in a SPARC-identified animalmodel, and in human. The VNc is an excellent test bed as it contains a broad spectrum of nerve fiber types,there are experimental data to facilitate model validation, and there are multiple applications of VNc stimulationwhere a lack of fiber selectivity limits the therapeutic window. The VNa is an excellent complement to the cervicalVNc, as a prototypical autonomic nerve of a size comparable to many of the small autonomic nerves targetedby SPARC projects. We will use the models that emerge from the pipeline to achieve analysis and design goalsto address critical gaps identified as SPARC priorities. Specifically, we will quantify of the effects of intra-speciesdifferences in nerve morphology on activation and block by building individual sample-specific models for eachnerve and specie. These models will also be used to quantify inter-species differences in nerve fiber activationand block and to identify electrode designs and stimulation parameters that produce equivalent degrees ofactivation and block across species. We will combine the resulting models with engineering optimization todesign approaches to increase the selectivity and efficiency of activation and block of different nerve fiber types.The outcomes will be a pipeline for modeling autonomic nerves, electrode geometries, and stimulationparameters, as well as tools that address the limitations of nerve stimulation selectivity and efficiency that hinderthe continued advance of physiological mapping studies and the development of bioelectronic therapies.', 
        'id': 'db090035-8a57-4474-8c3d-2536dee9499f', 
        'principal_investigator': 'GRILL, WARREN M.', 
        'title': 'MODELING ACTIVATION AND BLOCK OF AUTONOMIC NERVES FOR ANALYSIS AND DESIGN', 
        'award_id': 'OT2OD025340'}, 
    'versionPublishedAt': '2020-10-01T15:41:57.651749Z', 
    'datasetDOI': 'https://dx.doi.org/10.26275/maq2-eii4', 
    'tags': [
        'vagus nerve stimulation', 
        'neural anatomy', 
        'vagus nerve morphology', 
        'autonomic nervous system'], 
    'contributors': [
        {'firstName': 'Nicole', 'middleInitial': 'A', 'lastName': 'Pelot', 'degree': 'Ph.D.', 'orcid': '0000-0003-2844-0190'}, 
        {'firstName': 'Gabriel', 'middleInitial': 'B', 'lastName': 'Goldhagen', 'degree': None, 'orcid': None}, 
        {'firstName': 'Jake', 'middleInitial': 'E', 'lastName': 'Cariello', 'degree': None, 'orcid': None}, 
        {'firstName': 'Warren', 'middleInitial': 'M', 'lastName': 'Grill', 'degree': 'Ph.D.', 'orcid': '0000-0001-5240-6588'}], 
    'originatingArticleDOI': [], 
    'protocolsDOI': ['dx.doi.org/10.17504/protocols.io.6bvhan6']}, ...]
```

## parsing_protocols(authorization_key)
- `authorization_key` : API key obtained from protocols.io

Returns all the protocols in the SPARC workspace. Return object:
``` Python
[...{
  "authors" : [ {
    "affiliation" : "UCLA",
    "blocked_by_you" : false,
    "blocked_you" : false,
    "hide_following" : false,
    "image" : {
      "placeholder" : "/img/avatars/011.png",
      "source" : "/img/avatars/011.png",
      "webp_source" : ""
    },
    "is_verified_user" : false,
    "name" : "Pradeep  Rajendran",
    "username" : "pradeep-rajendran",
    "verified" : 0
  }, {
    "affiliation" : "UCLA",
    "blocked_by_you" : false,
    "blocked_you" : false,
    "hide_following" : false,
    "image" : {
      "placeholder" : "",
      "source" : "",
      "webp_source" : ""
    },
    "is_verified_user" : false,
    "name" : "John Tompkins",
    "username" : "",
    "verified" : 0
  }, {
    "affiliation" : "UCLA",
    "blocked_by_you" : false,
    "blocked_you" : false,
    "hide_following" : false,
    "image" : {
      "placeholder" : "",
      "source" : "",
      "webp_source" : ""
    },
    "is_verified_user" : false,
    "name" : "Kalyanam Shivkumar",
    "username" : "",
    "verified" : 0
  } ],
  "doi" : "10.17504/protocols.io.2n9gdh6",
  "title" : "Pig- Heart Neuonal and Fiber Immunocytochemistry",
  "url" : "https://www.protocols.io/view/pig-heart-neuonal-and-fiber-immunocytochemistry-2n9gdh6"
}...]
```


