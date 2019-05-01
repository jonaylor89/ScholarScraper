import { Component,ElementRef, OnInit,ViewEncapsulation, ViewChild, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ApiService } from './api.service';
import { Breakpoints } from '@angular/cdk/layout';
import * as d3 from 'd3'
import { debugOutputAstAsTypeScript } from '@angular/compiler';

//TODO
//Show count
//Display it using some Javascript library
//Prevent User from adding/deleting the same scholar twice 
//figure out how to save previous data so this process doesn't take long (after finding all citating store that author citations)
interface Node {
  id: string;
  group: number;
}

interface Link {
  source: string;
  target: string;
  value: number;
}

interface Graph {
  nodes: Node[];
  links: Link[];
}

/** @title Simple form field */
@Component({
  selector: 'form-field-overview-example',
  templateUrl: 'form-field-overview-example.html',
  styleUrls: ['form-field-overview-example.css'],
  encapsulation: ViewEncapsulation.None
})
export class FormFieldOverviewExample implements OnChanges, OnInit {
//D3 Set up//
@ViewChild('graph')
  private chartContainer: ElementRef;
  
@Input() data:any;


ngOnInit() {
    
    this._apiservice.getScholars().subscribe(data => this.apiScholars = data); //uncomment when using publication-cites api
    this._apiservice.getPublication().subscribe(data => this.apiPublications = data); //uncomment when using publication-cites api
    this._apiservice.getPublicationCites().subscribe(data => this.apiPublicationCites = data); //uncomment when using publication-cites api
    this._apiservice.getPublicationAuthor().subscribe(data => this.apiPublicationAuthor = data); //uncomment when using publication-cites api
    this._apiservice.getTotalCitations().subscribe(data => this.apiTotalCitations = data); //uncomment when using publication-cites api

    this.buildGraph();
    // this.initialized =true;

    
  }

  
ngOnChanges(changes: SimpleChanges) {
  // if(this.initialized){
  // this.buildGraph();
  // }
  // console.log(this.initialized);
  // this.initialized = false;
  // console.log(this.initialized);
  console.log(changes);
}
  
 
  
////////////////SCHOLAR SCRAPER LOGIC////////////////////
  public apiScholars = [];
  public scholarsInput = [];

  //input of user
  public mockScholarsInput = ["Alberto Cano"];

  //database to map user input to an id
  public mockScholars = [
    { full_name: "Alberto Cano", id: "8f_w4HQAAAAJ" },
    { full_name: "Dr Seuss", id: "1234567890" },
    { full_name: "Dr Zeus", id: "123" }
  ];

  //database to map scholarID to PublicationID
  public mockPublicationAuthor = [
    { scholarID: "8f_w4HQAAAAJ", publicationID: "1" },
    { scholarID: "8f_w4HQAAAAJ", publicationID: "2" },
    { scholarID: "8f_w4HQAAAAJ", publicationID: "3" },
    { scholarID: "1234567890", publicationID: "4" },
    { scholarID: "1234567890", publicationID: "5" },
    { scholarID: "1234567890", publicationID: "6" },
    { scholarID: "123", publicationID: "7" }
  ];

  //database that displays publications that cite each other
  public mockPublicationCites = [
    { publicationID: "1", publicationIDFK: '5' },
    { publicationID: "1", publicationIDFK: '4' },
    { publicationID: "6", publicationIDFK: '1' },
    { publicationID: "5", publicationIDFK: '2' },
    { publicationID: "6", publicationIDFK: '7' },
    { publicationID: "7", publicationIDFK: '6' },
    { publicationID: "7", publicationIDFK: '6' }

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
  public mockScholarsCitingEachOtherNamesLinks; //their actual names scholar: , citedby:
  public mockScholarsCitingEachOtherNamesNodes;  
  public combinedNodesAndLinks = [];
  public mockStorePublicationsCitedByOriginalAuthor;
  public mockStackOfScholarsCitingOriginalAuthorsPublication;
  public mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor;
  public citationCount = [];
  public displayData = false;
  public scholarCitationCount = [];


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


  }

  public apiPublications;
  public apiPublicationCites;
  public apiPublicationAuthor;
  public apiTotalCitations;
  public realStackOfOriginalAuthorsPublication;
  public realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication;
  public realStackOfScholarsCitingOriginalAuthorsPublication;
  public realStorePublicationsCitedByOriginalAuthor;
  public realStackOfAllPublicationsFromAuthorsCitingOriginalAuthor;
  public realScholarsCitingEachOther;
  public realScholarsCitingEachOtherNamesLinks;
  public realScholarsCitingEachOtherNamesNodes;
  apiResults(){
    this.data = true;
    // debugger;
    this.realScholarsCitingEachOtherNamesLinks = []; //their actual names scholar: , citedby: 
    this.realScholarsCitingEachOtherNamesNodes = []; 
    this.scholarCitationCount = [];
    let recordOfCitations = []
    this.realScholarsCitingEachOther = [];
    for (let m = 0; m < this.scholarsInput.length; m++) {
      
      this.realStackOfOriginalAuthorsPublication = []; //maybe turn into an object that contains scholarID and publication id, publicationID
      this.realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication = []; //publications that cited the original scholars publication, publicationID
      this.realStackOfScholarsCitingOriginalAuthorsPublication = [];
      this.realStorePublicationsCitedByOriginalAuthor = [];
      this.realStackOfAllPublicationsFromAuthorsCitingOriginalAuthor = [];
      let countOfOriginalScholar = 0;
      let countOfCitingScholar = 0;
      // this.mockScholarsCitingEachOtherNames = []; //their actual names scholar: , citedby: 
       //scholarID1 : scholarID2
      let realScholarID = '';
      // let name = this.mockScholars[0].full_name
      debugger;
      for (let i = 0; i < this.apiScholars.length; i++) {
        if (this.scholarsInput[m] == this.apiScholars[i].full_name) {
          console.log(this.scholarsInput[m] + " is equal to " + this.apiScholars[i].full_name)
          realScholarID = this.apiScholars[i].id;
        }
      }

      //we found a scholar that maps to the scholar database
      if (realScholarID != '') {
        //cycle through all their publications and store them
        for (let i = 0; i < this.apiPublicationAuthor.length; i++) {
          if (realScholarID == this.apiPublicationAuthor[i].scholarID) {
            this.realStackOfOriginalAuthorsPublication.push(this.apiPublicationAuthor[i].publicationID); //maybe make it a hashmap all publications of specific author

          }
        }
      }


      //cycle through publications that have cited the authors publication using mockPublicationCites
      //loop through mockStackOfScholarsPublication, loop through publication cites 
      // debugger;
      if (this.realStackOfOriginalAuthorsPublication.length > 0) {
        //loop through all the publications in publicationcites. then store the publications that have cited
        //the original authors publication
        //side note: check how to see contains
        for (let i = 0; i < this.apiPublicationCites.length; i++) {
          for (let j = 0; j < this.realStackOfOriginalAuthorsPublication.length; j++) {
            if (this.realStackOfOriginalAuthorsPublication[j] == this.apiPublicationCites[i].publicationID) {

              this.realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.push(this.apiPublicationCites[i].publicationIDFK) //this will contains publications that cited original scholars publication
            }
          }
        }
      }
      // debugger; //display publication 5 (publication that cited the original author)
      //but first loop through authors publication 5 and find all the authors of publication 5, 
      //once finding all the others of publication five  loop through those authors and find all of their publications to add
      //onto the stack

      //*DO A LOOP FOR EACH AUTHOR AND CHECK TO SEE IF THAT AUTHOR HAS BEEN CITED BY ORIGINAL AUTHOR
      // debugger
      if (this.realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length > 0) {
        for (let i = 0; i < this.apiPublicationAuthor.length; i++) {
          for (let j = 0; j < this.realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length; j++) {
            if (this.apiPublicationAuthor[i].publicationID == this.realStackOfPublicationsThatHaveCitedOriginalAuthorsPublication[j]) {
              if (!(this.realStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.apiPublicationAuthor[i].scholarID) > -1)) { //find a more efficient way to do this
                this.realStackOfScholarsCitingOriginalAuthorsPublication.push(this.apiPublicationAuthor[i].scholarID);
                //*now for each author do a loop determining if that authors publication has been cited by original author
              }
            }
          }
        }
      }
      // debugger; //1234567890
      //loop through this.mockStackOfScholarsCitingOriginalAuthorsPublication, find all of their publications
      //and store them
      // debugger;
      if (this.realStackOfScholarsCitingOriginalAuthorsPublication.length > 0) {
        for (let i = 0; i < this.apiPublicationAuthor.length; i++) {
          for (let j = 0; j < this.realStackOfScholarsCitingOriginalAuthorsPublication.length; j++) {
            if (this.apiPublicationAuthor[i].scholarID == this.realStackOfScholarsCitingOriginalAuthorsPublication[j]) {
              this.realStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.push(this.apiPublicationAuthor[i].publicationID);
            }
            //store the scholars publications

          }
        }
      }
      // debugger;
      //loop through the stack of publications that have cited the original scholars publications
      //check to see if these publications have been cited by the original scholars from the (this.mockStackOfScholarsPublication)
      // same this.mockPublicationCites database
      // debugger;
      if (this.realStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length > 0) {

        for (let i = 0; i < this.apiPublicationCites.length; i++) {
          // for(let j = 0; j < this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length; j++){ 

          if (this.realStackOfOriginalAuthorsPublication.indexOf(this.apiPublicationCites[i].publicationIDFK) > -1) {
            if (this.realStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.indexOf(this.apiPublicationCites[i].publicationID) > -1) {
              this.realStorePublicationsCitedByOriginalAuthor.push(this.apiPublicationCites[i].publicationID);
            }
          }

        }
      }
      //debugger; // this.mockStorePublicationsCitedByOriginalAuthor = 5
      //double check with john and cano about what this database actually contains 
      // (what if authors who are cited by original authors are not on the mockPublicationAuthorDatabase)

      ///////////debugger
      if (this.realStorePublicationsCitedByOriginalAuthor.length > -1) {
        //loop through mockPublicationAuthor Database
        for (let i = 0; i < this.apiPublicationAuthor.length; i++) {
          for (let j = 0; j < this.realStorePublicationsCitedByOriginalAuthor.length; j++) {
            //  debugger;
            if (this.apiPublicationAuthor[i].publicationID == this.realStorePublicationsCitedByOriginalAuthor[j]) {
              //check to see if author of that publication is in this.mockStackOfScholarsCitingOriginalAuthorsPublication.
              //which ensures that we are only including authors that are cited by original author
              //  debugger;
              if (this.realStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.apiPublicationAuthor[i].scholarID) > -1) {

                let newObj_1 = { scholarID1: realScholarID, scholarID2: this.apiPublicationAuthor[i].scholarID }
                newObj_1.scholarID2;
                // debugger;
                if (this.realScholarsCitingEachOther.length > 0) {
                  let found1 = this.mockScholarsCitingEachOther.some(el => el.scholarID1 === newObj_1.scholarID2);
                  let found2 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID1);
                  let found3 = this.mockScholarsCitingEachOther.some(el => el.scholarID1 === newObj_1.scholarID1);
                  let found4 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID2);
                  if ((found1 && found2)== false){
                    if((found3 && found4)== false){ this.realScholarsCitingEachOther.push(newObj_1);
                    }
                  }
             
                }
                else {
                  this.realScholarsCitingEachOther.push(newObj_1);

                 
                }
              }
            }
          }
        }
      }   
  }
  // debugger;
  for (let i = 0; i < this.realScholarsCitingEachOther.length; i++) {
    let publicationsOfScholar1 = [];
    let publicationsOfScholar2 = [];
    let countOfOriginalScholar = 0;
    let countOfCitingScholar = 0;
    // debugger;

    for (let j = 0; j < this.mockPublicationAuthor.length; j++) {
      if (this.realScholarsCitingEachOther[i].scholarID1 == this.apiPublicationAuthor[j].scholarID) {
        //do a arr.some to prevent storing the same publications multiple times
        let found = publicationsOfScholar1.some(el => el === this.apiPublicationAuthor[j].publicationID);
        if (!found)
          publicationsOfScholar1.push(this.apiPublicationAuthor[j].publicationID);
      }
      if (this.realScholarsCitingEachOther[i].scholarID2 == this.apiPublicationAuthor[j].scholarID) {
        //do a arr.some
        let found = publicationsOfScholar2.some(el => el === this.apiPublicationAuthor[j].publicationID);
        if (!found)
          publicationsOfScholar2.push(this.apiPublicationAuthor[j].publicationID);
      }

    }

    //further logic for counting
    //then clear out the two arrays and do another count
    //loop thorugh scholar citing each other
    // debugger;
    for (let k = 0; k < this.apiPublicationCites.length; k++) {

      if ((publicationsOfScholar1.indexOf(this.apiPublicationCites[k].publicationID) > -1)
        && (publicationsOfScholar2.indexOf(this.apiPublicationCites[k].publicationIDFK) > -1)) {
        countOfCitingScholar++;
      }

      if ((publicationsOfScholar2.indexOf(this.apiPublicationCites[k].publicationID) > -1)
        && (publicationsOfScholar1.indexOf(this.apiPublicationCites[k].publicationIDFK) > -1)) {
        countOfOriginalScholar++;
      }
    }
    
   
    // debugger;
    this.scholarCitationCount.push({number1: countOfOriginalScholar, number2: countOfCitingScholar});

    
    //  let found = publicationsOfScholar1.some()
  } 

  //find the scholar names for the id of scholar cites 
    let linksObj= [];
    let scholar_name1 = '';
    let scholar_name2 = '';
    // if (this.mockScholarsCitingEachOther.length > 0) { //unecessary delete later
        for (let i = 0; i <  this.realScholarsCitingEachOther.length; i++) {
          for (let j = 0; j <this.apiScholars.length; j++) {

            if(this.realScholarsCitingEachOther[i].scholarID1=== this.apiScholars[j].id){
              scholar_name1 = this.apiScholars[j].full_name
            }

            if(this.realScholarsCitingEachOther[i].scholarID2=== this.apiScholars[j].id){
              scholar_name2 = this.apiScholars[j].full_name
            }

            if(scholar_name1.length > 0 && scholar_name2.length > 0){
              // debugger
              linksObj.push({"scholarname1": scholar_name1, "number1": this.scholarCitationCount[i].number1, "scholarname2": scholar_name2, "number2": this.scholarCitationCount[i].number2,"value": 1})
              this.realScholarsCitingEachOtherNamesNodes.push({"id": scholar_name1, "group": 1});
              this.realScholarsCitingEachOtherNamesNodes.push({"id": scholar_name2, "group": 1});
              scholar_name1 = '';
              scholar_name2 = '';
            }

       }
        }
        // }
        debugger;
    for(let i = 0; i < this.scholarCitationCount.length; i++){
    this.realScholarsCitingEachOtherNamesLinks[i]= linksObj[i];
  }
  debugger;

}
  //////////////////////////SUBMIT RESULTS///////////////////

  submitResults() {
    this.data = true;
    // debugger;
    this.mockScholarsCitingEachOtherNamesLinks = []; //their actual names scholar: , citedby: 
    this.mockScholarsCitingEachOtherNamesNodes = []; 
    this.scholarCitationCount = [];
    let recordOfCitations = []
    this.mockScholarsCitingEachOther = [];
    for (let m = 0; m < this.scholarsInput.length; m++) {
      
      this.mockStackOfOriginalAuthorsPublication = []; //maybe turn into an object that contains scholarID and publication id, publicationID
      this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication = []; //publications that cited the original scholars publication, publicationID
      this.mockStackOfScholarsCitingOriginalAuthorsPublication = [];
      this.mockStorePublicationsCitedByOriginalAuthor = [];
      this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor = [];
      let countOfOriginalScholar = 0;
      let countOfCitingScholar = 0;
      // this.mockScholarsCitingEachOtherNames = []; //their actual names scholar: , citedby: 
       //scholarID1 : scholarID2
      let mockScholarID = '';
      // let name = this.mockScholars[0].full_name
     
      for (let i = 0; i < this.mockScholars.length; i++) {
        if (this.scholarsInput[m] == this.mockScholars[i].full_name) {
          console.log(this.scholarsInput[m] + " is equal to " + this.mockScholars[i].full_name)
          mockScholarID = this.mockScholars[i].id;
        }
      }

      //we found a scholar that maps to the scholar database
      if (mockScholarID != '') {
        //cycle through all their publications and store them
        for (let i = 0; i < this.mockPublicationAuthor.length; i++) {
          if (mockScholarID == this.mockPublicationAuthor[i].scholarID) {
            this.mockStackOfOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].publicationID); //maybe make it a hashmap all publications of specific author

          }
        }
      }


      //cycle through publications that have cited the authors publication using mockPublicationCites
      //loop through mockStackOfScholarsPublication, loop through publication cites 
      // debugger;
      if (this.mockStackOfOriginalAuthorsPublication.length > 0) {
        //loop through all the publications in publicationcites. then store the publications that have cited
        //the original authors publication
        //side note: check how to see contains
        for (let i = 0; i < this.mockPublicationCites.length; i++) {
          for (let j = 0; j < this.mockStackOfOriginalAuthorsPublication.length; j++) {
            if (this.mockStackOfOriginalAuthorsPublication[j] == this.mockPublicationCites[i].publicationID) {

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
      // debugger
      if (this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length > 0) {
        for (let i = 0; i < this.mockPublicationAuthor.length; i++) {
          for (let j = 0; j < this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication.length; j++) {
            if (this.mockPublicationAuthor[i].publicationID == this.mockStackOfPublicationsThatHaveCitedOriginalAuthorsPublication[j]) {
              if (!(this.mockStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.mockPublicationAuthor[i].scholarID) > -1)) { //find a more efficient way to do this
                this.mockStackOfScholarsCitingOriginalAuthorsPublication.push(this.mockPublicationAuthor[i].scholarID);
                //*now for each author do a loop determining if that authors publication has been cited by original author
              }
            }
          }
        }
      }
      // debugger; //1234567890
      //loop through this.mockStackOfScholarsCitingOriginalAuthorsPublication, find all of their publications
      //and store them
      // debugger;
      if (this.mockStackOfScholarsCitingOriginalAuthorsPublication.length > 0) {
        for (let i = 0; i < this.mockPublicationAuthor.length; i++) {
          for (let j = 0; j < this.mockStackOfScholarsCitingOriginalAuthorsPublication.length; j++) {
            if (this.mockPublicationAuthor[i].scholarID == this.mockStackOfScholarsCitingOriginalAuthorsPublication[j]) {
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
      // debugger;
      if (this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length > 0) {

        for (let i = 0; i < this.mockPublicationCites.length; i++) {
          // for(let j = 0; j < this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.length; j++){ 

          if (this.mockStackOfOriginalAuthorsPublication.indexOf(this.mockPublicationCites[i].publicationIDFK) > -1) {
            if (this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor.indexOf(this.mockPublicationCites[i].publicationID) > -1) {
              this.mockStorePublicationsCitedByOriginalAuthor.push(this.mockPublicationCites[i].publicationID);
            }
          }
          // if (this.mockPublicationCites[i].publicationID == this.mockStackOfAllPublicationsFromAuthorsCitingOriginalAuthor[j]){ //if a publicationID is the same as the publicationID that cited the original scholars publication
          //     //check to see if the on the cited section it contains the original scholars publication 

          //       // if(this.mockStackOfOriginalAuthorsPublication.indexOf(this.mockPublicationCites[i].publicationIDFK) > -1){ //if the orignal scholars publication is citing the publication of authors that had cited the original author
          //       //store the element.publicationID (which is the publicationID of publications that had cited the original scholars publication)
          //       //store all the publications  of scholars that have cited the original author that is cited by original othercited by the original  
          //       this.mockStorePublicationsCitedByOriginalAuthor.push(this.mockPublicationCites[i].publicationID); 
          //       // }
          // }
          // }

        }
      }
      //debugger; // this.mockStorePublicationsCitedByOriginalAuthor = 5
      //double check with john and cano about what this database actually contains 
      // (what if authors who are cited by original authors are not on the mockPublicationAuthorDatabase)

      ///////////debugger
      if (this.mockStorePublicationsCitedByOriginalAuthor.length > -1) {
        //loop through mockPublicationAuthor Database
        for (let i = 0; i < this.mockPublicationAuthor.length; i++) {
          for (let j = 0; j < this.mockStorePublicationsCitedByOriginalAuthor.length; j++) {
            //  debugger;
            if (this.mockPublicationAuthor[i].publicationID == this.mockStorePublicationsCitedByOriginalAuthor[j]) {
              //check to see if author of that publication is in this.mockStackOfScholarsCitingOriginalAuthorsPublication.
              //which ensures that we are only including authors that are cited by original author
              //  debugger;
              if (this.mockStackOfScholarsCitingOriginalAuthorsPublication.indexOf(this.mockPublicationAuthor[i].scholarID) > -1) {

                let newObj_1 = { scholarID1: mockScholarID, scholarID2: this.mockPublicationAuthor[i].scholarID }
                newObj_1.scholarID2;
                // debugger;
                if (this.mockScholarsCitingEachOther.length > 0) {
                  let found1 = this.mockScholarsCitingEachOther.some(el => el.scholarID1 === newObj_1.scholarID2);
                  let found2 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID1);
                  let found3 = this.mockScholarsCitingEachOther.some(el => el.scholarID1 === newObj_1.scholarID1);
                  let found4 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID2);
                  // let found3 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID2);
                  // let found4 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID1);
                  // let found2 = this.mockScholarsCitingEachOther.some(el => el.scholarID2 === newObj_1.scholarID2);
                  if ((found1 && found2)== false){
                    if((found3 && found4)== false){ this.mockScholarsCitingEachOther.push(newObj_1);
                    }
                  }
                  //   if(!(this.mockScholarsCitingEachOther.indexOf(newObj_1.scholarID2)>-1)){
                  //     debugger;


                  // }


                }
                else {
                  this.mockScholarsCitingEachOther.push(newObj_1);

                  // if(recordOfCitations.length < 1){
                  //   recordOfCitations.push(newObj_1);
                  // } else if(recordOfCitations.indexOf(newObj_1) > -1 && recordOfCitations.indexOf(newObj_1) > -1 && ) {
                    
                  // }
                }
              }
            }
          }
        }
      }


      // debugger;
      //logic for when user enters another name, and that name of the previous scholar includes that new name under
      //mock scholars citing each other, then don't repeat it, this should also be where we keep count of which scholar is citing who
      // let newObj = []
      // if (this.mockScholarsCitingEachOther.length > 0) { //unecessary delete later
      //   for (let i = 0; i < this.mockScholars.length; i++) {
      //     for (let j = 0; j < this.mockScholarsCitingEachOther.length; j++) {

      //       if (this.mockScholars[i].id == this.mockScholarsCitingEachOther[j].scholarID2) {

      //         newObj.push({ full_name: this.scholarsInput[m], scholarID2: this.mockScholars[i].full_name })
      //         // if(this.mockScholarsCitingEachOtherNames.length > 0 ){
      //         //   if(this.mockScholars[i].full_name != this.mockScholarsCitingEachOtherNames[j].full_name
      //         //     && newScholar != this.mockScholarsCitingEachOtherNames[j].scholarID2) {
      //         //   this.mockScholarsCitingEachOtherNames.push(newObj);
      //         // }
      //         // }

      //       }

      //     }
      //   }
      // }
      // //now loop through all the new obj found and make sure that we are not adding repeated information
      // // debugger;
      // //just loop through citingEachOthersName if newObj[i] == it then increment i and start citing each others name at 0
      // // debugger;
      // if (this.mockScholarsCitingEachOtherNamesLinks.length > 0) {
       
      //   for (let i = 0; i < newObj.length; i++) {
      //     for (let j = 0; j < this.mockScholarsCitingEachOtherNamesLinks.length; j++) {


      //       if ((newObj[i].full_name == this.mockScholarsCitingEachOtherNamesLinks[j].scholarID2
      //         && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNamesLinks[j].full_name)) {
      //         newObj.splice(i, 1);
      //         i = 0;
      //       }
      //       else
      //       if (newObj[i].full_name == this.mockScholarsCitingEachOtherNamesLinks[j].full_name
      //         && newObj[i].scholarID2 == this.mockScholarsCitingEachOtherNamesLinks[j].scholarID2) {
      //         newObj.splice(i, 1);
      //         i = 0;
      //       }
      //     }

      //   }
      //   for (let i = 0; i < newObj.length; i++) {
      //     this.mockScholarsCitingEachOtherNamesLinks.push(newObj[i]);
      //     // this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].full_name, "group": 1})
      //     // this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].scholarID2, "group": 1})
      //   }
      // }
      // else {
      //   // debugger;
      //   for (let i = 0; i < newObj.length; i++) {
      //     this.mockScholarsCitingEachOtherNamesLinks.push({ full_name: newObj[i].full_name, scholarID2: newObj[i].scholarID2, value: 1 });
      //     this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].full_name, "group": 1})
      //     this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].scholarID2, "group": 1})
      //   }

      // }

      //To get the count look at 
      //mockScholarsCitingEachOther
      //mockPublicationAuthor
      //mockPublicationCites
      // do a let find = arr.some
      // if true then store it
      //first check if scholarID is matching scholarID 1, then check if scholar ID2 is matching scholar ID 

      //make these lists empty for when looping to the next this.mockScholarsCitingEachOther

      // for()
      // this.combinedNodesAndLinks.push({"nodes": this.mockScholarsCitingEachOtherNamesNodes,"links": this.mockScholarsCitingEachOtherNamesLinks});
      // debugger;
      
  }
  // debugger;
  for (let i = 0; i < this.mockScholarsCitingEachOther.length; i++) {
    let publicationsOfScholar1 = [];
    let publicationsOfScholar2 = [];
    let countOfOriginalScholar = 0;
    let countOfCitingScholar = 0;
    // debugger;

    for (let j = 0; j < this.mockPublicationAuthor.length; j++) {
      if (this.mockScholarsCitingEachOther[i].scholarID1 == this.mockPublicationAuthor[j].scholarID) {
        //do a arr.some to prevent storing the same publications multiple times
        let found = publicationsOfScholar1.some(el => el === this.mockPublicationAuthor[j].publicationID);
        if (!found)
          publicationsOfScholar1.push(this.mockPublicationAuthor[j].publicationID);
      }
      if (this.mockScholarsCitingEachOther[i].scholarID2 == this.mockPublicationAuthor[j].scholarID) {
        //do a arr.some
        let found = publicationsOfScholar2.some(el => el === this.mockPublicationAuthor[j].publicationID);
        if (!found)
          publicationsOfScholar2.push(this.mockPublicationAuthor[j].publicationID);
      }

    }

    //further logic for counting
    //then clear out the two arrays and do another count
    //loop thorugh scholar citing each other
    // debugger;
    for (let k = 0; k < this.mockPublicationCites.length; k++) {

      if ((publicationsOfScholar1.indexOf(this.mockPublicationCites[k].publicationID) > -1)
        && (publicationsOfScholar2.indexOf(this.mockPublicationCites[k].publicationIDFK) > -1)) {
        countOfCitingScholar++;
      }

      if ((publicationsOfScholar2.indexOf(this.mockPublicationCites[k].publicationID) > -1)
        && (publicationsOfScholar1.indexOf(this.mockPublicationCites[k].publicationIDFK) > -1)) {
        countOfOriginalScholar++;
      }
      //     this.mockScholarsCitingEachOtherNamesLinks[k].number1 = countOfOriginalScholar;
      // this.mockScholarsCitingEachOtherNamesLinks[k].number2 = countOfCitingScholar;
    }
    
    // if(this.mockScholarsCitingEachOther.length == 1){
    //   this.mockScholarsCitingEachOtherNamesLinks[m].number1 = countOfOriginalScholar;
    //   this.mockScholarsCitingEachOtherNamesLinks[m].number2 = countOfCitingScholar;
    // }
     //     this.mockScholarsCitingEachOtherNamesLinks.push({ full_name: newObj[i].full_name, scholarID2: newObj[i].scholarID2, value: 1 });
      //     this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].full_name, "group": 1})
   
    // debugger;
    this.scholarCitationCount.push({number1: countOfOriginalScholar, number2: countOfCitingScholar});

    
    //  let found = publicationsOfScholar1.some()
  } 

  //find the scholar names for the id of scholar cites 
    let linksObj= [];
    let scholar_name1 = '';
    let scholar_name2 = '';
    // if (this.mockScholarsCitingEachOther.length > 0) { //unecessary delete later
        for (let i = 0; i <  this.mockScholarsCitingEachOther.length; i++) {
          for (let j = 0; j <this.mockScholars.length; j++) {

            if(this.mockScholarsCitingEachOther[i].scholarID1=== this.mockScholars[j].id){
              scholar_name1 = this.mockScholars[j].full_name
            }

            if(this.mockScholarsCitingEachOther[i].scholarID2=== this.mockScholars[j].id){
              scholar_name2 = this.mockScholars[j].full_name
            }

            if(scholar_name1.length > 0 && scholar_name2.length > 0){
              // debugger
              linksObj.push({"scholarname1": scholar_name1, "number1": this.scholarCitationCount[i].number1, "scholarname2": scholar_name2, "number2": this.scholarCitationCount[i].number2,"value": 1})
              this.mockScholarsCitingEachOtherNamesNodes.push({"id": scholar_name1, "group": 1});
              this.mockScholarsCitingEachOtherNamesNodes.push({"id": scholar_name2, "group": 1});
              scholar_name1 = '';
              scholar_name2 = '';
            }

            // if (this.mockScholars[i].id == this.mockScholarsCitingEachOther[j].scholarID2) {

             
              // newObj.push({ full_name: this.scholarsInput[m], scholarID2: this.mockScholars[i].full_name })
              // if(this.mockScholarsCitingEachOtherNames.length > 0 ){
              //   if(this.mockScholars[i].full_name != this.mockScholarsCitingEachOtherNames[j].full_name
              //     && newScholar != this.mockScholarsCitingEachOtherNames[j].scholarID2) {
              //   this.mockScholarsCitingEachOtherNames.push(newObj);
              // }
              // }
            // }
          }
        }
        // }
        debugger;
    for(let i = 0; i < this.scholarCitationCount.length; i++){
    this.mockScholarsCitingEachOtherNamesLinks[i]= linksObj[i];
    // this.mockScholarsCitingEachOtherNamesLinks[i].number2 = this.scholarCitationCount[i].number2;
    // this.mockScholarsCitingEachOtherNamesLinks.push({ scholar_name1: newObj[i].scholar_name1, scholar_name2: newObj[i].scholar_name2, value: 1 });
        // this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].scholar_name1, "group": 1})
        // this.mockScholarsCitingEachOtherNamesNodes.push({"id": newObj[i].scholar_name2, "group": 1})
  }
  debugger;

}


  title = 'ScholarScraperFE';


  constructor(private _apiservice: ApiService) { }
  
  
  
  


  

  //delete scholars from this.mockScholarsCitingEachOtherNames if full_name == scholar trying to delete
  //and make sure that the scholar in scholarID2 does not exist in the scholar input
  deleteScholar(deleteScholar: string) {
    for (let i = 0; i < this.scholarsInput.length; i++) {
      if (this.scholarsInput[i] == deleteScholar) {
        this.scholarsInput.splice(i, 1);
      }
    }

  }

  ///////////////D3.js Logic///////////////
  buildGraph(){
    // d3.select('svg').remove();
    // const element = this.chartContainer.nativeElement;
  // const data = this.data;
    const svg = d3.select('svg');
  const width = +svg.attr('width');
  const height = +svg.attr('height');

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id((d: any) => d.id))
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(width / 2, height / 2));

    let data = {
      nodes: [{id: "Alberto Cano", group: 1},
       {id: "Dr Seuss", group: 1}],
      links: [{source: "Alberto Cano", target: "Dr Seuss", value: 1, number1: 2, number2: 2}]
    }
    
    const nodes: Node[] = [...data.nodes];
    const links: Link[] = [...data.links];
    
    const graph: Graph = <Graph>{ nodes, links };

    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(graph.links)
      .enter()
      .append('line')
      .attr('stroke-width', (d: any) => Math.sqrt(d.value));

    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(graph.nodes)
      .enter()
      .append('circle')
      .attr('r', 5)
      .attr('fill', (d: any) => color(d.group));


    svg.selectAll('circle').call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended)
    );

    node.append('title')
      .text((d) => d.id);

    simulation
      .nodes(graph.nodes)
      .on('tick', ticked);

    simulation.force<d3.ForceLink<any, any>>('link')
      .links(graph.links);

    function ticked() {
      debugger;
      link
        .attr('x1', function(d: any) { return d.source.x; })
        .attr('y1', function(d: any) { return d.source.y; })
        .attr('x2', function(d: any) { return d.target.x; })
        .attr('y2', function(d: any) { return d.target.y; });

      node
        .attr('cx', function(d: any) { return d.x; })
        .attr('cy', function(d: any) { return d.y; });
    }


  function dragstarted(d) {
    if (!d3.event.active) { simulation.alphaTarget(0.3).restart(); }
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) { simulation.alphaTarget(0); }
    d.fx = null;
    d.fy = null;
  }
  }


}