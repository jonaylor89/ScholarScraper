import {Component, OnInit} from '@angular/core';
import { ApiService } from './api.service';         
import { Breakpoints } from '@angular/cdk/layout';

//TODO
//Save and display the saved data (Display if user entered Dr Zeus and Alberto Cano)
//Display deleted data
//Show count
//Show data
//Display it using some Javascript library
//Prevent User from adding/deleting the same scholar twice 
//figure out how to save previous data so this process doesn't take long (after finding all citating store that author citations)


/** @title Simple form field */
@Component({
  selector: 'form-field-overview-example',
  templateUrl: 'form-field-overview-example.html',
  styleUrls: ['form-field-overview-example.css'],
})
export class FormFieldOverviewExample implements OnInit {
    public scholars = [];
    public scholarsInput = [];

    //input of user
    public mockScholarsInput= ["Alberto Cano"];
    
    //database to map user input to an id
    public mockScholars = [
      {full_name:"Alberto Cano",id:"8f_w4HQAAAAJ"},
      {full_name:"Dr Seuss",id:"1234567890"},
      {full_name:"Dr Zeus",id:"123"}
    ];

    //database to map scholarID to PublicationID
    public mockPublicationAuthor = [
      {scholarID:"8f_w4HQAAAAJ", publicationID: "1"},
      {scholarID:"8f_w4HQAAAAJ", publicationID: "2"},
      {scholarID:"8f_w4HQAAAAJ", publicationID: "3"},
      {scholarID:"1234567890", publicationID: "4"},
      {scholarID:"1234567890", publicationID: "5"},
      {scholarID:"1234567890", publicationID: "6"},
      {scholarID:"123", publicationID: "7"}
    ];
    
    //database that displays publications that cite each other
    public mockPublicationCites = [
        {publicationID:"1", publicationIDFK:'5'},
        {publicationID:"1", publicationIDFK:'4'},
        {publicationID:"6", publicationIDFK:'1'},
        {publicationID:"5", publicationIDFK:'2'},
        {publicationID:"6", publicationIDFK:'7'},
        {publicationID:"7", publicationIDFK:'6'}
        
        // {publicationID:"1", publicationIDFK:'5'},
        // {publicationID:"1", publicationIDFK:'5'},
        // {publicationID:"1", publicationIDFK:'5'},
        

    ]


  //   public mockPublicationCites = [   
  //     {scholarID: "8f_w4HQAAAAJ", scholarIDFK: "1234567890", Date: "2012/04/23"},
  //     {scholarID: "8f_w4HQAAAAJ", scholarIDFK: "1234567890", Date: "2013/04/23"},
  //     {scholarID: "8f_w4HQAAAAJ", scholarIDFK: "1234567890", Date: "2013/04/23"},
  //     {scholarID: "1234567890", scholarIDFK: "8f_w4HQAAAAJ", Date: "2016/04/23"}
      
  // ];

  public mockStackOfOriginalAuthorsPublication; //maybe turn into an object that contains scholarID and publication id, publicationID
  public mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication; //publications that cited the original scholars publication, publicationID
  public mockScholarsCitingEachOther; //scholarID1 : scholarID2
  public mockScholarsCitingEachOtherNames= [] ; //their actual names scholar: , citedby: 
  public mockStorePublicationsCitedByOriginalAuthor;
  public mockStackOfScholarsCitingOriginalAuthorsPublication ;
  public mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor ;
  public citationCount = [];
  
  
  addScholar(newScholar: string) {
    // if (newScholar) {
    //   this.scholarsInput.push(newScholar);
    //   console.log(this.scholars.toString);
    // }
    // this.scholars.forEach(element => {
    //   console.log(newScholar+ " is equal to " + element.full_name)
      
    //   if(newScholar == element.full_name){
    //     alert(newScholar+ " is equal to " + element.full_name);
    //     //use element.id and look into publication-cites to find all the scholars that have cited them
    //     //then check with the authors that cited element.id and see if element.id has cited
    //   }
    // }); //uncomment once you use an api
    this.mockStackOfOriginalAuthorsPublication = []; //maybe turn into an object that contains scholarID and publication id, publicationID
    this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication = []; //publications that cited the original scholars publication, publicationID
    this.mockScholarsCitingEachOther = []; //scholarID1 : scholarID2
    // this.mockScholarsCitingEachOtherNames = []; //their actual names scholar: , citedby: 
    this.mockStorePublicationsCitedByOriginalAuthor = [];
    this.mockStackOfScholarsCitingOriginalAuthorsPublication = [];
    this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor = [];


    this.scholarsInput.push(newScholar); //keep track of the current scholars we want to know about
    // let mockScholarID = '';
    // // let name = this.mockScholars[0].full_name
    // for(let i = 0; i < this.mockScholars.length; i++){
    //   if(newScholar ==  this.mockScholars[i].full_name) {
    //     console.log(newScholar+ " is equal to " + this.mockScholars[i].full_name)
    //     mockScholarID =  this.mockScholars[i].id;
    //   }
    // }
    
    // //we found a scholar that maps to the scholar database
    
    // if(mockScholarID != ''){
    //     //cycle through all their publications and store them
    //     for(let i = 0; i < this.mockPublicationAuthor.length; i++){
    //       if(mockScholarID == this.mockPublicationAuthor[i].scholarID){
    //         this.mockStackOfOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].publicationID); //maybe make it a hashmap all publications of specific author

    //       }
    //     }
    // }
    

    // //cycle through publications that have cited the authors publication using mockPublicationCites
    // //loop through mockStackOfScholarsPublication, loop through publication cites 
    
    // if(this.mockStackOfOriginalAuthorsPublication.length > 0){
    //      //loop through all the publications in publicationcites. then store the publications that have cited
    //      //the original authors publication
    //      //side note: check how to see contains
    //   for(let i = 0; i < this.mockPublicationCites.length; i++){
    //     for(let j = 0; j < this.mockStackOfOriginalAuthorsPublication.length; j++){
    //       if(this.mockStackOfOriginalAuthorsPublication[j] == this.mockPublicationCites[i].publicationID){ //find a more efficient way to do this
    //             this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.push(this.mockPublicationCites[i].publicationIDFK) //this will contains publications that cited original scholars publication
    //       }
    //     }
    //   }
    // }
    // // debugger; //display publication 5 (publication that cited the original author)
    // //but first loop through authors publication 5 and find all the authors of publication 5, 
    // //once finding all the others of publication five  loop through those authors and find all of their publications to add
    // //onto the stack

    // //*DO A LOOP FOR EACH AUTHOR AND CHECK TO SEE IF THAT AUTHOR HAS BEEN CITED BY ORIGINAL AUTHOR

    // if(this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length > 0){ 
    //   for(let i = 0; i < this.mockPublicationAuthor.length; i++){
    //     for(let j = 0; j < this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length; j++){
    //       if(this.mockPublicationAuthor[i].publicationID == this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication[j]){
    //         this.mockStackOfScholarsCitingOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].scholarID);
    //         //*now for each author do a loop determining if that authors publication has been cited by original author
    //       }
    //     }
    //   }
    // }
    // // debugger; //1234567890
    // //loop through this.mockStackOfScholarsCitingOriginalAuthorsPublication, find all of their publications
    // //and store them
    // // debugger;
    // if(this.mockStackOfScholarsCitingOriginalAuthorsPublication.length > 0){
    //   for(let i = 0; i < this.mockPublicationAuthor.length; i++){
    //     for(let j = 0; j < this.mockStackOfScholarsCitingOriginalAuthorsPublication.length; j++){
    //       if(this.mockPublicationAuthor[i].scholarID == this.mockStackOfScholarsCitingOriginalAuthorsPublication[j]){
    //         this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.push(this.mockPublicationAuthor[i].publicationID);
    //       }
    //       //store the scholars publications
          
    //     }
    //   }
    // }
    // // debugger;
    // //loop through the stack of publications that have cited the original scholars publications
    // //check to see if these publications have been cited by the original scholars from the (this.mockStackOfScholarsPublication)
    // // same this.mockPublicationCites database
    
    // if(this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length > 0){

    //   for(let i = 0; i < this.mockPublicationCites.length; i++){
    //     for(let j = 0; j < this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length; j++){ 
        
    //       if (this.mockPublicationCites[i].publicationID == this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor[j]){ //if a publicationID is the same as the publicationID that cited the original scholars publication
    //           //check to see if the on the cited section it contains the original scholars publication 

    //             if(this.mockStackOfOriginalAuthorsPublication.indexOf(this.mockPublicationCites[i].publicationIDFK) > -1){ //if the orignal scholars publication is citing the publication of authors that had cited the original author
    //             //store the element.publicationID (which is the publicationID of publications that had cited the original scholars publication)
    //             //store all the publications  of scholars that have cited the original author that is cited by original othercited by the original  
    //             this.mockStorePublicationsCitedByOriginalAuthor.push(this.mockPublicationCites[i].publicationID); 
    //             }
    //       }
    //   }

    //   }
    // }
    // //debugger; // this.mockStorePublicationsCitedByOriginalAuthor = 5
    // //double check with john and cano about what this database actually contains 
    // // (what if authors who are cited by original authors are not on the mockPublicationAuthorDatabase)

     
    // if(this.mockStorePublicationsCitedByOriginalAuthor.length > -1){
    //    //loop through mockPublicationAuthor Database
    //    for(let i = 0; i < this.mockPublicationAuthor.length; i++){
    //      for(let j = 0; j < this.mockStorePublicationsCitedByOriginalAuthor.length; j++){
    //       //  debugger;
    //        if(this.mockPublicationAuthor[i].publicationID == this.mockStorePublicationsCitedByOriginalAuthor[j]){
    //          //check to see if author of that publication is in this.mockStackOfScholarsCitingOriginalAuthorsPublication.
    //          //which ensures that we are only including authors that are cited by original author
    //          if(this.mockStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.mockPublicationAuthor[i].scholarID ) > -1){
    //           let newObj = {scholarID1: mockScholarID, scholarID2: this.mockPublicationAuthor[i].scholarID}
    //           this.mockScholarsCitingEachOther.push(newObj);
    //          }
    //        }
    //      }
    //    }
    //   }

    // // debugger;
    // //logic for when user enters another name, and that name of the previous scholar includes that new name under
    // //mock scholars citing each other, then don't repeat it, this should also be where we keep count of which scholar is citing who
    // let newObj = []
    // if(this.mockScholarsCitingEachOther.length > 0){ //unecessary delete later
    //   for(let i = 0; i <this.mockScholars.length; i++){
    //     for(let j = 0; j < this.mockScholarsCitingEachOther.length; j++){
          
    //       if(this.mockScholars[i].id == this.mockScholarsCitingEachOther[j].scholarID2){
  
    //             newObj.push({full_name: newScholar, scholarID2: this.mockScholars[i].full_name})
    //           // if(this.mockScholarsCitingEachOtherNames.length > 0 ){
    //           //   if(this.mockScholars[i].full_name != this.mockScholarsCitingEachOtherNames[j].full_name
    //           //     && newScholar != this.mockScholarsCitingEachOtherNames[j].scholarID2) {
    //           //   this.mockScholarsCitingEachOtherNames.push(newObj);
    //           // }
    //         // }
            
    //       }
          
    //     }
    //   }
    // }
    //   //now loop through all the new obj found and make sure that we are not adding repeated information
    //   // debugger;
    //   //just loop through citingEachOthersName if newObj[i] == it then increment i and start citing each others name at 0
    //   if(this.mockScholarsCitingEachOtherNames.length > 0 ){
    //   let i = 0
    //   let savedIndex= [];
    //   for(let i = 0; i < newObj.length; i++){
    //   for(let j = 0; j < this.mockScholarsCitingEachOtherNames.length; j++){
       
        
    //     if((newObj[i].full_name == this.mockScholarsCitingEachOtherNames[j].scholarID2
    //          && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNames[j].full_name)) {
    //           newObj.splice(i,1); 
    //         i = 0;
    //          }
        
    //     if(newObj[i].full_name == this.mockScholarsCitingEachOtherNames[j].full_name
    //           && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNames[j].scholarID2) {    
    //         newObj.splice(i,1);
    //         i = 0;
    //     }
    //   }
        
    //   } 
    //   for(let i = 0; i < newObj.length; i++){
    //     this.mockScholarsCitingEachOtherNames.push(newObj[i]);
    //   }
    // }
    // else {
    //   for(let i = 0; i < newObj.length; i++){
    //   this.mockScholarsCitingEachOtherNames.push({full_name: newObj[i].full_name, scholarID2: newObj[i].scholarID2});
    //   }
      
    // }
    
  }

  
//delete scholars from this.mockScholarsCitingEachOtherNames if full_name == scholar trying to delete
//and make sure that the scholar in scholarID2 does not exist in the scholar input
  deleteScholar(deleteScholar: string) {
    //loop through this.mockScholarsCitingEachOtherNames
    // if(this.scholarsInput.indexOf(deleteScholar)>-1){
    //   for(let i = 0; i < this.mockScholarsCitingEachOtherNames.length; i++){
    //     if(this.mockScholarsCitingEachOtherNames[i].full_name == deleteScholar){
    //       if(!(this.scholarsInput.indexOf(this.mockScholarsCitingEachOtherNames[i].scholarID2)>-1)){
    //         this.mockScholarsCitingEachOtherNames.splice(i,1);
    //       }
    //     }
    //   }
    // }
    
    
    for (let i = 0; i < this.scholarsInput.length; i++) {
      if(this.scholarsInput[i] == deleteScholar){
        this.scholarsInput.splice(i,1);
      }
    }

  }

  submitResults(){

    // this.mockStackOfOriginalAuthorsPublication = []; //maybe turn into an object that contains scholarID and publication id, publicationID
    // this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication = []; //publications that cited the original scholars publication, publicationID
    // this.mockScholarsCitingEachOther = []; //scholarID1 : scholarID2
    this.mockScholarsCitingEachOtherNames = []; //their actual names scholar: , citedby: 
    // this.mockStorePublicationsCitedByOriginalAuthor = [];
    // this.mockStackOfScholarsCitingOriginalAuthorsPublication = [];
    // this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor = [];
    for(let m= 0; m < this.scholarsInput.length;m++){
      this.mockStackOfOriginalAuthorsPublication = []; //maybe turn into an object that contains scholarID and publication id, publicationID
      this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication = []; //publications that cited the original scholars publication, publicationID
      this.mockStackOfScholarsCitingOriginalAuthorsPublication = [];
      this.mockStorePublicationsCitedByOriginalAuthor = [];
      this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor = [];
      // this.mockScholarsCitingEachOtherNames = []; //their actual names scholar: , citedby: 
      this.mockScholarsCitingEachOther = []; //scholarID1 : scholarID2
    let mockScholarID = '';
    // let name = this.mockScholars[0].full_name
    for(let i = 0; i < this.mockScholars.length; i++){
      if(this.scholarsInput[m] ==  this.mockScholars[i].full_name) {
        console.log(this.scholarsInput[m]+ " is equal to " + this.mockScholars[i].full_name)
        mockScholarID =  this.mockScholars[i].id;
      }
    }
    
    //we found a scholar that maps to the scholar database
    if(mockScholarID != ''){
        //cycle through all their publications and store them
        for(let i = 0; i < this.mockPublicationAuthor.length; i++){
          if(mockScholarID == this.mockPublicationAuthor[i].scholarID){
            this.mockStackOfOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].publicationID); //maybe make it a hashmap all publications of specific author

          }
        }
    }
    

    //cycle through publications that have cited the authors publication using mockPublicationCites
    //loop through mockStackOfScholarsPublication, loop through publication cites 
    
    if(this.mockStackOfOriginalAuthorsPublication.length > 0){
         //loop through all the publications in publicationcites. then store the publications that have cited
         //the original authors publication
         //side note: check how to see contains
      for(let i = 0; i < this.mockPublicationCites.length; i++){
        for(let j = 0; j < this.mockStackOfOriginalAuthorsPublication.length; j++){
          if(this.mockStackOfOriginalAuthorsPublication[j] == this.mockPublicationCites[i].publicationID){ //find a more efficient way to do this
                this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.push(this.mockPublicationCites[i].publicationIDFK) //this will contains publications that cited original scholars publication
          }
        }
      }
    }
    // debugger; //display publication 5 (publication that cited the original author)
    //but first loop through authors publication 5 and find all the authors of publication 5, 
    //once finding all the others of publication five  loop through those authors and find all of their publications to add
    //onto the stack

    //*DO A LOOP FOR EACH AUTHOR AND CHECK TO SEE IF THAT AUTHOR HAS BEEN CITED BY ORIGINAL AUTHOR

    if(this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length > 0){ 
      for(let i = 0; i < this.mockPublicationAuthor.length; i++){
        for(let j = 0; j < this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length; j++){
          if(this.mockPublicationAuthor[i].publicationID == this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication[j]){
            this.mockStackOfScholarsCitingOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].scholarID);
            //*now for each author do a loop determining if that authors publication has been cited by original author
          }
        }
      }
    }
    // debugger; //1234567890
    //loop through this.mockStackOfScholarsCitingOriginalAuthorsPublication, find all of their publications
    //and store them
    // debugger;
    if(this.mockStackOfScholarsCitingOriginalAuthorsPublication.length > 0){
      for(let i = 0; i < this.mockPublicationAuthor.length; i++){
        for(let j = 0; j < this.mockStackOfScholarsCitingOriginalAuthorsPublication.length; j++){
          if(this.mockPublicationAuthor[i].scholarID == this.mockStackOfScholarsCitingOriginalAuthorsPublication[j]){
            this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.push(this.mockPublicationAuthor[i].publicationID);
          }
          //store the scholars publications
          
        }
      }
    }
    // debugger;
    //loop through the stack of publications that have cited the original scholars publications
    //check to see if these publications have been cited by the original scholars from the (this.mockStackOfScholarsPublication)
    // same this.mockPublicationCites database
    
    if(this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length > 0){

      for(let i = 0; i < this.mockPublicationCites.length; i++){
        for(let j = 0; j < this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length; j++){ 
        
          if (this.mockPublicationCites[i].publicationID == this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor[j]){ //if a publicationID is the same as the publicationID that cited the original scholars publication
              //check to see if the on the cited section it contains the original scholars publication 

                if(this.mockStackOfOriginalAuthorsPublication.indexOf(this.mockPublicationCites[i].publicationIDFK) > -1){ //if the orignal scholars publication is citing the publication of authors that had cited the original author
                //store the element.publicationID (which is the publicationID of publications that had cited the original scholars publication)
                //store all the publications  of scholars that have cited the original author that is cited by original othercited by the original  
                this.mockStorePublicationsCitedByOriginalAuthor.push(this.mockPublicationCites[i].publicationID); 
                }
          }
      }

      }
    }
    //debugger; // this.mockStorePublicationsCitedByOriginalAuthor = 5
    //double check with john and cano about what this database actually contains 
    // (what if authors who are cited by original authors are not on the mockPublicationAuthorDatabase)

     
    if(this.mockStorePublicationsCitedByOriginalAuthor.length > -1){
       //loop through mockPublicationAuthor Database
       for(let i = 0; i < this.mockPublicationAuthor.length; i++){
         for(let j = 0; j < this.mockStorePublicationsCitedByOriginalAuthor.length; j++){
          //  debugger;
           if(this.mockPublicationAuthor[i].publicationID == this.mockStorePublicationsCitedByOriginalAuthor[j]){
             //check to see if author of that publication is in this.mockStackOfScholarsCitingOriginalAuthorsPublication.
             //which ensures that we are only including authors that are cited by original author
             if(this.mockStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.mockPublicationAuthor[i].scholarID ) > -1){
              let newObj = {scholarID1: mockScholarID, scholarID2: this.mockPublicationAuthor[i].scholarID}
              this.mockScholarsCitingEachOther.push(newObj);
             }
           }
         }
       }
      }

    // debugger;
    //logic for when user enters another name, and that name of the previous scholar includes that new name under
    //mock scholars citing each other, then don't repeat it, this should also be where we keep count of which scholar is citing who
    let newObj = []
    if(this.mockScholarsCitingEachOther.length > 0){ //unecessary delete later
      for(let i = 0; i <this.mockScholars.length; i++){
        for(let j = 0; j < this.mockScholarsCitingEachOther.length; j++){
          
          if(this.mockScholars[i].id == this.mockScholarsCitingEachOther[j].scholarID2){
  
                newObj.push({full_name: this.scholarsInput[m], scholarID2: this.mockScholars[i].full_name})
              // if(this.mockScholarsCitingEachOtherNames.length > 0 ){
              //   if(this.mockScholars[i].full_name != this.mockScholarsCitingEachOtherNames[j].full_name
              //     && newScholar != this.mockScholarsCitingEachOtherNames[j].scholarID2) {
              //   this.mockScholarsCitingEachOtherNames.push(newObj);
              // }
            // }
            
          }
          
        }
      }
    }
      //now loop through all the new obj found and make sure that we are not adding repeated information
      // debugger;
      //just loop through citingEachOthersName if newObj[i] == it then increment i and start citing each others name at 0
      if(this.mockScholarsCitingEachOtherNames.length > 0 ){
      let i = 0
      let savedIndex= [];
      for(let i = 0; i < newObj.length; i++){
      for(let j = 0; j < this.mockScholarsCitingEachOtherNames.length; j++){
       
        
        if((newObj[i].full_name == this.mockScholarsCitingEachOtherNames[j].scholarID2
             && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNames[j].full_name)) {
              newObj.splice(i,1); 
            i = 0;
             }
        
        if(newObj[i].full_name == this.mockScholarsCitingEachOtherNames[j].full_name
              && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNames[j].scholarID2) {    
            newObj.splice(i,1);
            i = 0;
        }
      }
        
      } 
      for(let i = 0; i < newObj.length; i++){
        this.mockScholarsCitingEachOtherNames.push(newObj[i]);
      }
    }
    else {
      for(let i = 0; i < newObj.length; i++){
      this.mockScholarsCitingEachOtherNames.push({full_name: newObj[i].full_name, scholarID2: newObj[i].scholarID2});
      }
      
    }
    debugger;
  }


  }


  title = 'ScholarScraperFE';


 constructor(private _apiservice: ApiService){}
 
  ngOnInit(){
    
    this._apiservice.getScholars().subscribe(data => this.scholars = data); //uncomment when using publication-cites api
    
    
    
    // this.scholars = this.mockscholars;

  }
}

//WHAT IF INSTEAD OF DOUBLE FOR LOOPS I JUST DIRECTLY ACCESS IT IN IF STATEMENTS BUT WAIT NO