import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {FormFieldOverviewExample} from './form-field-overview-example';
import { HttpClientModule } from '@angular/common/http';
import {ApiService} from './api.service';


import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatNativeDateModule} from '@angular/material';

import {DemoMaterialModule} from './material-module';
@NgModule({
  
  imports: [
    BrowserModule,
    HttpClientModule,

    FormsModule,
    DemoMaterialModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    // FormFieldOverviewExample
    // ApiService
  ],
  declarations: [FormFieldOverviewExample],
  providers: [ApiService],
  // entryComponents: [FormFieldOverviewExample],
  // declarations: [FormFieldOverviewExample],
  bootstrap: [FormFieldOverviewExample]
})
export class FormFieldOverviewExampleModule { }
