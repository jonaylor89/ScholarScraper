import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {FormFieldOverviewExample} from './form-field-overview-example';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    FormFieldOverviewExample
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [FormFieldOverviewExample]
})
export class AppModule { }
