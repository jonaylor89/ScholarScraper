import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Scholar} from './apiClass'
import {Publication} from './apiClass'
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  scholarsApi: string = 'http://localhost:8000/scholar';
  publicationApi: string  = 'http://localhost:8000/publication';
  publicationAuthorApi: string = 'http://localhost:8000/publication-author';
  publicationCitesApi: string = 'http://localhost:8000/publication-cites';
  totalCitationsApi: string = 'http://localhost:8000/total-citation';

  constructor(private httpClient: HttpClient) {}
  
  

  public getScholars(url?: string){
    return this.httpClient.get<Scholar[]>(`${this.scholarsApi}`);
  }

  public getPublication(url?: string){
    return this.httpClient.get<Publication[]>(`${this.publicationApi}`)
  }

  public getPublicationAuthor(url?: string){
    return this.httpClient.get<Publication[]>(`${this.publicationAuthorApi}`)
  }

  public getPublicationCites(url?: string){
    return this.httpClient.get<Publication[]>(`${this.publicationCitesApi}`)
  }

  public getTotalCitations(url?: string){
    return this.httpClient.get<Publication[]>(`${this.totalCitationsApi}`)
  }

  

  // public getScholarPublicationCites
}