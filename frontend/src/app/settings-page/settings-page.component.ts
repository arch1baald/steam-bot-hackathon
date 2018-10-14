import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { UserService } from '../user.service';

import {ModalViewComponent} from '../modal-view/modal-view.component';
import {Router} from '@angular/router';

import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.css']
})
export class SettingsPageComponent implements OnInit {

  constructor(private http:HttpClient,private popup:MatDialog, private router:Router,private user:UserService) { }

  ngOnInit() {
    this.http.get("https://pivasbot.appspot.com/api/getSettings/?user="+this.user.getUserId()).subscribe((data: any) => {
       // this.currFriends= data.data.profile_stats.all_matches;
       //this.matches=data.data.matches;
       this.botName=data.botName;
       this.botDiscription=data.botDiscription;
       this.botWelcome = data.botWelcome;
       this.botRespond = data.botRespond;
    });
    
    this.http.get("https://pivasbot.appspot.com/api/acceptFriendRequests/?user=Dmitry").subscribe();
  }
  public botName: string = "adhjcgauygscagscy";
  public botDiscription : string;
  public botWelcome : string;
  public botRespond : string;
  //public 

   public sendSettings(botName: string, botDiscription : string, botWelcome : string, botRespond : string): void
  {
      //this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
    
     this.http.post("https://pivasbot.appspot.com/api/setSettings/",{"user": this.user.getUserId(),"name": botName, "discription": botDiscription, "welcome": botWelcome, "respond": botRespond}).subscribe();
     this.displayPopup("Settings changed");
  } 
  public displayPopup(text:string):void
  {
    this.popup.open(ModalViewComponent).afterClosed().subscribe(result => {
      this.router.navigate(["/dashboard"]);
      //window.location.reload();
    });;
  }

}
