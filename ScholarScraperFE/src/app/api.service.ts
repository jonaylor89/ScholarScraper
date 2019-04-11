import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL: string = 'localhost:8000/scholar';

  constructor(private httpClient: HttpClient) {

    
  }
  public getScholarById(scholarID: string){
    // return 
  }
}