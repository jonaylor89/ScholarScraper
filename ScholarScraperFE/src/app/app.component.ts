import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  scholars = [];
  addScholar(newScholar: string) {
    if (newScholar) {
      this.scholars.push(newScholar);
    }
  }

    deleteScholar(deleteScholar: string) {
      console.log(this.scholars)
      for (var i = 0; i < this.scholars.length; i++) {
        if(this.scholars[i] === deleteScholar){
          this.scholars.splice(i,1);
        }
      }
      
    
  
    
    
    // document.getElementById('button').onclick = function() {
    //   // alert("button was clicked");
    //   var scholarID = document.getElementById('scholarID').innerText;
    //   alert(scholarID + "Hello");
    // }​
  }
  title = 'ScholarScraperFE';
}


