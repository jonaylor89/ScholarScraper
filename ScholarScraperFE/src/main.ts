// import { enableProdMode } from '@angular/core';
// import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

// import { AppModule } from './app/app.module';
// import { environment } from './environments/environment';
// import { AppComponent} from './app/app.component'

// if (environment.production) {
//   enableProdMode();
// }

// platformBrowserDynamic().bootstrapModule(AppModule)
//   .catch(err => console.error(err));
import './polyfills';
import { Observable } from 'rxjs';
import {HttpClientModule} from '@angular/common/http';
import {NgModule} from '@angular/core';

import {BrowserModule} from '@angular/platform-browser';


// import {FormsModule, ReactiveFormsModule} from '@angular/forms';
// import {MatNativeDateModule} from '@angular/material';

// import {DemoMaterialModule} from './material-module';

import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {FormFieldOverviewExampleModule} from './app/form-field-overview-example.module'
// import {FormFieldOverviewExample} from './app/form-field-overview-example';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    // FormsModule,
    // DemoMaterialModule,
    // MatNativeDateModule,
    // ReactiveFormsModule,
    FormFieldOverviewExampleModule
    // FormFieldOverviewExample
  ],
  // entryComponents: [FormFieldOverviewExample],
  // declarations: [FormFieldOverviewExample],
  // bootstrap: [FormFieldOverviewExample],
  providers: []
})
export class AppModule {
  data: Observable<any>;
}

platformBrowserDynamic().bootstrapModule(FormFieldOverviewExampleModule);


/**  Copyright 2019 Google Inc. All Rights Reserved.
    Use of this source code is governed by an MIT-style license that
    can be found in the LICENSE file at http://angular.io/license */