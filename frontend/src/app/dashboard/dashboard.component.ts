import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { UserService } from '../user.service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(private http:HttpClient,private user:UserService) { }
  //https://pivasbot.appspot.com/api/getExample/
  ngOnInit() {
    //this.data=
    this.http.get("https://pivasbot.appspot.com/api/getDashboard/?user="+this.user.getUserId()).subscribe((data:any)=>{
      this.nameBot = data.nameBot;
      this.linkBot = data.linkBot;
      this.currFriends=data.currFriends;
      this.maxFriends=data.maxFriends;
      this.steamMessages=data.steamMessages;
    });
    //this.http.get("https://alpha.gosu.ai/offpubg/api/profile/391917310").subscribe((data: any) => {
       // this.currFriends= data.data.profile_stats.all_matches;
      // this.matches=data.data.matches;
   // });
    
    
  }
  
  public steamMessages : Array<any>;
  public currFriends: number;
  public maxFriends: number;
  public nameBot: string;
  public linkBot: string;


}
