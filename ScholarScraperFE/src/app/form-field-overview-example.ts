import {Component} from '@angular/core';

/** @title Simple form field */
@Component({
  selector: 'form-field-overview-example',
  templateUrl: 'form-field-overview-example.html',
  styleUrls: ['form-field-overview-example.css'],
})
export class FormFieldOverviewExample {
    scholars = [];
  addScholar(newScholar: string) {
    if (newScholar) {
      this.scholars.push(newScholar);
    }

    var json = [   
      {
      "scholarID": "Alberto Cano",
      "scholarIDFK": "Dr. Seuss",
      "Date": "2012/04/23"
      },
      {
          "scholarID": "Alberto Cano",
          "scholarIDFK": "Dr. Seuss",
          "Date": "2013/04/23"
      },
      {
          "scholarID": "Alberto Cano",
          "scholarIDFK": "Dr. Seuss",
          "Date": "2013/04/23"
      },
      {
          "scholarID": "Dr. Seuss",
          "scholarIDFK": "Alberto Cano",
          "Date": "2016/04/23"
      }
  ]
  // var obj = JSON.parse(json);
  }

  deleteScholar(deleteScholar: string) {
    for (var i = 0; i < this.scholars.length; i++) {
      if(this.scholars[i] === deleteScholar){
        this.scholars.splice(i,1);
      }
    }
  }
  title = 'ScholarScraperFE';
}


/**  Copyright 2019 Google Inc. All Rights Reserved.
    Use of this source code is governed by an MIT-style license that
    can be found in the LICENSE file at http://angular.io/license */


// import { Component, OnInit } from '@angular/core';

// @Component({
//   selector: 'app-root',
//   templateUrl: './app.component.html',
//   styleUrls: ['./app.component.css'],
// })
// export class AppComponent {
//   scholars = [];
//   addScholar(newScholar: string) {
//     if (newScholar) {
//       this.scholars.push(newScholar);
//     }
//   }

//   deleteScholar(deleteScholar: string) {
//     for (var i = 0; i < this.scholars.length; i++) {
//       if(this.scholars[i] === deleteScholar){
//         this.scholars.splice(i,1);
//       }
//     }
//   }
//   title = 'ScholarScraperFE';
// }