import {Component, OnInit} from '@angular/core';
import { ApiService } from './api.service';

/** @title Simple form field */
@Component({
  selector: 'form-field-overview-example',
  templateUrl: 'form-field-overview-example.html',
  styleUrls: ['form-field-overview-example.css'],
})
export class FormFieldOverviewExample implements OnInit {
    public scholars = [];
    public scholarsInput = [];

  addScholar(newScholar: string) {
    if (newScholar) {
      this.scholarsInput.push(newScholar);
    }

    this.scholars.forEach(element => {
      debugger;
      console.log(newScholar+ " is equal to " + element.full_name)
      if(newScholar == element.full_name){
        alert(newScholar+ " is equal to " + element.full_name);
        //use element.id and look into publication-cites to find all the scholars that have cited them
        //then check with the authors that cited element.id and see if element.id has cited
      }
    });
  }

  deleteScholar(deleteScholar: string) {
    for (var i = 0; i < this.scholarsInput.length; i++) {
      if(this.scholarsInput[i] === deleteScholar){
        this.scholarsInput.splice(i,1);
      }
    }
  }


  title = 'ScholarScraperFE';
  

 constructor(private _apiservice: ApiService){}
  ngOnInit(){
    this._apiservice.getScholars().subscribe(data => this.scholars = data);
    // JSON.stringify(this.scholars.toString);

  }
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