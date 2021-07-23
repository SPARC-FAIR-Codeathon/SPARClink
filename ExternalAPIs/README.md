# External APIs

This folder contains the implementations for APIs to communicate with external resources.

## NIH_NCBI.py
API implementations to communicate with [NIH RePORTER](https://api.reporter.nih.gov/) and [NCBI](https://www.ncbi.nlm.nih.gov/home/develop/api/).

### NCBI API uses

#### getCitedBy (id_type, id)
- `id_type`: Type of the given `id`. 'pm_id' for PubMed articles or 'pmc_id' for PubMed Central articles. 
- `id`     : Identifier for the article.

Returns a dictionary of the articles that cite the given article, with doi as the key.
```
title       : Title of the paper
journal     : Name of the journal
year        : Publication year
author_list : Names of authors
doi         : DOI of the paper
pm_id       : PubMed id (if available)
pmc_id      : PubMed Central id of the paper
```

#### getPublicationsWithSearchTerm (search_term)
- `search_term`: Search term to look for in PubMed Central.

Returns a dictionary of the publications that matches the given search term, with the doi as the key. 
```
title       : Title of the paper
journal     : Name of the journal
year        : Publication year
author_list : Names of authors
doi         : DOI of the paper
pm_id       : PubMed id (if available)
pmc_id      : PubMed Central id of the paper
```
e.g. To find all the articles that mention the doi `10.26275/DUZ8-MQ3N`
``` python
getPublicationsWithSearchTerm('"10.26275/DUZ8-MQ3N"')
```
To find the article with the doi `10.26275/DUZ8-MQ3N`
``` python
getPublicationsWithSearchTerm('10.26275/DUZ8-MQ3N[doi]')
```

### NIH RePORTER API uses

#### generateRecord(getProjectFundingDetails (project_no)):
- `project_no`: Project number (also known as the award number) of NIH funding associated with Pennsieve datasets.

Returns a dictionary of the funding details of the grants, with the project number as the key. A project can have multiple grant applications (e.g. extensions, ammendments)
```
appl_id   : Application identifier
institute : Name of the organization that received funding
country   : Country of the organization
amount    : Amount received
year      : Fiscal year
keywords  : Keywords of the project topic.
```

#### getPublications (appl_id)
- `appl_id` : Application identifier of a grant.

Returns a dictionary of all the publications associated with the grant, with doi as the key.
```
title       : Paper title
journal     : Name of the journal
year        : Published year
author_list : Names of authors.
url         : URL to the paper
pm_id       : PubMed id of the paper
doi         : Paper DOI
```






