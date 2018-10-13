import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(private http:HttpClient) { }
  //https://pivasbot.appspot.com/api/getExample/
  ngOnInit() {
    //this.data=
    this.http.get("https://pivasbot.appspot.com/api/getExample/").subscribe();
    this.http.get("https://alpha.gosu.ai/offpubg/api/profile/391917310").subscribe((data: any) => {
        this.currFriends= data.data.profile_stats.all_matches;
       this.matches=data.data.matches;
    });
    
    
  }
  
  public matches : Array<any>;
  public currFriends: number;


}
