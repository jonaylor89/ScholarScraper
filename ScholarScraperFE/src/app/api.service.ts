import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Scholar} from './scholar'
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL: string = 'http://localhost:8000/scholar';
  scholarName = '';

  private mockURL: string ='./mockpublicatincites.json'

  constructor(private httpClient: HttpClient) {

    
  }
  public getScholarByName(scholarName: string){
    return this.scholarName;
  }
  

  public getScholars(url?: string){
    return this.httpClient.get<Scholar[]>(`${this.apiURL}`);
  }

  // public getScholarPublicationCites
}