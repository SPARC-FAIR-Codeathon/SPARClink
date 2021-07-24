# sparc-portal-demo

This demo page is built using VueJS and Tailwind CSS. It has been developed to mimic the SPARC portal found at sparc.science. In order to get this project running please run the following commands: 

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
#### Deploy to Firebase
If you would like to push your own fork/clone of this repository to Firebase as a hosting provider, use the following instructions. You must already have a google email account and a project set up in your Firebase console. Please also remove any existing .firebaserc files. You don't need to edit your firebase.json file since it refers to the public files required for the host process.
``` bash
npm install -d firebase-tools

// login to firebase
firebase login

// initialize the firebase repo
firebase init

npm run deploy
```



### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
