import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {FormFieldOverviewExample} from './form-field-overview-example';
import { HttpClientModule } from '@angular/common/http';
import {ApiService} from './api.service';

@NgModule({
  declarations: [
    FormFieldOverviewExample
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ApiService
  ],
  providers: [ApiService],
  bootstrap: [FormFieldOverviewExample]
})
export class AppModule { }
