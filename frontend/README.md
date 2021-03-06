# sparc-portal-demo

This demo page is built using [VueJS](https://vuejs.org/) and [Tailwind CSS](https://tailwindcss.com/). It has been developed to mimic the SPARC portal found at [sparc.science](https://sparc.science). In order to get this project running please refer to the [Project setup](https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/frontend/README.md#project-setup) section. 

## Project setup
``` bash
npm install
```

### Compiles and hot-reloads for development
``` bash 
npm run serve
```

### Compiles and minifies for production
``` bash
npm run build
```

### Lints and fixes files
``` bash
npm run lint
```
### Deploy to Firebase
If you would like to push your own fork/clone of this repository to Firebase as a hosting provider, use the following instructions. You must already have a google email account and a project set up in your Firebase console. Please also remove any existing `.firebaserc` files. You don't need to edit your `firebase.json` file since it refers to the public files required for the deployment process.
``` bash
npm install -D firebase-tools

// login to firebase
npx firebase login

// initialize the firebase repo
npx firebase init

npm run deploy
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Requesting data from the real-time database
SPARClink uses a Firebase real-time database as its intermediary data storage server. This allows for the backend citation extraction system to reside in a seperate server and allow the frontend to pull data asynchronously. If you prefer another data storage mechanism please add and modify the appropriate end point in the SPARClink component found in the `frontend/src/components/SparcLink/SparcLink.vue` file. The url endpoint for the GET request can be found in the `organizeData` function in the `methods` section. Our backend systems only allows authenticated users to write to the database so you will need to refer to the appropriate User ID when referencing the object.

## Adjusting the physics of the visualization
[d3.js](https://d3js.org/) provides extensive documentation on the physics that we implement on our visualizations. If you would like to modify how the graph behaves, the best place to start is at the force simulations in the `drawCanvas` function. d3.js also provides the option of rendering graphs in SVG elements but the limit of nodes that a simulation can accept, before there is a considerable performance drop, is low.
```javascript
this.simulation = d3
  .forceSimulation(nodes)
  .force(
    "link",
    d3.forceLink(links).id((d) => d.id)
  )
  .force("x", d3.forceX())
  .force("y", d3.forceY())
  .force("charge", d3.forceManyBody().strength(this.strength))
  .force("center", d3.forceCenter(WIDTH / 2, HEIGHT / 2));
```
You may define your own forces to act on the nodes or use d3's default forces. Please be aware that the canvas itself has a limit on the amount of nodes that can be drawn in its context before performance takes a hit. Within our own testing 8,000 to 10,000 nodes is the limit of acceptable performance. If your database is larger than this amount, please see if you can filter out any nodes that are present in the data.

## Adjusting the wordcloud
The [d3-cloud](https://github.com/jasondavies/d3-cloud) library is used to generate the visualizations. To modify the rendered image, edit the lines of code below. The data for the function is returned from the backend api found [here](https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/MLDataIndexingEngine/README.md#word-cloud).
```javascript
var layout = cloud()
  .size([300,300])
  .words(
    keywords.map(function (d, i) {
      return { text: d, size: 10 + values[i] * 90 };
    })
  )
  .padding(5)
  .rotate(0)
  .font("Asap, Verdana, Arial, Helvetica, sans-serif")
  .fontSize(function (d) {
    return d.size;
  })
  .on("end", draw);
```
